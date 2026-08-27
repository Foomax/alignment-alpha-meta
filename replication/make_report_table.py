#!/usr/bin/env python3
"""Regenerate the results numbers + row table for META-REPORT.md from experiments/*/ledger.json.
Prints the summary block and the markdown table; run at the end to refresh the report."""
import json, glob
from collections import Counter
rows=[json.load(open(f)) for f in glob.glob("experiments/*/ledger.json")]
n=len(rows)
located=[r for r in rows if r.get("claim_located")]
repro=[r for r in located if r.get("claim_reproduced")]
tiers=Counter(r.get("quality_tier") for r in repro)
tax=Counter(r.get("blocking_reason") for r in rows)
print(f"N={n} | located={len(located)} | reproduced={len(repro)} ({len(repro)/max(len(located),1):.0%} of located, {len(repro)/n:.0%} of attempted)")
print(f"reproduced tiers: {dict(tiers)}")
print(f"failure taxonomy (all): {dict(tax)}")
notrep=[r for r in located if not r.get('claim_reproduced')]
print(f"located-but-not: {len(notrep)} ({', '.join(r['quality_tier'] for r in notrep)})")
print(f"never-located: {n-len(located)} ({', '.join(sorted(r['blocking_reason'] for r in rows if not r.get('claim_located')))})")
