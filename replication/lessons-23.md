# lessons-23 — append-only write-guards, recompute paths, unseeded nulls (2026-08-28, from H36c)

- **A nonzero exit is not always a failure — read WHY.** tarcle's `stage2`/`floors` computed everything correctly
  then exited nonzero on an author append-only guard: *"refusing to overwrite results/…json with differing content;
  results are never overwritten."* If you ledger that as a failure you throw away a clean recompute. Symptom: nonzero
  rc but a full table of numbers printed just above. Fix: read the last lines before the `|| echo FAILED`; if the
  numbers are there, the run succeeded — the write was refused by design.
- **Why the guard fired: unseeded permutation nulls.** The recompute matched every DETERMINISTIC quantity
  (participation_ratio 3.116 exact) but the permutation-test z differed (7.76 vs 8.49) because `n_perm=200` with no
  fixed seed → different null each run → "differing content" → overwrite refused. Both z>7 / percentile 100, so the
  science is identical. Lesson: expect artifact-overwrite guards to trip on any stochastic field; judge the deterministic ones.
- **Recompute path when stage-1 needs GPU + a config.** `extract.py` (Stage 1) wanted a positional
  `experiments/<run>.json` and used relative imports (run as `-m pkg.module`, never `python pkg/mod.py`). The README's
  real reproduction is Stage-2 numpy over committed `results/` — `stage2`'s `root` arg DEFAULTS to `results/fv`, so the
  whole chain runs bare. When a repo commits its intermediate artifacts, prefer the recompute path; tier it `recompute`, not `exact`.
- **Chain with `|| echo FAILED $m`, not `|| break`.** Running the six stages with a non-fatal marker per stage gave
  maximal signal in ONE node (4 of 6 wrote, 2 hit the guard) instead of stopping at the first nonzero. `break` would
  have hidden margin_split/support_gate — the exact stages carrying the headline anchors.
