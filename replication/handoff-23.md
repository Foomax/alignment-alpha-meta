# handoff-23 — batch after R27–R32 (2026-08-27 23:30)

Rapid batch of rerun outcomes:
- **R31 (`peppinob-ol`) EXIT 0 — reproduces, pending fact-variant recompute.** `graph_subgraph_scores.py` over committed graph data gave output byte-identical to the author's committed CSVs (standard 5 datasets: S_Repl 0.689, S_Comp 0.890). The post's headline (0.5394 Repl / 0.8257 Comp) is the **fact variant** (`usa_states_fact_batch`): committed values 0.5425 / 0.8412 ≈ target within ~1.5 pts. **R31b** queued to recompute the fact variant myself before ledgering.
- **R32 (`g-w1`) EXIT 124** — trains 30 VAEs (range(20)+range(10)) × 100 epochs; 60-min box too short (catalogue said "minutes"). **R32c** 120-min box. Target 92.58% classification-from-encoding.
- **R27 (`ibm`)** missing `typeguard` (transformer-lens dep) under torch 2.3.1 → **R27c** adds typeguard/jaxtyping.
- **R28 (`jim-maar`)** `wandb`→`pkg_resources` gone in setuptools ≥81 → pinned **`setuptools<81` in `tree_prep.sh`** (global) + **R28c**.
- **R30 (`artmtt`)** wrong PyPI `sparsify` shadowed EleutherAI's `Sae` → **R30c** installs `sparsify @ git+EleutherAI/sparsify`.
- **R29 (`tenseisoham`)** ENOSPC again in uv cache (now 39 GB) → freed jordanmccann (11 GB) + cywinski (2.6 GB) src → 57 GB free → **R29c**.
- Currently running: R6b (cywinski script 5, the ~20% recovery figure). Queue tail: R12b, R17b, R18b, R19b, R21b, R5c, R4c, R13c, R14c, R25c, R27c, R28c, R30c, R31b, R32c, R29c.
- Ledger: 18 attempted / 12 reproduced (R31 will make 13 after R31b). Next: handoff-24, lessons-20.
