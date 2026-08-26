# Replicate: Do Sparse Autoencoders (SAEs) transfer across base and finetuned language models?

Source post: `bsXPTiAhhwt5nwBW3` (2024-09-29, LW karma 28). Repo: `tommasomncttn/sae-transferability` @ `0bdb3c4cfdc8056a203ab3a48c32d105c197ff62`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> SAE transferability from base to finetuned models is highly model-dependent: an SAE trained on Gemma-2b degrades drastically on a Python-code finetune while an SAE trained on Mistral-7B transfers well to a MetaMath finetune, and residual-activation similarity (cosine/Euclidean distance) between base and finetuned models anecdotally predicts this transferability.

Supporting quote from the post: "We got drastically different results for our Gemma-2b-python-codes and Mistral-7B-MetaMath finetunes."

**Headline metric:** Reconstruction CE Loss Delta / R^2 variance explained, base vs finetuned model with same SAE
**Claimed value:** Gemma-2b: loss delta 0.51 -> 4.21, R^2 0.97 -> -10.27; Mistral-7B: loss delta 0.15 -> 0.16, R^2 0.68 -> 0.58
**Direction of the claim:** na
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 12 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `notebooks/4_sae_eval.ipynb` (confidence: high)
- Produces: 4_sae_eval.ipynb output tables (Reconstruction CE Loss Delta, R^2 variance explained) comparing base vs finetuned model with the same pretrained SAE, for both Gemma-2b/python-finetune and Mistral-7B/MetaMath pairs.
- Models: google/gemma-2b (2.0B, gated), mistral-7b (mistralai/Mistral-7B-v0.1, via TransformerLens name) (7.0B, gated), shahdishank/gemma-2b-it-finetune-python-codes (2.0B), meta-math/MetaMath-Mistral-7B (7.0B)
- Estimated VRAM: 15 GB — Base model loaded fp16 via HookedSAETransformer.from_pretrained; largest case is Mistral-7B (~14GB weights) plus SAE + a controllable number of forward-pass batches, well within 24GB and far above the T4/L4 the README recommends.
- Data: ctigges/openwebtext-gemma-1024-cl or the SAE's own training dataset (loaded automatically by SAELens' ActivationsStore); availability: hf-hub
- Estimated runtime: minutes to hours (Sample size is fully controlled by activation_store's total_batches/store_batch_size_prompts/context_size (documented in README); no fixed runtime given but designed to run on free/low-tier Colab GPUs.)
- Stated compute in the repo: T4 GPU recommended for Gemma-2b, L4 GPU recommended for Mistral-7B (both on Colab).
- Known blockers: requires downloading a public gemma-2b/it-finetune and a public MetaMath-Mistral-7B finetune from the HF Hub, and a residual-stream outlier-filtering config (outlier_cfg.json, included in repo root); notebooks assume identical base/finetune tokenizer vocabularies and are written for Google Colab + Google Drive paths, needing light local adaptation; no version pins in requirements.txt (bare package names only)
- Inspector's notes: Best-documented repo of this batch: a clear README walks through the exact config (BASE_MODEL/FINETUNE_MODEL/RELEASE/hook_part/layer_num) needed to reproduce each of the two headline model pairs, all using public SAELens-hosted SAEs and public HF checkpoints. Both target models are far smaller than the T4/L4 Colab GPUs the authors used, so a 3090 has ample headroom.

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
