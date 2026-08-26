# Replicate: Finding features in Transformers: Contrastive directions elicit stronger low-level perturbation responses than baselines

Source post: `QrPxNDprJwXiE73Py` (2026-03-20, LW karma 39). Repo: `franciscohs/contrastive-vs-sae-perturbation` @ `4fbe15471fdc5dc3474a8115dad0e721870e04fe`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Contrastive (difference-of-means) feature directions elicit a downstream perturbation response at much smaller magnitudes than SAE feature directions, which behave similarly to random directions, across multiple models and experimental setups, suggesting SAE directions are not treated specially by the model.

Supporting quote from the post: "Contrastive (difference-of-means, English→Mandarin) feature directions elicit a downstream response at much smaller perturbation magnitudes than SAE directions, which behave similarly to random directions. This holds across multiple models "

**Headline metric:** perturbation magnitude (angle in degrees) needed to elicit downstream response (L2 distance / KL divergence / cosine distance)
**Claimed value:** contrastive directions break through the suppression 'activation plateau' at much smaller magnitudes than SAE or random directions; SAE directions behave similarly to random directions
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `generate_figures.py` (confidence: high)
- Produces: results/gemma-9b-en-zh/plot_complete.png and plot_simplified.png (English/Mandarin contrast, L2 metric, layer 2) — the paper's main figure
- Models: google/gemma-2-9b (9.0B, gated), meta-llama/Llama-3.1-8B (8.0B, gated), Qwen/Qwen3-1.7B (1.7B)
- Estimated VRAM: 24 GB — README states ~24GB VRAM for Gemma2-9B bf16 (main figure); Llama-3.1-8B and Qwen3-1.7B runs need less since they're smaller models
- Data: FineWeb (random-direction baseline, streamed via datasets), bilingual/gender/programming paired prompts (included as data/*.py), Gemma Scope / Llama Scope / Qwen3 SAEs (via SAELens from HF Hub); availability: hf-hub
- Estimated runtime: hours (not stated explicitly; full --sweep spans 9 figure configs x 3 models x N_ANGLES=90 x N_ACT=30 x N_CURVES=10 x N_DIRS=10 forward passes; a --plot-only pass using the repo's committed results/*.pkl reproduces every figure in seconds with no GPU)
- Stated compute in the repo: Requires ~24GB VRAM (for Gemma2-9B in bfloat16). An RTX 4090 or A100 works well.
- Known blockers: none recorded
- Inspector's notes: Unusually reproducible repo: precomputed sweep data (.pkl) and plots for all 9 figures are already committed, so figures regenerate without any GPU via --plot alone; full from-scratch reproduction needs gated HF access to Gemma-2-9B and Llama-3.1-8B.

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
