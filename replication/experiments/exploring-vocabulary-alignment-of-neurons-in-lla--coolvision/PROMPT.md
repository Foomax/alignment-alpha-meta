# Replicate: Exploring vocabulary alignment of neurons in Llama-3.2-1B

Source post: `nnHnNdHLhbrnmEXDr` (2025-06-07, LW karma 4). Repo: `coolvision/interp` @ `cfe19a1b18d1055c6e9a838eecab3c59ec288c50`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Applying the logit lens to MLP output weights of Llama-3.2-1B reveals that a subset of neurons are strongly aligned with specific vocabulary token embeddings (forming a long tail in the max-dot-product distribution), with this vocabulary alignment concentrated more in later layers, while other neurons remain roughly equidistant from all vocabulary tokens.

Supporting quote from the post: "In summary, strong vocabulary alignment is clearly visible in a subset of neurons – especially in later layers."

**Headline metric:** max dot product between MLP neuron output weight and unembedding matrix (logit-lens alignment)
**Claimed value:** non-symmetric, long-tailed distribution with a significant number of neurons strongly aligned to vocabulary; alignment more prevalent in later layers
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `LLaMA_jun_4_2025_neurons.ipynb` (confidence: high)
- Produces: Histogram and sorted-line plots (notebook cells 4-10) of max |dot product| between each MLP neuron's W_out/W_in/W_gate row and the unembedding matrix W_U, per layer.
- Models: meta-llama/Llama-3.2-1B-Instruct (1.0B, gated)
- Estimated VRAM: 5 GB — TransformerLens HookedTransformer.from_pretrained defaults to fp32 when no dtype is passed; 1B params x4 bytes ~4GB weights, plus a trivial activation footprint since the notebook only does matrix multiplies of MLP weights against W_U (no dataset forward passes).
- Data: none listed; availability: not applicable — no dataset is used, only the model's own weights
- Estimated runtime: minutes (Pure weight-space analysis (dot products of W_out/W_in/W_gate against W_U across 16 layers); no training, no dataset iteration, no generation.)
- Stated compute in the repo: none
- Known blockers: meta-llama/Llama-3.2-1B-Instruct is gated on HuggingFace — needs license acceptance; no requirements.txt/pyproject.toml — transformer_lens/transformers versions must be inferred
- Inspector's notes: Extremely lightweight: a self-contained 13-cell notebook plus a utils.ipynb helper (%run'd in), no README. Entirely weight-space analysis with no dataset or gradient computation, so it is nearly guaranteed to reproduce given the same model checkpoint.

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
