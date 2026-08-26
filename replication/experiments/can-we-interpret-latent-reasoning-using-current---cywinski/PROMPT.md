# Replicate: Can we interpret latent reasoning using current mechanistic interpretability tools?

Source post: `YGAimivLxycZcqRFR` (2025-12-22, LW karma 44). Repo: `cywinski/codi` @ `f0bf2fa0f5a54c749395a5d095bc406ad18b8efc`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Standard mechanistic interpretability techniques (logit lens, activation patching, probing) can reveal that a CODI latent-reasoning model stores intermediate math calculation results in specific latent vectors (the third and fifth of six)

Supporting quote from the post: "We find that the model solves maths problems requiring three reasoning steps by storing the two intermediate values in specific latent vectors (the third and fifth of six)."

**Headline metric:** accuracy recovery / answer-flip rate under activation patching
**Claimed value:** model recovers ~20% accuracy (from 55% baseline) when patching in latent vectors after mean-ablating specific numbers; patching third/fifth latent vectors with different-intermediate-value vectors notably decreases accuracy while same-value patching leaves accuracy unchanged
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/4_mean_latent_patching_same_vs_diff.py` (confidence: high)
- Produces: accuracy recovery under mean-ablation + latent-vector patching and answer-flip rates under same/different-value latent patching, from experiments/4_mean_latent_patching_same_vs_diff.py and experiments/5_step2_latent_patching.py
- Models: meta-llama/Llama-3.2-1B-Instruct (1.2B, gated), bcywinski/codi_llama1b-answer_only (trained CODI checkpoint) (1.2B)
- Estimated VRAM: 4 GB — inference-only activation patching / logit-lens / probing experiments on a 1.2B-param model with a LoRA-based CODI adapter loaded on top; no training required for the interpretability experiments themselves
- Data: GSM8K-derived prompts (produced by prepare_prompts_json.py); availability: in-repo
- Estimated runtime: minutes (inference-only patching/logit-lens/probing experiments over a small prompt set with a 1.2B model)
- Stated compute in the repo: none
- Known blockers: meta-llama/Llama-3.2-1B-Instruct is gated on HF and requires an accepted license plus HF_TOKEN (per .env.template)
- Inspector's notes: Cleanest repo in this batch: explicit .env.template, fully pinned requirements.txt, and experiment scripts numbered to match the blog post's figures directly; both the base model and the trained CODI checkpoint are small and on HF hub.

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
