# Replicate: Towards a Science of Evals for Sycophancy

Source post: `WrKLhJWdTzbnTnXbx` (2025-02-01, LW karma 8). Repo: `andrejfsantos4/decomposing-sycophancy` @ `3461d47da3461c379c1f0bcb5bb62a9d8b67a869`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> The standard method of measuring LLM sycophancy (accuracy drop when an opinion decoy is added to a multiple-choice prompt) substantially overestimates true sycophancy, because most of the apparent effect is actually driven by a 'repetition bias' (the model favoring an answer merely because it is repeated in the prompt) rather than genuine agreement-seeking: in their Mistral-7B-Instruct/ARC-Easy setup, the naively measured 34-point accuracy drop reduces to a 22-point 'real sycophancy' effect once noise (~1 point) and repetition bias (~12 points) are subtracted out.

Supporting quote from the post: "Thus, by adjusting for both the noise and repetition bias factors, we conclude that the real sycophancy in our model is responsible for an accuracy degradation of 22 percentage points - less than two-thirds of the originally measured decrea"

**Headline metric:** accuracy on ARC-Easy under different decoy conditions
**Claimed value:** Baseline 75%; Opinion Bias 40.7% (-34.3pp); Noise (Opinion Decoy) 74.2% (-0.8pp); Repetition Bias 56.3% (-18.7pp from baseline); Noise (Repetition Decoy) 68.3% (-6.7pp from baseline); real sycophancy estimated at -22pp
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 10 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `sycophancy_decomposed.ipynb` (confidence: high)
- Produces: Per-condition accuracy on ARC-Easy (Baseline / Opinion Bias / Noise (Opinion Decoy) / Repetition Bias / Noise (Repetition Decoy)) computed by the notebook's evaluation loop and reported in the README results table.
- Models: mistralai/Mistral-7B-Instruct-v0.1 (7.0B)
- Estimated VRAM: 15 GB — AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map='auto') for a 7B model -- ~14-15GB fp16 weights plus KV cache/activations for ARC-Easy multiple-choice prompts.
- Data: allenai/ai2_arc (ARC-Easy test split); availability: hf-hub
- Estimated runtime: unknown (none given)
- Stated compute in the repo: none
- Known blockers: Notebook is written for Google Colab (README: 'configured to run in Google Colab') with no requirements.txt -- minor local porting needed; The same model-selection cell also supports a 30B Vicuna model (unused for reported results) which would not fit a 3090; only the Mistral branch is needed
- Inspector's notes: Small, self-contained, inference-only eval; a fp16 7B model comfortably fits a 3090 with plenty of room for batched ARC-Easy scoring.

## Budget

**90 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
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
