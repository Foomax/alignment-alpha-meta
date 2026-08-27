# handoff-27 — POLICY SHIFT: stop after the tail, meta-report written (2026-08-28 04:50)

User decision: stop after the current tail, write the meta-report, then follow handoff-synth §B.

- **No more requeues.** The remaining tail (R12c running; then R14d, R18c, R25d, R28d, R29d, R30d, R4d, R5d) gets ONE final judgement each: reproduced if it ran, else ledger the honest reason (env/runtime/model-access/code-bug). Do not add R*e entries.
- **META-REPORT.md written** (provisional): 25 attempted, 17 located, 14 reproduced (82% of located; 11 exact + 3 recompute). Finding: engineering rot >> scientific fragility; 2 genuine scientific misses (AntiPaSTO config-drift, jordanmccann partial), both characterised. Regenerate numbers with `python3 make_report_table.py` when the tail is done.
- **Quality tiers** annotated on every `ledger.json` (`annotate_tiers.py`): exact 11, recompute 3, partial 1, not 1, n/a 9.
- Then, in order (handoff-synth §B3): (2) finalise META-REPORT numbers; (3) package the harness with lessons-synth as its manual; (4) selectively run 2–3 high-value HOURS-class rows from queue.md (contested negatives / safety-relevant, ≤16 GB) — not all 38.
- Ledger: 25 / 14 reproduced. Next: handoff-28, lessons-24 (only for material events).
