#!/usr/bin/env python3
"""Tabulate what the repo-inspection pass found, across every inspected candidate.

This is an object-level result about the corpus in its own right: of the posts that *look*
replicable from their claims (open models, code linked, a number to hit), how many actually
ship the experiment that produced the number? Writes inspection_summary.json."""
import collections, glob, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
R = []
for p in sorted(glob.glob(os.path.join(HERE, "inspect", "result_*.json"))):
    R += json.load(open(p))
C = {c["post_id"]: c for c in json.load(open(os.path.join(HERE, "candidates.json")))["candidates"]}
n = len(R)
S = {}
S["inspected"] = n
S["fits"] = dict(collections.Counter(r.get("fits_3090") for r in R))
S["needs_closed_api"] = sum(1 for r in R if r.get("needs_closed_api"))
S["no_entrypoint"] = sum(1 for r in R if not r.get("entrypoint"))
S["no_headline_artifact"] = sum(1 for r in R if not r.get("headline_artifact"))
S["data_missing"] = sum(1 for r in R if (r.get("data") or {}).get("available") == "missing")
S["language"] = dict(collections.Counter(r.get("language") for r in R))
S["has_requirements"] = sum(1 for r in R if (r.get("env") or {}).get("has_requirements"))
S["pinned_versions"] = sum(1 for r in R if (r.get("env") or {}).get("pinned_versions"))
S["stated_compute"] = sum(1 for r in R if (r.get("env") or {}).get("stated_compute"))
# what the closed API is for
api_for = collections.Counter()
for r in R:
    if r.get("needs_closed_api"):
        t = (r.get("needs_closed_api_for") or "").lower()
        api_for["judge/grader" if re.search(r"judg|grad|scor|rubric|label", t) else
                "data generation" if re.search(r"generat|synth|caption", t) else
                "model under test" if re.search(r"under test|target model|the model", t) else "other/unspecified"] += 1
S["closed_api_used_for"] = dict(api_for)
# blocker taxonomy by keyword over the free-text blockers
tax = collections.Counter()
for r in R:
    text = " ".join(r.get("blockers") or []).lower() + " " + (r.get("notes") or "").lower()
    hit = False
    for key, rx in [("fp32-default-load", r"fp32|float32|no dtype|torch_dtype"),
                    ("multi-gpu-assumed", r"cuda:1|multi-gpu|2x|two gpus|tp=2|ddp"),
                    ("experiment-not-in-repo", r"not in (the )?repo|doesn't contain|does not contain|no code for|not implemented|missing script|isn't there|placeholder|0-byte|empty file"),
                    ("hardcoded-result", r"hardcod|literal|precomputed|already contains the exact"),
                    ("data-private", r"google drive|gitignore|not checked in|withheld|password|private"),
                    ("pretraining-from-scratch", r"from scratch|pretrain"),
                    ("stated->24gb", r"80 ?gb|a100|h100|h200|55 ?gb|52 ?gb|48 ?gb|64 ?gb")]:
        if re.search(rx, text):
            tax[key] += 1; hit = True
    if not hit and (r.get("blockers")):
        tax["other"] += 1
S["blocker_taxonomy"] = dict(tax.most_common())
S["fit_by_selector_tier"] = {}
for t in ["T1", "T2", "T?"]:
    sub = [r for r in R if C.get(r["post_id"], {}).get("tier") == t]
    S["fit_by_selector_tier"][t] = {"n": len(sub), **dict(collections.Counter(r.get("fits_3090") for r in sub))}
json.dump(S, open(os.path.join(HERE, "inspection_summary.json"), "w"), indent=1)
print(json.dumps(S, indent=1))
