# Replicate: Adding noise to a sandbagging model can reveal its true capabilities

Source post: `jZfNX4GJPdptxSxt4` (2025-07-11, LW karma 18). Repo: `lovkush-a/arena-sandbagging-mi` @ `d801cd70a6945d42e14370465da13b86815c376f`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Adding noise to the weights of a sandbagging Qwen2.5-1.5B-Instruct model can increase its GSM8k performance (revealing hidden capability), replicating the main effect from 'Noise Injection Reveals Hidden Capabilities of Sandbagging Language Models' with a different model and dataset.

Supporting quote from the post: "If you add noise to the parameters of a model that is sandbagging, then sometimes its performance on a task can increase."

**Headline metric:** accuracy on 350 GSM8k questions vs weight noise level
**Claimed value:** for some seeds, accuracy of the sandbagging-prompted model increases as noise is added, while the normal-prompted model's accuracy decreases with noise
**Direction of the claim:** +
**Uncertainty the post reported:** seeds
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/exp07_add_noise_with_batches.py (uses src/eval_model_on_dataset_batches.evaluate_model_on_dataset)` (confidence: high)
- Produces: logs/20250529_qwen_prompts1/*.csv (per noise_scale/seed accuracy on GSM8K, sandbag vs original prompt) -- committed logs already show the qualitative effect (some seeds: sandbag accuracy rises with noise while original accuracy falls)
- Models: Qwen/Qwen2.5-1.5B-Instruct (1.5B)
- Estimated VRAM: 8 GB — 1.5B model in bf16 (~3GB weights) with batch_size=350 (whole 350-question GSM8K eval in one batch), max_new_tokens=400, GQA with only 2 KV heads (Qwen2.5-1.5B config) keeps the KV cache to roughly 6-7GB even at this batch size
- Data: gsm8k (main config), first 350 rows of the train split; availability: hf-hub
- Estimated runtime: hours (10 seeds x 5 noise scales x 2 prompt conditions = 100 generation runs of 350 examples each (batch_size=350, max_new_tokens=400) on a 1.5B model -- each run is a couple of minutes, so the full seed/noise-scale sweep plausibly finishes in a few hours on a 3090)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Small, simple ARENA-capstone-style repo with no pinned versions but a very direct, single-file entrypoint; requirements.txt lists transformer-lens but the actual final experiment (exp07) uses plain HF transformers, per the README's own note about switching backends mid-project. Committed logs/ CSVs from the original run are included, so the qualitative claim can be checked without even re-running anything.

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
