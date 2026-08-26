# Replicate: Learning Multi-Level Features with Matryoshka SAEs

Source post: `rKM9b6B2LqwSB5ToN` (2024-12-19, LW karma 46). Repo: `bartbussmann/matryoshka_sae` @ `c7c57877bb81df67fdac611f9c31ffc10495db0b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Matryoshka SAEs trained on Gemma-2-2B achieve worse reconstruction (MSE / variance explained) than standard BatchTopK SAEs but similar downstream cross-entropy loss, show dramatically lower feature-absorption rates (~0.03 vs up to ~0.29 for large BatchTopK SAEs) and feature-splitting, more disentangled latents (less shared information via meta-SAEs), and better targeted concept-erasure (TPP/SCR) performance, but show mixed results on k-sparse probing and only small differences in automated interpretability scores.

Supporting quote from the post: "Matryoshka SAEs show dramatically lower rates of feature absorption, feature splits and shared information between latents."

**Headline metric:** feature absorption rate (first-letter task, per Chanin et al. methodology)
**Claimed value:** Matryoshka SAEs maintain absorption rates around 0.03 even as dictionary size increases, vs BatchTopK SAEs reaching approximately 0.29 at larger dictionary sizes
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `main.py (trains the SAE checkpoints only; no evaluation code present)` (confidence: low)
- Produces: not identified
- Models: google/gemma-2-2b (2.61B, gated)
- Estimated VRAM: 12 GB — gemma-2-2b loaded via HookedTransformer.from_pretrained_no_processing(...).to(bfloat16) for forward-pass-only activation extraction (no LM gradients, model is frozen); six SAEs (dict sizes 2304 up to 36864, mostly fp32) are trained jointly with a modest activation buffer (num_batches_in_buffer=10, model_batch_size=32) — comfortably under 24GB.
- Data: Skylion007/openwebtext (streamed from HF Hub), 5e8 tokens; availability: hf-hub
- Estimated runtime: hours (num_tokens=5e8 streamed through gemma-2-2b (model_batch_size=32, seq_len=128) to train 6 SAEs jointly; no runtime is stated in the repo, but 500M tokens through a 2B-param model is a multi-hour single-GPU job.)
- Stated compute in the repo: none
- Known blockers: This repo is SAE-training code only. The requested headline metric — feature absorption rate on the first-letter task, per Chanin et al. — has no implementation anywhere in the repo; it would need to be built or sourced from a separate evaluation codebase (e.g. SAEBench).; No requirements.txt / pyproject.toml / environment.yml at all — README only says `pip install transformer_lens`; exact dependency versions (including implicit torch) are unknown.; gemma-2-2b is gated on HF Hub
- Inspector's notes: The repo reproduces the SAE checkpoints referenced by the post (5 BatchTopK SAEs + 1 Matryoshka SAE, all on Gemma-2-2B layer-8 resid_pre) but contains none of the downstream interpretability evaluations — absorption, feature splitting, meta-SAE disentanglement, TPP/SCR concept erasure, k-sparse probing, or auto-interp — that the post's target_value is actually stated in terms of.

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
