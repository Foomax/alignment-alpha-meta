#!/usr/bin/env python3
"""Add a quality_tier field to each experiments/*/ledger.json.
Tiers (lessons-synth Part 4): exact (regenerated the core computation from source and matched),
recompute (re-ran a script over the author's COMMITTED artefacts/models without regenerating them),
partial (some components match, others don't / direction-only), not (located and genuinely off),
n/a (never located: env/runtime/unclear-entrypoint/vram/api-key/model-access)."""
import json, glob, os
TIER = {
  "jaehoonlee0829/cross-model-alignment-geometry": "exact",
  "lovkush-a/arena-sandbagging-mi": "exact",
  "fractalmachinist/ioi": "exact",
  "ameya-bit/quotesbyniche": "exact",
  "coolvision/interp": "exact",
  "mild-rgb/qwen-2.5-1.5b-echo_repeat-investigation": "exact",
  "noanabeshima/matryoshka-saes": "exact",
  "mshinkle/activation_plateau_mechanisms": "exact",
  "cywinski/codi": "exact",             # headline exact; ~20% recovery addendum is partial
  "phusroyal/phu-bluedot_1st_puzzle": "exact",
  "ai-forever/data_leakage_detect": "exact",
  "vaiyr/probe-necessity": "recompute", # aggregates committed per-cell results
  "peppinob-ol/attribution-graph-probing": "recompute",  # recompute over committed graphs (byte-identical)
  "patrickod32/seq2feature": "recompute",  # evaluates the committed 5MB probe on committed data
  "jeffreywilliamportfolio/jlens-basin-swaps": "n/a",
  "wassname/antipasto": "not",          # config drift; 270M reproduces, 1B does not
  "jordanmccann/polymorphism-is-rotation": "partial",  # toy+Haar exact, Pythia-EV off
}
n=0
for f in glob.glob("experiments/*/ledger.json"):
    d=json.load(open(f)); repo=d.get("repo")
    if repo in TIER: d["quality_tier"]=TIER[repo]
    elif d.get("claim_reproduced") is None: d["quality_tier"]="n/a"
    else: d["quality_tier"]="unclassified"
    json.dump(d, open(f,"w"), indent=1); n+=1
print(f"annotated {n} ledgers")
# summary
from collections import Counter
c=Counter(json.load(open(f)).get("quality_tier") for f in glob.glob("experiments/*/ledger.json"))
print("tiers:", dict(c))
