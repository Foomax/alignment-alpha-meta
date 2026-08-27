# handoff-11 — after R15 (2026-08-27 18:00)

- R15 (`noanabeshima/matryoshka-saes`) **reproduced** on the toy model (vanilla 9/20 absorbed latents vs Matryoshka 0/20; numbers extracted from the saved plotly HTML). LM half not in repo → UNRESOLVED.
- R12 failed one import short + placeholder `login("Your hf token")`; R12b queued (notebook copy with the login stubbed, full import pre-install). Gotcha fixed on the way: some notebooks store `cell.source` as a single string — always `splitlines(keepends=True)` before line-wise edits (my first two stub attempts silently changed nothing).
- Late queue: R17 next, then R18, R19, R20, R21, R23, R3b, R4b, R5b, R8b, R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b (22 remaining).
- Ledger: 14 rows — 10 reproduced, 1 not, 1 unclear-entrypoint, 1 api-key, 1 pending. Next numbering: handoff-12, lessons-8.
