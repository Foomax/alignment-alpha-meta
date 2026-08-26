# Replicate: You don't need error nodes, you need better features

Source post: `4tEnmAwFNtz9zJ6cz` (2026-07-27, LW karma 26). Repo: `evan-lloyd/mechinterp-experiments` @ `d563cf5840546944441f3538a9cdb07327b92b50`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Replacement-aware SAE training, combined with a LISTA-based encoder and KL fine-tuning, greatly reduces the KL divergence of a full SAE-replacement model from the base Gemma-2-2B model (validation KL 0.379-0.535 vs 1.006 for standard SAE training, vs 1.669 for Gemma Scope), producing replacement models that remain fluent and capable enough to give valid multiple-choice answers, whereas standard-trained replacement models are largely incoherent.

Supporting quote from the post: "Replacement-aware training greatly reduces KL divergence between the replacement model and base model as compared to standard methods, without sacrificing faithfulness"

**Headline metric:** Validation KL divergence from base model (nats)
**Claimed value:** 0.379-0.535 (replacement-aware + LISTA (+fine-tune)) vs 1.006 (standard) vs 1.669 (Gemma Scope)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 4 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `transformers_sae/scripts/train_gemma_standard.py or train_gemma_with_lista.py -> scripts/fine_tune_gemma.py -> scripts/validate_gemma.py -> notebooks/gemma_plots.ipynb` (confidence: medium)
- Produces: notebooks/gemma_plots.ipynb KL-divergence comparison table (standard vs replacement-aware+LISTA(+fine-tune) vs Gemma Scope)
- Models: google/gemma-2-2b (2.0B, gated)
- Estimated VRAM: 14 GB — 2B model bf16 (~5GB) plus a full-model replacement wrapping every layer with a per-layer SAE (dict size 16384, LISTA encoder) trained jointly; TRAINING_BATCH_SIZE is hardcoded to 2 (1024-token sequences) even for the CUDA path, suggesting a VRAM-constrained design
- Data: monology/pile-uncopyrighted-parquet (streaming), monology/pile-test-val, CommonsenseQA (for the CQA fine-tune variant); availability: hf-hub
- Estimated runtime: hours to ~1-2 days per single training run (NUM_TRAINING_TOKENS = 5e7 at batch_size 2 x 1024 tokens/step through a 2B model + 26 SAEs; author states reproducing ALL runs in the post takes 'several days on a 5090' (32GB, faster than a 3090), implying a single run/row is well under a day on faster hardware and plausibly under ~2 days on a 3090)
- Stated compute in the repo: README: 'I don't have a unified script for reproducing my main training runs... it would take at least several days on a 5090 to reproduce every run used in the post'
- Known blockers: google/gemma-2-2b requires accepting Google's gated license on Hugging Face; No single reproduce-the-table script - training, fine-tuning, validation, and plotting are separate manual invocations chained per README prose; The Gemma Scope comparison point (1.669 nats) is an externally published SAE suite, not trained in this repo - would need to separately download Gemma Scope's checkpoints to reproduce that column
- Inspector's notes: Training code is real, runnable, and uses conspicuously small batch sizes suggesting consumer-GPU development, but reproducing the exact headline KL table requires chaining several scripts by hand plus sourcing an external SAE suite (Gemma Scope) for one of the three comparison numbers.

## Budget

**480 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
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
