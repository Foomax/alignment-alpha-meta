# Replicate: Activation Magnitudes Matter On Their Own: Insights from Language Model Distributional Analysis

Source post: `6PCjTM55jdYBgHNyp` (2025-01-10, LW karma 4). Repo: `good-epic/activation-tails` @ `cd30fc5feb6c60afb72eb450a3ce84d7b28b2c29`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Restricting analysis to only the extreme 'tail' values of transformer residual-stream activation distributions (rather than using all activation values) improves prediction of input-text properties (subject/attribute) via empirical log-likelihood classification: for GPT2-Small, GPT2-Medium, GPT2-Large, and Pythia-1B, tails-only analysis improved average F1 by 0.03 for subject prediction and 0.06 for attribute prediction versus using all activation values, though it failed almost entirely for the two smaller Pythia models (160M, 410M).

Supporting quote from the post: "the tails only analysis improved the average F1 score for prediction of sentence subject by 0.03 and for sentence attribute by 0.06"

**Headline metric:** F1 score, tails-only vs all-points activation-distribution analysis
**Claimed value:** tails-only analysis improved average F1 by 0.03 (subject) and 0.06 (attribute) for GPT2-Small/Medium/Large and Pythia-1B; failed almost entirely for Pythia-160M and Pythia-410M
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 7 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `kde_predict_main.py` (confidence: high)
- Produces: F1 scores from `kde_predict_main.py --detect-tails` (tails-only) vs. the full-activation-distribution run, aggregated/visualized in results_analysis.ipynb.
- Models: gpt2 (0.124B), gpt2-medium (0.355B), gpt2-large (0.774B), EleutherAI/pythia-160m-deduped (0.16B), EleutherAI/pythia-410m-deduped (0.41B), EleutherAI/pythia-1b-deduped (1.0B)
- Estimated VRAM: 2 GB — All models are <=1B parameters loaded via TransformerLens HookedTransformer with no dtype override; even fp32 for a 1B model is only ~4GB.
- Data: data_in/*.json bundled sentence datasets (economics, poetry, one-level categories), plus a bundled train/test split JSON; availability: in-repo
- Estimated runtime: minutes to low hours (README gives the exact two reproduction commands; data_in files are small JSON sentence lists, and the only heavy step is per-layer, per-category KDE fitting on activations (batch_size 20).)
- Stated compute in the repo: none
- Known blockers: No requirements/pin file at all — versions of torch, transformer_lens, scikit-learn, and scipy are entirely unconstrained.
- Inspector's notes: Simplest and most directly reproducible repo of the batch: exact README-given commands map onto the paper's headline result, every model is <=1B, and all data is bundled in-repo.

## Budget

**240 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
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
