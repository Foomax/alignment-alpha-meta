# handoff-16 — after R21 (2026-08-27 19:55)

- R21 (`patrickod32/seq2feature`): the notebook ran 37 min through the evaluation cells and died at the final "summary sentence" cell on a late `google.colab` import; nbconvert wrote no output notebook, so the computed metrics were lost. **R21b queued**: `google.colab` stubbed via `sys.modules` in a prepended cell (all import lines commented), run with `--allow-errors`, 60-min box.
- Generic change: every pending nbconvert entry in `tree_late.txt` now runs with `--allow-errors` (partial outputs are written even if a late cell fails). Judge such notebooks from `executed.ipynb` cell outputs, and check the error cell before trusting the numbers.
- Late queue after R21: R23 running; then R3b, R4b, R5b, R8b, R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b, R19b, R21b. Disk 81 GB free.
- Ledger unchanged: 14 attempted / 10 reproduced. Next: handoff-17, lessons-13.
