# handoff-13 — after R18 (2026-08-27 19:00)

- R18 (`sunmoonron`, OLMo-1B super-weight): steps 01 and 03 ran (33 min; `base/broken/patch.safetensors` now exist in `src/`), step 07 needs `patched_merged.safetensors`, written by `04_test_patch.py`. **R18b queued: `04 → 07`** (60-min box). Not ledgered yet.
- R17 → R17b (`sae-lens<4`) already queued. Late queue: R19 running next; then R20, R21, R23, R3b, R4b, R5b, R8b, R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b.
- Disk 81 GB free after venv deletion (the disk-bounded queue works). Ledger unchanged: 13 attempted / 10 reproduced.
- `handoff-synth.md` + `lessons-synth.md` exist and are the entry point for a fresh instance; this series continues for state deltas only. Next: handoff-14, lessons-10.
