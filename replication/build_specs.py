#!/usr/bin/env python3
"""
build_specs.py -- merge candidates.json + inspect/result_*.json into one folder per experiment.

For every candidate the inspection pass judged feasible (fits_3090 in {yes, probably, tight},
no closed API needed, an entrypoint identified), writes:

  experiments/<slug>/spec.json   the machine-readable contract the runner reads
  experiments/<slug>/PROMPT.md   the Claude Opus prompt for this experiment (prompts.md P9)
  experiments/<slug>/run.sh, report.py   copied from template/

and queue.md, the ranked human-readable run order. Re-runnable; never overwrites an existing
ledger.json or run.log.

Usage: python3 replication/build_specs.py [--include-tight] [--limit N]
"""
import argparse, collections, glob, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NUM = re.compile(r"-?\d+(?:\.\d+)?")


def slugify(title, repo):
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48]
    owner = repo.split("/")[0].lower()[:16]
    return f"{base}--{owner}"


def first_number(s):
    m = NUM.search(str(s or ""))
    return float(m.group(0)) if m else None


def tolerance_for(cand):
    """A default tolerance the runner can override. Stated so the choice is visible.

    Decided from the FIRST number in the headline (the one target_numeric holds), not from
    anything that appears later in a long compound value string.
    """
    metric = (cand.get("metric") or "").lower()
    val = str(cand.get("target_value") or "")
    unc = cand.get("uncertainty_reported", "none")
    nums = list(NUM.finditer(val))
    if not nums:
        return "manual", "headline is not a single scalar; judge by hand"
    if len(nums) >= 4:
        return "manual", f"headline is a compound of {len(nums)} numbers; compare the components by hand"
    m = nums[0]
    first_is_pct = val[m.end():m.end() + 2].strip().startswith("%") or "pp" == val[m.end():m.end() + 2]
    spread = "; post reported spread" if unc != "none" else "; post reported no spread, tolerance is a guess"
    if first_is_pct:
        return "abs:5", "percentage metric: 5 points" + spread
    v = float(m.group(0))
    if 0 <= v <= 1 and any(k in metric for k in ["auroc", "auc", "accuracy", "cka", "f1", "correlation", "r^2", "r2", "cosine", "fraction", "rate", "score"]):
        return "abs:0.05", "unit-interval metric: 0.05 absolute" + spread
    return "rel:0.15", "other scalar metric: 15% relative" + spread


def runtime_class(s):
    """Collapse the inspectors' free-text runtime estimates to minutes|hours|days|unknown.
    The longest unit mentioned wins: 'minutes to hours' is an hours-class budget."""
    s = (s or "").lower()
    if "day" in s or "week" in s:
        return "days"
    if "hour" in s:
        return "hours"
    if "minute" in s or "second" in s:
        return "minutes"
    return "unknown"


def budget_for(insp, cand):
    rt = runtime_class(insp.get("est_runtime"))
    work = cand.get("workload")
    return {"minutes": 45, "hours": 240, "days": 480}.get(
        rt, 180 if work in ("lm-ft", "aux-train") else 90)


