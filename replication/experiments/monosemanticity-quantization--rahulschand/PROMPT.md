# Replicate: Monosemanticity & Quantization

Source post: `8uMA6vwitdwqs5AH4` (2024-10-22, LW karma 1). Repo: `rahulschand/monosemanticity-quantization` @ `dd00a2557d265e2f55c86a601957c9905d7cb886`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Training a sparse autoencoder on a quantized 1-layer transformer (gelu-2l) shows that 8-bit quantization only slightly degrades SAE reconstruction accuracy and active-feature count relative to full precision, while 4-bit quantization degrades the underlying model so severely that its activations become near-noise, causing the SAE to achieve deceptively low L1/L2 loss by zeroing out over 80% of features rather than learning genuine fine-grained features.

Supporting quote from the post: "more than 80% of features are below 1e-5"

**Headline metric:** percentage of SAE features with average activation below 1e-5, by model precision
**Claimed value:** full precision and 8-bit show similar, gradual feature-learning trends with 8-bit only slightly behind; 4-bit shows more than 80% of features below 1e-5, indicating the SAE largely zeros out features rather than learning them
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `train.py (SAE training) chained by hand with quant.py/degrade.py/analyse_quant.py -- no single script runs the full quantize -> train -> measure pipeline` (confidence: low)
- Produces: percentage of SAE hidden features with freqs < 1e-5 (computed via get_freqs in my_utils.py / analysis.py, logged to wandb during train.py and printed/histogrammed in analysis.py) for full/8-bit/4-bit quantized gelu-2l
- Models: ? (0.003B)
- Estimated VRAM: 3 GB — gelu-2l is Neel Nanda's toy 2-layer, d_model=512 transformer (~a few million params); the SAE (my_utils.py AutoEncoder) has dict_size = act_size(512) * dict_mult(32) = 16384, so encoder+decoder weights are ~33M floats (~130MB fp32) plus an activation buffer of buffer_size=batch_size(2048)*buffer_mult(384)=786432 rows x 512 floats (~1.6GB fp32). All comfortably under 24GB.
- Data: NeelNanda/c4-code-20k (HF dataset, used by degrade.py and my_utils.py); availability: hf-hub
- Estimated runtime: hours-days (uncertain) (my_utils.py's unmodified default_cfg sets num_tokens=int(2e9) (2 billion tokens) for SAE training -- this is the original Neel Nanda 1L-SAE repo's default, carried over unchanged; the README/scripts never state how many tokens were actually used for the post's reported percentages, so whether the real run used the full 2e9-token budget (which would take many hours to ~a day+ on one 3090 for repeated forward passes through gelu-2l to refill the activation buffer) is unknown.)
- Stated compute in the repo: none
- Known blockers: no requirements.txt/pyproject.toml/environment.yml at all -- deps must be inferred from imports; no single script wires together quant.py (produces quant_4.bin/quant_8.bin) -> train.py (trains the SAE) -> analyse_quant.py/analysis.py (computes the <1e-5 feature percentage); my_utils.py's HookedTransformer.from_pretrained(cfg['model_name']) call for loading a quantized checkpoint is commented out, so the quantized-model SAE training path requires hand-editing the script; num_tokens actually used for the reported precision-by-precision comparison is unstated (repo carries the original repo's 2e9-token default, which may or may not match what produced the post's numbers)
- Inspector's notes: This is a lightly-modified fork of Neel Nanda's public 1L-Sparse-Autoencoder repo with a handful of loose, hand-run scripts (hardcoded filenames like quant_4.bin, quant_8.bin) rather than a packaged pipeline; a competent engineer could stitch it together and the model/SAE are tiny, but exact reproduction of the reported percentages is uncertain given the missing token budget and disconnected scripts.

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
