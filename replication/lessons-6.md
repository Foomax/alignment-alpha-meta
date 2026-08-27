# lessons-6 — from R6 (2026-08-27 17:50)

New:
1. **Set the time-box from the author's own per-item timing, not the catalogue tag.** The catalogue said "minutes"/45; the script's tqdm showed 12.8 s/prompt × 200 = 43 min of generation plus model load. Reading the first minute of a run's progress bar and multiplying is a 10-second check that would have saved a 45-minute dead run.
2. **Map ordinal language to the script's indexing before judging.** "Third and fifth of six latent vectors" = 0-indexed positions 2 and 4 in the output table; judging the table without that mapping would read as "positions 3 and 5 don't matter".
3. **A compound target can be split across sibling scripts.** The spec's `headline_artifact` listed two scripts; the `entrypoint` names one. Judge what the entrypoint measures, mark the rest UNRESOLVED, and queue the sibling — don't fold an unmeasured number into the verdict.
4. **Transient HF download failures self-heal with retries inside the box** — several `HTTPSConnectionPool` errors, then success; no action needed beyond a generous box (contrast with the xet *stall* in lessons-1 A1, which never recovers).

Confirmed: lessons-1 A5 (extraction-only/short boxes), lessons-5 #1.
