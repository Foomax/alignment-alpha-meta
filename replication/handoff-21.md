# handoff-21 — after R10b/R13b/R14b (2026-08-27 22:15)

- R10b (`james-sullivan/ArithmeticTransformer`) ledgered **`runtime`**: entrypoint `EstimateLLC.ipynb` needs grokking checkpoints not committed; regenerating = `GrokkingAdditionMultiplication.ipynb`, ~6000 epochs × 8 ratios, multi-hour. Author's result graphs committed and consistent with the claim; not regenerated.
- R13b failed (`sae_lens.toolkit`: prep's import scan reinstalled sae-lens ≥6 over the needed <6) → **R13c** pins `sae-lens<6` after prep. R14b failed with a stale/incomplete venv → **R14c** after deleting the venv. Both requeued; R13b/R14b/R10b removed from `tree_late.txt`.
- **Lesson applied**: `tree_prep.sh`'s import-list install can override a version pin a rerun needs; when a rerun requires `pkg<N`, pin it in the rerun command *after* prep (prep runs first).
- Late queue: R25 running; then R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b, R19b, R21b, R5c, R4c, R13c, R14c (16 remaining). Disk 63 GB.
- Ledger: 18 attempted / 12 reproduced (taxonomy: none 14, api-key 1, unclear-entrypoint 1, vram 1, runtime 1). Next: handoff-22, lessons-18.
