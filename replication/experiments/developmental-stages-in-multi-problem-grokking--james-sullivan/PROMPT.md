# Replicate: Developmental Stages in Multi-Problem Grokking

Source post: `ronAKFdTDE7tiZk2c` (2024-09-29, LW karma 5). Repo: `james-sullivan/arithmetictransformer` @ `4a10f5e13b56222a028bb0c2bc1e96af452203f0`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Varying the ratio of addition to multiplication problems in training data shifts the timing of grokking (local learning coefficient decline) toward whichever operation dominates, but does not produce separate, distinct developmental stages in the LLC curve for each operation, contrary to the author's hypothesis.

Supporting quote from the post: "the LLC curves did not reveal separate, distinct stages for learning addition versus multiplication, contrary to the initial hypothesis."

**Headline metric:** local learning coefficient (LLC) curve shape / stage separation across addition:multiplication training ratios
**Claimed value:** no distinct additional developmental stages observed; a single LLC decline across all ratios tested (30-70% addition), though the decline's onset timing shifted earlier for more uneven ratios
**Direction of the claim:** 0
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/EstimateLLC.ipynb` (confidence: high)
- Produces: graphs/llc_during_training_all.png and per-ratio loss_llc_training_*.png (LLC-vs-checkpoint curves across addition fractions)
- Models: ? (0.0002B)
- Estimated VRAM: 1 GB — 1-layer transformer, d_model=128, d_head=32, d_mlp=512, 4 heads (~0.2M params); full-batch training on ~17k modular-arithmetic examples plus SGLD LLC sampling (3 chains x 150 draws) via devinterp — negligible VRAM even in fp32.
- Data: modular addition/multiplication dataset (generated in-notebook via create_dataset(), max_nums=130, mod_value=113); availability: in-repo
- Estimated runtime: minutes (6000-epoch full-batch training of a ~0.2M-param 1-layer transformer, repeated across ~9 addition:multiplication ratios (0.3-0.7), plus SGLD LLC estimation (3 chains, 150 draws, 50 burn-in) per saved checkpoint — each stage is CPU-feasible in minutes, near-instant on a 3090.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: The two notebooks (train, then estimate LLC) are the full pipeline and are self-contained; pretrained checkpoints are optionally hosted on Google Drive but are not required since training from scratch is trivial and fast.

## Budget

**45 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
at 30 minutes). When the budget is exceeded, stop and record `blocking_reason: runtime`.

## Procedure

1. `cd` into this folder. Read `spec.json`. Run `./run.sh`. It clones at the pinned sha, builds a
   venv from the repo's own requirements, runs the entrypoint under `timeout`, and logs to
   `run.log` + `vram.log`.
2. If install fails: fix **only** the environment (a version pin, a missing system package, a
   CUDA-index torch wheel). Record every fix. Do not touch experiment code. If you cannot fix it
   in 30 minutes, `report.py --reason env`.
3. If the entrypoint needs an argument the inspection did not capture, read the README and the
   script's argparse; prefer the configuration the post describes. Record it as a fix.
4. If the run needs a gated model, the HF token is already on this machine; if it is not,
   `--reason model-access`.
5. When it finishes, find the headline number in the output. Compare to the claimed value
   under the tolerance. Then:
   `python3 report.py --observed "<value>" --reason none [--fix "..."]... [--notes "..."]`
   — or with the right `--reason` if it failed. If the metric is not a scalar, pass
   `--reproduced true|false` and say why in `--notes`.
6. Append 3–6 lines to `run.log` under `== VERDICT`: what you observed, what you compared it to,
   what you changed, what you would need to go further.

## Do not

- Do not run more than **1 seed(s)** unless the run is under 10 minutes; if it is, run 3
  and report the spread — that is more valuable than the point estimate.
- Do not substitute a different model, dataset, or judge and call it a replication. Note it as a
  follow-up in `--notes` instead.
- Do not read the post's conclusion into ambiguous output. If you cannot tell which number is
  the headline, `--reason unclear-entrypoint` and say what you saw.
- Do not push, do not open issues, do not contact the authors.
