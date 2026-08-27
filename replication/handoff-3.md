# handoff-3 — first pass over the minute-class queue (nodes 2–14) and the rerun plan (2026-08-27 14:45)

## Pass-1 outcomes
| node | slug (short) | exit | class | action |
|---|---|---|---|---|
| 2 | ioi (fractalmachinist) | 0 | reproduced exactly | ledgered (handoff-2) |
| 3 | polymorphism-is-rotation (jordanmccann) | 2 | runner: descriptive entrypoint run literally | rerun R3: `python -m replicate run-fast` |
| 4 | error_pathology (dajale423) | 1 | env: needs author's `e2e_sae` fork (pyproject git dep) + submodule; auto-fix installed the wrong PyPI package | rerun R4 |
| 5 | sae-dataset-dependence (ckkissane) | 1 | env: numpy missing (plotly import) | rerun R5 |
| 6 | codi (cywinski) | 124 | runtime: 200 prompts × 12.8 s > 45-min box; model downloads flaky | rerun R6 with 95-min box (recorded as budget override) |
| 7 | data_leakage_detect (ai-forever) | 0 | ran defaults (AUC 0.912 on bookmia/bag_of_words), not the headline dataset/attack | rerun R7 with `--dataset vl_mia_img_Flickr_2k --attack bag_of_visual_words` (target 98.6 ± 5) |
| 8 | activation_plateau (mshinkle) | 1 | runner: `.sh` entrypoint with trailing description → run as python | rerun R8: `bash full_experiment.sh` with venv on PATH |
| 9 | top_down_vs_bottom_up (ak47na) | 1 | unclear-entrypoint: needs pre-generated completions + W&B artifact, stale cells | ledgered as `unclear-entrypoint`, no rerun |
| 10 | arithmetictransformer (james-sullivan) | 1 | env: `neel_plotly` | rerun R10 |
| 11 | probe-necessity (vaiyr) | 0 | reproduced exactly (aggregate of shipped per-cell results) | ledgered |
| 12 | llm-typos (idostik) | 1 | code-bug: `NameError: true` inside the author's notebook | ledger as `code-bug` once the cell is identified; no edit |
| 13 | deep-dive-l1h5 (mamiglia) | 1 | env: `sae_lens.toolkit` removed in sae-lens ≥ 6 → pin `<6` | rerun R13 |
| 14 | superposition-replication (uchicago-xlab) | 1 | runner: relative import → `python -m synth.run` | rerun R14 |

## Runner lessons (applied)
- Spec `entrypoint` is prose in ~1/3 of rows; the thin runner executes it literally. Pass 2 uses hand-written invocations (`tree_rerun.sh`).
- Auto-fix by module name is right ~60 % of the time; wrong when the package lives on the author's GitHub (R4) or when the API moved between major versions (R13).
- `nvidia-smi` compute-app check alone has gaps between phases; treat runner scripts as busy too.
- 45-min catalogue budgets are guesses; author-stated runtimes win (R6).

## Queue state
Pass 1 continues from node 15 (`noanabeshima/matryoshka-saes`) to 32. `tree_rerun.sh` is armed and starts when pass 1 ends and the GPU is free. Ledger rows for rerun candidates are written after pass 2.
