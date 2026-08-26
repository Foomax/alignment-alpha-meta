#!/usr/bin/env python3
"""
pareto.py -- an 80/20 over the replication candidates: which fifth of the projects carries most
of the value of replicating, and of those, which run on the RTX 3090 in this machine?

Two families of factors, scored 0..1 each, combined as value x feasibility (a geometric mean, so
a project that is worthless OR unrunnable scores low, not average):

VALUE  -- why would anyone care whether this result holds?
  contested     the phenomenon has both positive and negative findings in the corpus (findings §1)
  phenomenon_n  how many other posts study the same phenomenon (downstream dependents)
  in_degree     how many other posts' depends_on name this post or its repo (real influence)
  attention     log LW karma, AF promotion
  negative      a negative/null/replication claim: re-verifying one is disproportionately informative
  specified     the post reported uncertainty on the headline (target is well-defined)
  rigor         baseline + ablation + held-out + seeds + >=2 model families (from the read claims)

FEASIBILITY -- can it be run here, and will the run test the published claim?
  fits          inspector's fits_3090 (yes 1, probably .8, tight .5, unknown .3, no 0)
  api           needs_closed_api -> 0 (hard)
  entrypoint    confidence high 1 / medium .6 / low .2 / none 0
  artifact      headline artifact identified in the repo
  data          in-repo/hf-hub 1, download-script .8, unknown .4, missing 0
  runtime       minutes 1, hours .7, unknown .4, days .2
  hygiene       requirements present, versions pinned, compute stated

Writes replication/pareto.json and prints the ranking. --top-frac (default 0.2) sets the cut.
"""
import argparse, collections, glob, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load():
    C = {c["post_id"]: c for c in json.load(open(os.path.join(HERE, "candidates.json")))["candidates"]}
    I = {}
    for p in sorted(glob.glob(os.path.join(HERE, "inspect", "result_*.json"))):
        for r in json.load(open(p)):
            I[r["post_id"]] = r
    claims = {}
    for fn in os.listdir(os.path.join(ROOT, "p3", "claims")):
        if fn.endswith(".json"):
            claims[fn[:-5]] = json.load(open(os.path.join(ROOT, "p3", "claims", fn)))
    U = json.load(open(os.path.join(ROOT, "union.json")))["records"]
    pmap = json.load(open(os.path.join(ROOT, "p3", "phenomenon_map.json")))
    return C, I, claims, U, pmap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-frac", type=float, default=0.2)
    a = ap.parse_args()
    C, I, claims, U, pmap = load()

    # phenomenon sizes and contestedness over the whole corpus
    byp = collections.defaultdict(collections.Counter)
    for c in claims.values():
        ph = pmap.get(c.get("phenomenon"), c.get("phenomenon"))
        byp[ph][c.get("claim_type")] += 1
    contested = {p for p, ct in byp.items() if ct["positive"] and (ct["negative"] + ct["null"])}
    phen_n = {p: sum(ct.values()) for p, ct in byp.items()}
    max_phen = max(phen_n.values())

    # in-degree: other posts naming this post id or this repo in depends_on
    indeg = collections.Counter()
    repo_of = {pid: (U[pid]["own_repo"] or "").lower() for pid in U}
    for pid, c in claims.items():
        for d in {str(x).strip().lower() for x in (c.get("depends_on") or []) if x}:
            for q in U:
                if q == pid:
                    continue
                if d == q.lower() or (repo_of[q] and d == repo_of[q]):
                    indeg[q] += 1
    max_in = max(indeg.values()) if indeg else 1

    rows = []
    for pid, c in C.items():
        r = I.get(pid, {})
        cl = claims[pid]
        u = U[pid]
        ph = c["phenomenon"]
        d = cl.get("design") or {}
        rigor = sum([bool(d.get("baseline")), bool(d.get("ablation")), bool(d.get("held_out")),
                     bool(d.get("seeds_n")), (cl.get("n_model_families") or 0) >= 2]) / 5
        value = {
            "contested": 1.0 if ph in contested else 0.0,
            "phenomenon_n": min(1.0, math.log1p(phen_n.get(ph, 1)) / math.log1p(max_phen)),
            "in_degree": min(1.0, math.log1p(indeg.get(pid, 0)) / math.log1p(max_in)),
            "attention": min(1.0, math.log1p(max(u["karma_lw"], 0)) / math.log1p(500)) * (1.0 if u["in_af"] else 0.8),
            "negative": 1.0 if c["claim_type"] in ("negative", "null", "replication") else 0.4,
            "specified": 1.0 if c["uncertainty_reported"] != "none" else 0.3,
            "rigor": rigor,
        }
        wv = {"contested": 2.0, "phenomenon_n": 1.0, "in_degree": 1.5, "attention": 1.0,
              "negative": 1.0, "specified": 1.0, "rigor": 1.0}
        V = sum(value[k] * wv[k] for k in value) / sum(wv.values())

        fit = {"yes": 1.0, "probably": 0.8, "tight": 0.5, "unknown": 0.3, "no": 0.0}.get(r.get("fits_3090"), 0.0)
        data = (r.get("data") or {}).get("available")
        env = r.get("env") or {}
        rt = (r.get("est_runtime") or "").lower()
        rtc = "days" if ("day" in rt or "week" in rt) else "hours" if "hour" in rt else \
              "minutes" if ("minute" in rt or "second" in rt) else "unknown"
        feas = {
            "fits": fit,
            "api": 0.0 if r.get("needs_closed_api") else 1.0,
            "entrypoint": {"high": 1.0, "medium": 0.6, "low": 0.2}.get(r.get("entrypoint_confidence"), 0.0) if r.get("entrypoint") else 0.0,
            "artifact": 1.0 if r.get("headline_artifact") else 0.2,
            "data": {"in-repo": 1.0, "hf-hub": 1.0, "download-script": 0.8, "unknown": 0.4, "missing": 0.0}.get(data, 0.4),
            "runtime": {"minutes": 1.0, "hours": 0.7, "unknown": 0.4, "days": 0.2}[rtc],
            "hygiene": (0.4 * bool(env.get("has_requirements")) + 0.3 * bool(env.get("pinned_versions"))
                        + 0.3 * bool(env.get("stated_compute"))),
        }
        wf = {"fits": 2.0, "api": 3.0, "entrypoint": 1.5, "artifact": 1.0, "data": 1.5, "runtime": 1.0, "hygiene": 0.5}
        # hard gates: no API, must fit at least 'tight', must have an entrypoint
        F = sum(feas[k] * wf[k] for k in feas) / sum(wf.values())
        if feas["api"] == 0 or fit == 0 or feas["entrypoint"] == 0:
            F = min(F, 0.15)
        score = math.sqrt(max(V, 1e-6) * max(F, 1e-6))
        rows.append({"post_id": pid, "title": c["title"], "repo": c["repo"], "phenomenon": ph,
                     "claim_type": c["claim_type"], "karma": u["karma_lw"], "in_af": u["in_af"],
                     "value": round(V, 3), "feasibility": round(F, 3), "score": round(score, 3),
                     "value_factors": {k: round(v, 2) for k, v in value.items()},
                     "feas_factors": {k: round(v, 2) for k, v in feas.items()},
                     "in_degree": indeg.get(pid, 0), "phenomenon_n": phen_n.get(ph, 0),
                     "fits_3090": r.get("fits_3090"), "runtime_class": rtc,
                     "entrypoint": r.get("entrypoint"), "vram_gb": r.get("vram_estimate_gb"),
                     "needs_closed_api": bool(r.get("needs_closed_api")),
                     "target": c["target_value"], "metric": c["metric"]})
    rows.sort(key=lambda x: -x["score"])
    k = max(1, round(len(rows) * a.top_frac))
    top = rows[:k]
    total = sum(x["score"] for x in rows)
    share = sum(x["score"] for x in top) / total if total else 0
    runnable = [x for x in top if x["fits_3090"] in ("yes", "probably") and not x["needs_closed_api"]]
    out = {"_meta": {"n": len(rows), "top_frac": a.top_frac, "k": k,
                     "top_k_share_of_total_score": round(share, 3),
                     "runnable_in_top_k": len(runnable),
                     "weights_value": {"contested": 2.0, "phenomenon_n": 1.0, "in_degree": 1.5, "attention": 1.0,
                                       "negative": 1.0, "specified": 1.0, "rigor": 1.0},
                     "weights_feasibility": {"fits": 2.0, "api": 3.0, "entrypoint": 1.5, "artifact": 1.0,
                                             "data": 1.5, "runtime": 1.0, "hygiene": 0.5}},
           "top": top, "all": rows}
    json.dump(out, open(os.path.join(HERE, "pareto.json"), "w"), indent=1)

    print(f"{len(rows)} candidates scored; top {k} ({a.top_frac:.0%}) hold {share:.0%} of total score; "
          f"{len(runnable)} of the top {k} are runnable here (fit yes/probably, no closed API)\n")
    print(f"{'#':>3} {'score':>5} {'val':>5} {'feas':>5} {'fit':8} {'rt':7} {'C':1} {'in°':>3} {'type':8}  title / repo")
    for i, x in enumerate(rows[:k], 1):
        print(f"{i:>3} {x['score']:>5.2f} {x['value']:>5.2f} {x['feasibility']:>5.2f} {str(x['fits_3090']):8} "
              f"{x['runtime_class']:7} {'*' if x['value_factors']['contested'] else ' '} {x['in_degree']:>3} "
              f"{x['claim_type'][:8]:8}  {x['title'][:56]}\n{'':52}{x['repo']}  [{x['phenomenon'][:30]}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
