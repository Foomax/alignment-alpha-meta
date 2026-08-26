# Replicate: Latent Space Collapse? Understanding the Effects of Narrow Fine-Tuning on LLMs

Source post: `f6LoBqSKXFZzMYACN` (2025-02-28, LW karma 3). Repo: `tenseisoham/finetuning-mechinterp` @ `483cc014d5cea7691675d7e4e27389bb9acc660b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Narrow sentiment fine-tuning of GPT-2 does not simply overwrite pretrained representations but reconfigures and 'squishes' the model's output and activation space, concentrating sentiment information in middle-to-late layers while sharply degrading general language modeling (perplexity) on non-sentiment inputs.

Supporting quote from the post: "fine-tuning does not simply overwrite pre-trained representations but reconfigures them entirely, redistributing sentiment-specific information across layers and squishing the output representation space"

**Headline metric:** perplexity on non-sentiment tokens
**Claimed value:** 160.87 (base model) vs 49,802.45 (fine-tuned model)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `logit-lens-analysis.ipynb` (confidence: high)
- Produces: compute_perplexity() output in logit-lens-analysis.ipynb comparing base vs. fine-tuned GPT-2 on non-sentiment text (the 160.87 vs 49,802.45 numbers).
- Models: gpt2 (0.124B)
- Estimated VRAM: 2 GB — GPT-2 small full fine-tune plus forward-pass perplexity evaluation -- trivial footprint even at fp32.
- Data: imdb (HF datasets, for sentiment fine-tuning and eval); availability: hf-hub
- Estimated runtime: minutes (GPT-2 small full fine-tune on IMDb sentiment (finetune-sentiment-gpt2small.ipynb, checkpoint-3126 implies a few thousand steps) followed by perplexity eval over a 200-sample IMDb subset -- well under an hour on a 3090.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Clean, small-scale, fully self-contained notebook sequence (finetune -> post-finetune analysis -> logit-lens perplexity/entropy -> alignment/transferability). No README beyond a one-paragraph pointer to the LessWrong post; no requirements file, but all dependencies are standard and unpinned so version drift risk is low for such a simple pipeline.

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
