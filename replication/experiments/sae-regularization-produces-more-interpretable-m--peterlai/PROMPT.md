# Replicate: SAE regularization produces more interpretable models

Source post: `sYFNGRdDQYQrSJAd8` (2025-01-28, LW karma 21). Repo: `peterlai/gpt-circuits` @ `1cf99ec0580f33e19c37099b02d37a01b284ba5f`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Adding an SAE loss term as a regularizer during LLM training (jointly training SAE layers alongside model weights) improves downstream SAE feature sparsity/reconstruction quality on nearly all layers of a small character-level GPT-2 model, without apparently harming overall model performance.

Supporting quote from the post: "We find that SAE regularization improves SAE performance on all layers and does not seem to impact the model's overall performance."

**Headline metric:** cross-entropy loss increase at fixed SAE sparsity (L0~50)
**Claimed value:** SAE regularization reliably yields better (lower) cross-entropy loss increase on most layers; less dependable on some layers (e.g. layer 3); regularized models also reach slightly lower overall cross-entropy loss
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/regularization/train.py (steps 0-4, e.g. `python -m experiments.regularization.train --setup=all-layers --step=0..4`)` (confidence: high)
- Produces: experiments/regularization/results.sweep.json and results.sums.json (regularized vs. normal cross-entropy-loss-increase-at-fixed-L0 per layer), exported by train.py --step=4
- Models: ? (0.001B)
- Estimated VRAM: 1 GB — Toy character-level GPT-2, 4 layers, 64 embedding width (<1M params), trained on tiny-shakespeare (1.1MB); SAE regularization layers are similarly tiny (n_features up to ~4096 per layer). Would run on CPU; trivial on any GPU.
- Data: tiny-shakespeare (in-repo: data/shakespeare/input.txt, ASCII/character tokenizer); availability: in-repo
- Estimated runtime: hours (max_steps=15000 for base and regularized GPT training, plus num_sweep_steps=8 SAE-coefficient sweeps for both the normal and regularized models — all on a sub-1M-parameter model; no runtime is stated in the repo, but each individual run should be minutes, with the full multi-step pipeline totaling low single-digit hours on one GPU.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Fully self-contained toy reproduction: tiny in-repo data, no external model downloads, no gating. The five-step pipeline (train base GPT, train SAE-regularized GPT, sweep SAE loss coefficients on both, export results) is explicit in experiments/regularization/train.py and setup.py.

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
