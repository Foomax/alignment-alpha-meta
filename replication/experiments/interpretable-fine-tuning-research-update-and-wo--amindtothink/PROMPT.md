# Replicate: Interpretable Fine Tuning Research Update and Working Prototype

Source post: `xZkBDAgQGqm6tvCvy` (2025-05-16, LW karma 14). Repo: `amindtothink/interpretable-fine-tuning` @ `eed9438f1ca8a6c99dbdc71c5ce2692611eb5da6`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> ISaeRFT (Interpretable Sparse Autoencoder Representation Fine Tuning) — a technique that gradient-optimizes IA3-style learned scaling factors on SAE latents via a HuggingFace PeftModel — has a working prototype where DPO loss decreases significantly within as few as 20 training steps, though the research is at a very early stage with no major proof of concept yet on downstream tasks.

Supporting quote from the post: "DPO loss goes down significantly in as few as 20 steps."

**Headline metric:** DPO loss during training
**Claimed value:** DPO loss goes down significantly in as few as 20 steps
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/training/ia3_training_isaerft_disable_available.py` (confidence: high)
- Produces: wandb-logged DPO loss curve produced by src/training/ia3_training_isaerft_disable_available.py -- the plot referenced in the post as 'DPO loss goes down significantly in as few as 20 steps'.
- Models: google/gemma-2-2b (2.0B, gated)
- Estimated VRAM: 10 GB — Frozen gemma-2-2b (bf16, ~4-5GB) plus a frozen SAE (gemma-scope-2b-pt-res-canonical, layer 20, width 16k, a few hundred MB); only a small IA3-style adapter is trained via DPOTrainer. The repo's own REPRODUCE.md notes bitsandbytes/deepspeed are pinned in requirements.txt but unused by the tracked training code -- no quantization or multi-GPU sharding needed.
- Data: trl-internal-testing/hh-rlhf-helpful-base-trl-style (DPO preference data, auto-downloaded); availability: hf-hub
- Estimated runtime: unknown (Post states DPO loss 'decreases significantly within as few as 20 steps' but gives no wall-clock figure; the repo's own REPRODUCE.md doc also states no runtime/VRAM figure could be found anywhere in the code, comments, or commit history.)
- Stated compute in the repo: none
- Known blockers: google/gemma-2-2b is a gated model (licence acceptance + `hf auth login` required); Training scripts call wandb.init()/report_to='wandb' unconditionally -- needs a wandb account/API key or a code edit to disable; NEURONPEDIA_API_KEY is read by the same script for feature-description fetching (interpretability/visualization side-channel, not needed for the core DPO-loss curve, but its absence may error depending on code path)
- Inspector's notes: This repo ships an unusually thorough audit doc (REPRODUCE.md, apparently written by a prior reviewer) which I cross-checked directly against the source; the actual compute footprint is small since only a tiny adapter is trained on a frozen 2B model, but no explicit VRAM figure is stated anywhere in the repo itself.

## Budget

**180 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
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
