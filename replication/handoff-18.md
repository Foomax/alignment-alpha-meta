# handoff-18 — after R3b (2026-08-27 21:25)

- R3b (`jordanmccann/polymorphism-is-rotation`) ledgered **not reproduced (partial)**: toy-model post-rotation SAE EV 0.977–0.991 ✓ (target 0.976–0.990); Haar-rotation statistics ✓ (repo `verify` 6/6: KS 0.00272, p 1.000, ‖R−P‖ 29.60, ‖R−I‖ 31.99); Pythia-70m post-rotation alignment EV **0.20–0.48** ✗ (target 0.85–0.99). Cause unresolved; `run-full` (14 h) is the only untried lever.
- Runtime: 58 min run-fast + rebuild + 5 min verify. Venv deleted by the queue; rebuilt once for verify (`tree_prep.sh` works standalone).
- Late queue: R4b running; then R5b, R8b, R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b, R19b, R21b. Disk ≈ 62 GB free.
- Ledger: 16 attempted / 11 reproduced. Next: handoff-19, lessons-15.
