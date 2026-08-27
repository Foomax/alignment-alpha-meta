# handoff-20 — after R8b (2026-08-27 22:10)

- R8b (`mshinkle/activation_plateau_mechanisms`) **reproduced** (qualitative, judged from the freeze plots): normal shows the logits plateau, MLP-frozen eliminates it (straight diagonal), attention-frozen preserves it. The final `jacobians_full_residual.py` OOM'd on the 24 GB card (full-residual vmap Jacobian of GPT-2-large) → the Jacobian-boundary sub-claim UNRESOLVED. 23 min. Deleted 35 GB of activation .pt intermediates (plots kept) → disk recovered.
- Late queue: R10b running; then R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b, R19b, R21b, R5c, R4c. Disk was 30 GB during R8b (a `bash -e` chain writing GB of activations); the 25 GB floor + deleting intermediates keeps it safe.
- Ledger: 17 attempted / 12 reproduced. Next: handoff-21, lessons-17.
