# handoff-28 — H36c (tarcle imposter-FVs) reproduced; H57b running (2026-08-28 06:40)

Read `handoff-synth.md` first (operating rules + §B direction). This is an incremental note.

## What just happened
- **H36c (star2vec/tarcle) = REPRODUCED, tier recompute.** First of the two hours-class negative-claim
  scale-tests. Ran the numpy-only Stage-2 chain (`-m tarcle.{stage2,floors,measure_corr,margin_split,
  offset_audit,support_gate}`) over the committed `results/fv` artifacts; GPU stage-1 `extract` not needed.
  - Two target anchors EXACT: `margin_split` primary(12)=**+0.352** [t +0.35]; Sep-Dec partB=**-1.000** [t -1.000].
  - Full "imposter" thesis holds: low-diversity FVs collapse out-of-pool (monotone +margin -> -1.0, "R-collapse")
    while `support_gate` says GO / "claim A survives strong" — i.e. they behaviorally ace the task. That IS the claim.
  - `stage2`/`floors` recompute matches committed deterministic values (PR 3.116, conc ~0.75, additivity ~1.15);
    they exit nonzero ONLY on the author's append-only write-guard (unseeded perm-null differs run-to-run). Benign.
- **H57b (filyp/sneaky-mamba) RUNNING** (pid ~835140, 240-min cap). Builds mamba-ssm `--no-build-isolation`
  + `CUDA_HOME=/usr`, then runs the author's 3 `architecture` arms (mamba/switcher/transformer) via `run_h57.sh`,
  each timeout 30m. Judge when it lands. Note: arm-toggle is a documented deviation (running author's own conditions).

## Ledger now
`python3 ledger.py`: **35 attempted · 34 installs · 21 runs · 20 located · 15 reproduced** (75% of located; 12 exact + 3 recompute).
Taxonomy: none 19, env 6, runtime 3, unclear-entrypoint 2, vram 2, api-key 1, data 1, model-access 1.

## Next
1. Judge H57b at exit; write handoff-29/lessons-24 + human-oversight §28.
2. **Update META-REPORT.md** to fold in the two hours-class rows (tarcle ✅ recompute; sneaky-mamba TBD) and
   refresh the headline counts + the "89% of located" number. Do this once BOTH hours-class rows are in.
3. Then STOP (per the user's "stop after the tail + follow suggested steps"): harness is packaged (HARNESS.md);
   the scale-test sample is the last planned work. Do not open new requeue rounds.

## Coordination note
Another instance is now steering direction via `prompts2/` (see `nav.md` line 28: a wild-pass menu +
a research-director prompt with hour-stamped `handoff-&-lessons-HH.md` logs). Its cadence is separate from this
numbered handoff-N/lessons-N series — no collision. Don't touch `prompts2/`; it's theirs.