PROMPT = """# Replicate: {title}

Source post: `{post_id}` ({date}, LW karma {karma}). Repo: `{repo}` @ `{sha}`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> {claim}

Supporting quote from the post: "{quote}"

**Headline metric:** {metric}
**Claimed value:** {target}
**Direction of the claim:** {direction}
**Uncertainty the post reported:** {unc}
**Tolerance for "reproduced":** `{tol}` — {tol_why}

## What the inspection pass found (read-only, {insp_date})

- Entrypoint: `{entrypoint}` (confidence: {entry_conf})
- Produces: {artifact}
- Models: {models}
- Estimated VRAM: {vram} GB — {vram_basis}
- Data: {data_needed}; availability: {data_avail}
- Estimated runtime: {runtime} ({runtime_basis})
- Stated compute in the repo: {stated_compute}
- Known blockers: {blockers}
- Inspector's notes: {notes}

## Budget

**{budget} minutes** of wall-clock for the run itself (environment setup not counted, but cap that
at 30 minutes). When the budget is exceeded, stop and record `blocking_reason: runtime`.

## Procedure

1. `cd` into this folder. Read `spec.json`. Run `./run.sh`. It clones at the pinned sha, builds a
   venv from the repo's own requirements, runs the entrypoint under `timeout`, and logs to
   `run.log` + `vram.log`.
2. If install fails: fix **only** the environment (a version pin, a missing system package, a
   CUDA-index torch wheel). Record every fix. Do not touch experiment code. If you cannot fix it
   in 30 minutes, `report.py --reason env`.
3. If the entrypoint needs an argument the inspection did not capture, read the README and the
   script's argparse; prefer the configuration the post describes. Record it as a fix.
4. If the run needs a gated model, the HF token is already on this machine; if it is not,
   `--reason model-access`.
5. When it finishes, find the headline number in the output. Compare to the claimed value
   under the tolerance. Then:
   `python3 report.py --observed "<value>" --reason none [--fix "..."]... [--notes "..."]`
   — or with the right `--reason` if it failed. If the metric is not a scalar, pass
   `--reproduced true|false` and say why in `--notes`.
6. Append 3–6 lines to `run.log` under `== VERDICT`: what you observed, what you compared it to,
   what you changed, what you would need to go further.

## Do not

- Do not run more than **{seeds} seed(s)** unless the run is under 10 minutes; if it is, run 3
  and report the spread — that is more valuable than the point estimate.
- Do not substitute a different model, dataset, or judge and call it a replication. Note it as a
  follow-up in `--notes` instead.
- Do not read the post's conclusion into ambiguous output. If you cannot tell which number is
  the headline, `--reason unclear-entrypoint` and say what you saw.
- Do not push, do not open issues, do not contact the authors.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-tight", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    cands = {c["post_id"]: c for c in json.load(open(os.path.join(HERE, "candidates.json")))["candidates"]}
    insp = {}
    for p in sorted(glob.glob(os.path.join(HERE, "inspect", "result_*.json"))):
        try:
            for r in json.load(open(p)):
                insp[r["post_id"]] = r
        except Exception as e:
            print(f"skipping {p}: {e}", file=sys.stderr)
    ok_fit = {"yes", "probably"} | ({"tight"} if a.include_tight else set())
    rows, skipped = [], collections.Counter()
    for pid, c in cands.items():
        r = insp.get(pid)
        if not r:
            skipped["not inspected"] += 1; continue
        if r.get("status") != "ok":
            skipped[f"status={r.get('status')}"] += 1; continue
        if r.get("needs_closed_api"):
            skipped["needs closed API"] += 1; continue
        if r.get("fits_3090") not in ok_fit:
            skipped[f"fit={r.get('fits_3090')}"] += 1; continue
        if not r.get("entrypoint"):
            skipped["no entrypoint"] += 1; continue
        if (r.get("data") or {}).get("available") == "missing":
            skipped["data missing"] += 1; continue
        rows.append((c, r))
    # rank: contested & cheap first; fit certainty; then the selector's score
    fit_rank = {"yes": 0, "probably": 1, "tight": 2}
    rt_rank = {"minutes": 0, "hours": 1, "unknown": 2, "days": 3}
    rows.sort(key=lambda cr: (fit_rank[cr[1]["fits_3090"]], rt_rank[runtime_class(cr[1].get("est_runtime"))],
                              -cr[0]["score"]))
    if a.limit:
        rows = rows[:a.limit]

    U = json.load(open(os.path.join(ROOT, "union.json")))["records"]
    ov_path = os.path.join(HERE, "budget_overrides.json")
    overrides = {k: v for k, v in json.load(open(ov_path)).items() if not k.startswith("_")} if os.path.exists(ov_path) else {}
    made = 0
    qlines = ["# Replication queue — run order\n",
              f"{len(rows)} experiments passed selection + inspection. Ranked: certain fit → short "
              "runtime → replication value (contested phenomenon, cheap model, negative result, "
              "well-specified target). Each row is a folder under `experiments/`.\n",
              "| # | slug | tier | fit | runtime | VRAM | phenomenon | claim | target |", "|---|---|---|---|---|---|---|---|---|"]
    for i, (c, r) in enumerate(rows, 1):
        slug = slugify(c["title"], c["repo"])
        d = os.path.join(HERE, "experiments", slug)
        os.makedirs(d, exist_ok=True)
        tol, tol_why = tolerance_for(c)
        budget = budget_for(r, c)
        if slug in overrides:
            budget = overrides[slug]["budget_minutes"]
        spec = {
            "slug": slug, "post_id": c["post_id"], "title": c["title"], "date": c["date"],
            "repo": c["repo"], "head_sha": r.get("head_sha") or c.get("head_sha"),
            "entrypoint": r["entrypoint"], "entrypoint_confidence": r.get("entrypoint_confidence"),
            "python_version": (r.get("env") or {}).get("python_version") or "3.11",
            "key_deps": (r.get("env") or {}).get("key_deps"),
            "models": r.get("models_needed") or c["models"],
            "phenomenon": c["phenomenon"], "contested": c["contested"], "claim_type": c["claim_type"],
            "primary_claim": c["primary_claim"], "quote": c["quote"],
            "metric": c["metric"], "target_value": c["target_value"],
            "target_numeric": first_number(c["target_value"]), "direction": c["direction"],
            "uncertainty_reported": c["uncertainty_reported"],
            "tolerance": tol, "tolerance_rationale": tol_why,
            "vram_estimate_gb": r.get("vram_estimate_gb"), "fits_3090": r["fits_3090"],
            "est_runtime": r.get("est_runtime"), "est_runtime_class": runtime_class(r.get("est_runtime")),
            "budget_minutes": budget,
            "budget_override_reason": overrides.get(slug, {}).get("reason"),
            "seeds_to_run": 1, "data": r.get("data"), "blockers": r.get("blockers"),
            "inspector_notes": r.get("notes"), "headline_artifact": r.get("headline_artifact"),
            "selector_tier": c["tier"], "selector_score": c["score"],
        }
        json.dump(spec, open(os.path.join(d, "spec.json"), "w"), indent=1)
        with open(os.path.join(d, "PROMPT.md"), "w") as fh:
            fh.write(PROMPT.format(
                title=c["title"], post_id=c["post_id"], date=c["date"], karma=c["karma_lw"],
                repo=c["repo"], sha=spec["head_sha"], claim=c["primary_claim"],
                quote=(c["quote"] or "")[:240], metric=c["metric"], target=c["target_value"],
                direction=c["direction"], unc=c["uncertainty_reported"], tol=tol, tol_why=tol_why,
                insp_date="2026-08-26", entrypoint=r["entrypoint"], entry_conf=r.get("entrypoint_confidence"),
                artifact=r.get("headline_artifact") or "not identified",
                models=", ".join(f"{m.get('hf_id') or '?'} ({m.get('params_b')}B{', gated' if m.get('gated') else ''})"
                                 for m in (r.get("models_needed") or [])) or ", ".join(c["models"]),
                vram=r.get("vram_estimate_gb") if r.get("vram_estimate_gb") is not None else "?",
                vram_basis=r.get("vram_basis") or "no basis given",
                data_needed=", ".join((r.get("data") or {}).get("needed") or []) or "none listed",
                data_avail=(r.get("data") or {}).get("available"), runtime=r.get("est_runtime"),
                runtime_basis=r.get("est_runtime_basis") or "none given",
                stated_compute=(r.get("env") or {}).get("stated_compute") or "none",
                blockers="; ".join(r.get("blockers") or []) or "none recorded",
                notes=r.get("notes") or "", budget=budget, seeds=spec["seeds_to_run"]))
        for f in ["run.sh", "report.py"]:
            dst = os.path.join(d, f)
            if not os.path.exists(dst):
                shutil.copy(os.path.join(HERE, "template", f), dst)
                os.chmod(dst, 0o755)
        made += 1
        qlines.append(f"| {i} | `{slug}` | {c['tier']} | {r['fits_3090']} | {runtime_class(r.get('est_runtime'))} | "
                      f"{r.get('vram_estimate_gb') or '?'} | {c['phenomenon'][:28]}{' ⚔' if c['contested'] else ''} | "
                      f"{c['claim_type']} | {str(c['target_value'])[:40]} |")
    qlines.append(f"\n## Not queued\n")
    for k, v in skipped.most_common():
        qlines.append(f"- {v} — {k}")
    open(os.path.join(HERE, "queue.md"), "w").write("\n".join(qlines) + "\n")
    print(f"built {made} experiment folders; skipped {dict(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
