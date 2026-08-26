#!/usr/bin/env python3
"""
Write ledger.json for this experiment from run.log + whatever the runner fills in by hand.

Usage: python3 report.py --observed "<value or null>" --reason none|env|data|model-access|vram|runtime|code-bug|api-key|unclear-entrypoint [--notes "..."] [--fix "..."]...

Mechanical fields (installs, runs, wallclock, peak VRAM) are parsed from run.log / vram.log.
Judgement fields (observed value, reproduced?, blocking reason) come from the agent, because
deciding whether 0.79 reproduces "~0.8 AUROC" is not something a regex should do.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def within(observed, claimed, tol):
    """tol like 'abs:0.05', 'rel:0.1', 'direction', 'manual'. Returns True/False/None."""
    if tol == "manual" or observed is None or claimed is None:
        return None
    try:
        o, c = float(observed), float(claimed)
    except (TypeError, ValueError):
        return None
    kind, _, v = tol.partition(":")
    if kind == "abs":
        return abs(o - c) <= float(v)
    if kind == "rel":
        return abs(o - c) <= float(v) * abs(c)
    if kind == "direction":
        return (o > 0) == (c > 0)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--observed", default=None)
    ap.add_argument("--reason", required=True)
    ap.add_argument("--notes", default="")
    ap.add_argument("--fix", action="append", default=[])
    ap.add_argument("--seeds", type=int, default=None)
    ap.add_argument("--reproduced", choices=["true", "false"], default=None,
                    help="override the tolerance check when the metric is not scalar")
    a = ap.parse_args()
    spec = json.load(open(os.path.join(HERE, "spec.json")))
    log = open(os.path.join(HERE, "run.log")).read() if os.path.exists(os.path.join(HERE, "run.log")) else ""
    installs = bool(re.search(r"INSTALL-EXIT 0", log)) or ("INSTALL-EXIT" not in log and "RUN-EXIT" in log)
    m = re.search(r"RUN-EXIT (\d+) after (\d+) min", log)
    runs = bool(m and m.group(1) == "0")
    minutes = float(m.group(2)) if m else 0.0
    vram = None
    vp = os.path.join(HERE, "vram.log")
    if os.path.exists(vp):
        vals = [float(x) for x in re.findall(r"\d+", open(vp).read())]
        vram = round(max(vals) / 1024, 1) if vals else None
    observed = None if a.observed in (None, "", "null") else a.observed
    located = observed is not None
    rep = within(observed, spec.get("target_numeric"), spec.get("tolerance", "manual"))
    if a.reproduced is not None:
        rep = a.reproduced == "true"
    try:
        gpu = subprocess.check_output(["nvidia-smi", "--query-gpu=name,driver_version",
                                       "--format=csv,noheader"], text=True).strip()
    except Exception:
        gpu = "unknown"
    entry = {
        "post_id": spec["post_id"], "repo": spec["repo"], "head_sha": spec["head_sha"],
        "attempted_at": dt.date.today().isoformat(), "machine": gpu + " / 24GB",
        "installs": installs, "runs": runs, "claim_located": located,
        "claim_reproduced": rep if located else None,
        "claimed_value": spec.get("target_value"), "observed_value": observed,
        "delta": (round(float(observed) - float(spec["target_numeric"]), 4)
                  if located and spec.get("target_numeric") is not None and
                  re.fullmatch(r"-?\d+(\.\d+)?", str(observed)) else None),
        "tolerance_used": spec.get("tolerance"), "blocking_reason": a.reason,
        "env_fixes": a.fix, "wallclock_minutes": minutes, "peak_vram_gb": vram,
        "seeds_run": a.seeds, "notes": a.notes,
        "artifact_paths": [p for p in ["run.log", "vram.log", "executed.ipynb"]
                           if os.path.exists(os.path.join(HERE, p))],
    }
    json.dump(entry, open(os.path.join(HERE, "ledger.json"), "w"), indent=1)
    print(json.dumps(entry, indent=1))


if __name__ == "__main__":
    sys.exit(main())
