#!/usr/bin/env python3
"""
select.py -- which of the 741 posts' experiments can be replicated on one RTX 3090 (24 GB)?

Reads p3/claims/*.json + union.json, parses the model sizes the extractors recorded, and tiers
each post by whether its largest model fits the card under the most demanding thing the post
appears to do (inference / LoRA / full fine-tune). Requires shipped code and a quantitative
headline number, because a replication needs a target.

Usage:  python3 replication/select.py            # table + replication/candidates.json
        python3 replication/select.py --all      # include tier-3 (does not fit) for the record

Tiers (24 GB, single card, no offload):
  T1  fits comfortably   -- largest model <= 9B params; no full fine-tune above 1.5B
  T2  fits with tricks   -- <= 14B (8-bit / QLoRA), or <= 32B inference-only at 4-bit,
                            or gpt-oss-20b (native MXFP4). Fidelity-to-original is a risk.
  T3  does not fit       -- anything larger, or full fine-tune of a >1.5B model
Every tier is a heuristic from strings an LLM extracted; the repo inspection pass is the check.
"""
import argparse, collections, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLAIMS = os.path.join(ROOT, "p3", "claims")
VRAM_GB = 24

# family -> assumed billions of params when the extractor recorded no size (conservative: the
# LARGEST commonly used member, so an unknown does not sneak into tier 1)
FAMILY_DEFAULT = {
    "gpt-2": 1.5, "gpt2": 1.5, "pythia": 2.8, "gemma": 9, "llama": 8, "qwen": 7, "qwen2.5": 7,
    "qwen3": 8, "mistral": 7, "olmo": 7, "gpt-oss": 20, "gpt-j": 6, "phi": 3.8, "tinyllama": 1.1,
    "deepseek": 671, "kimi": 1000, "glm": 355, "minimax": 456, "mixtral": 47, "qwq": 32,
    "llama 3.1": 8, "llama 3.2": 3, "llama 3.3": 70, "smollm": 1.7, "bloom": 7,
}
# named variants that carry no digit
NAMED = {"small": 0.124, "medium": 0.355, "large": 0.774, "xl": 1.5, "r1": 671, "v3": 671,
         "v3.1": 671, "k2": 1000, "k2.5": 1000, "4 scout": 109, "4 maverick": 400, "m3": 456}

SIZE_RX = re.compile(r"(\d+(?:\.\d+)?)\s*([bBmM])(?![a-zA-Z])")
MOE_RX = re.compile(r"(\d+)\s*x\s*(\d+(?:\.\d+)?)\s*[bB]")


def params_b(family, size):
    """Best-effort billions of parameters. Returns (value, how)."""
    fam = (family or "").strip().lower()
    s = (size or "").strip().lower()
    if s and s != "none":
        m = MOE_RX.search(s)
        if m:
            return float(m.group(1)) * float(m.group(2)), "moe"
        hits = SIZE_RX.findall(s)
        if hits:
            v, unit = hits[-1]
            v = float(v)
            return (v / 1000 if unit.lower() == "m" else v), "parsed"
        for k, v in NAMED.items():
            if k in s:
                return v, "named"
    for k, v in FAMILY_DEFAULT.items():
        if fam.startswith(k):
            return v, "family-default"
    return None, "unknown"


TRAIN_LM = re.compile(r"\b(fine-?tun|sft\b|lora|qlora|rlhf|dpo|grpo|ppo\b|reinforcement learning"
                      r"|unlearn|continued pretrain|distill(?:ed|ation)? (?:into|to)|train(?:ed|ing)? (?:a |the )?"
                      r"(?:model|llm|policy|lm\b))", re.I)
TRAIN_AUX = re.compile(r"\btrain(?:ed|ing)? (?:an? |the )?(?:sae|sparse autoencoder|crosscoder|probe|"
                       r"classifier|transcoder|steering|linear)", re.I)
FULL_FT = re.compile(r"\b(full(?:-| )fine-?tun|full-parameter|from scratch)\b", re.I)


def workload(c):
    text = " ".join([c.get("primary_claim") or "", c.get("quote") or "", c.get("phenomenon") or ""])
    if FULL_FT.search(text):
        return "full-ft"
    if TRAIN_LM.search(text):
        return "lm-ft"
    if TRAIN_AUX.search(text):
        return "aux-train"
    return "inference"


def tier(max_b, work, fams):
    if max_b is None:
        return "T?", "no parseable model size"
    if work == "full-ft":
        return ("T1", "full FT of <=1.5B") if max_b <= 1.5 else ("T3", f"full FT of {max_b:g}B")
    if max_b <= 9:
        return "T1", f"<= 9B ({work})"
    if any("gpt-oss" in f for f in fams) and max_b <= 20 and work == "inference":
        return "T2", "gpt-oss-20b native MXFP4, inference"
    if max_b <= 14:
        return "T2", f"{max_b:g}B needs 8-bit / QLoRA ({work})"
    if max_b <= 32 and work == "inference":
        return "T2", f"{max_b:g}B inference-only at 4-bit; fidelity risk"
    return "T3", f"{max_b:g}B ({work})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    U = json.load(open(os.path.join(ROOT, "union.json")))["records"]
    FN = json.load(open(os.path.join(ROOT, "p3", "findings_numbers.json")))
    pmap = json.load(open(os.path.join(ROOT, "p3", "phenomenon_map.json")))
    # phenomena with both signs, from findings.py's definition, recomputed here cheaply
    byp = collections.defaultdict(collections.Counter)
    C = {}
    for fn in os.listdir(CLAIMS):
        if fn.endswith(".json"):
            c = json.load(open(os.path.join(CLAIMS, fn)))
            C[fn[:-5]] = c
            ph = pmap.get(c.get("phenomenon"), c.get("phenomenon"))
            byp[ph][c.get("claim_type")] += 1
    contested = {p for p, ct in byp.items() if ct["positive"] and (ct["negative"] + ct["null"])}
    phen_n = {p: sum(ct.values()) for p, ct in byp.items()}

    rows = []
    stats = collections.Counter()
    for pid, c in C.items():
        u = U[pid]
        if c.get("primary_claim") == "STUB":
            stats["stub"] += 1
            continue
        ms = [m for m in (c.get("models") or []) if isinstance(m, dict)]
        if not ms:
            stats["no models listed"] += 1
            continue
        if not all(m.get("open_weight") for m in ms):
            stats["needs closed model"] += 1
            continue
        repo = u["own_repo"]
        if not repo:
            gh = [d for d in (c.get("depends_on") or []) if "/" in str(d) and "arxiv" not in str(d).lower()]
            stats["no own repo"] += 1
            continue
        eff = c.get("effect") or {}
        if not eff.get("value"):
            stats["no quantitative headline"] += 1
            continue
        sizes = [params_b(m.get("family"), m.get("size")) for m in ms]
        known = [v for v, _ in sizes if v is not None]
        max_b = max(known) if known else None
        fams = [str(m.get("family", "")).lower() for m in ms]
        work = workload(c)
        t, why = tier(max_b, work, fams)
        ph = pmap.get(c.get("phenomenon"), c.get("phenomenon"))
        score = 0.0
        score += 3.0 if ph in contested else 0.0
        score += 1.5 if eff.get("uncertainty_reported", "none") != "none" else 0.0
        score += {"high": 1.0, "medium": 0.3, "low": -1.0}[c.get("extractor_confidence", "low")]
        score += 1.0 if c.get("claim_type") == "negative" else 0.0
        score += 0.5 if c.get("reproducible_in_principle") == "code+data" else 0.0
        score += min(2.0, math.log1p(max(u["karma_lw"], 0)) / 3)
        score += 1.0 if (max_b or 99) <= 3 else 0.5 if (max_b or 99) <= 9 else 0.0
        score += 0.5 if phen_n.get(ph, 0) >= 3 else 0.0
        score -= 1.0 if work == "lm-ft" else 0.0
        rows.append({
            "post_id": pid, "date": u["date"], "title": u["title"], "karma_lw": u["karma_lw"],
            "in_af": u["in_af"], "repo": repo, "tier": t, "tier_reason": why,
            "max_params_b": max_b, "size_parse": [h for _, h in sizes], "workload": work,
            "models": [f"{m.get('family')} {m.get('size') or ''}".strip() for m in ms],
            "phenomenon": ph, "contested": ph in contested, "claim_type": c.get("claim_type"),
            "primary_claim": c.get("primary_claim"), "metric": eff.get("metric"),
            "target_value": eff.get("value"), "direction": eff.get("direction"),
            "uncertainty_reported": eff.get("uncertainty_reported"),
            "design": c.get("design"), "reproducible": c.get("reproducible_in_principle"),
            "extractor_confidence": c.get("extractor_confidence"), "quote": c.get("quote"),
            "score": round(score, 2),
        })
        stats[t] += 1

    rows.sort(key=lambda r: ({"T1": 0, "T2": 1, "T?": 2, "T3": 3}[r["tier"]], -r["score"]))
    keep = rows if a.all else [r for r in rows if r["tier"] in ("T1", "T2", "T?")]
    out = {"_meta": {"vram_gb": VRAM_GB, "funnel": dict(stats), "n_candidates": len(keep),
                     "n_t1": stats["T1"], "n_t2": stats["T2"], "n_unknown_size": stats["T?"],
                     "n_t3": stats["T3"], "contested_phenomena": len(contested)},
           "candidates": keep}
    json.dump(out, open(os.path.join(HERE, "candidates.json"), "w"), indent=1)

    print("funnel (741 posts):")
    for k in ["stub", "no models listed", "needs closed model", "no own repo",
              "no quantitative headline", "T3", "T?", "T2", "T1"]:
        print(f"  {stats[k]:>4}  {k}")
    print(f"\n{'tier':4} {'score':>5} {'maxB':>5} {'work':9} {'C':1} {'type':8} {'karma':>5}  title / repo")
    for r in keep[:60]:
        print(f"{r['tier']:4} {r['score']:>5} {str(r['max_params_b'] or '?'):>5} {r['workload']:9} "
              f"{'*' if r['contested'] else ' '} {r['claim_type'][:8]:8} {r['karma_lw']:>5}  "
              f"{r['title'][:52]}\n{'':36}{r['repo']}   [{r['phenomenon'][:34]}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
