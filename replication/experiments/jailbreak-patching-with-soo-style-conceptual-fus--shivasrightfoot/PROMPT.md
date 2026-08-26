# Replicate: Jailbreak Patching with SOO-Style Conceptual Fusion

Source post: `EXj2bYK2rg8TMrncF` (2026-07-16, LW karma 8). Repo: `shivasrightfoot/soo-jailbreak-conceptual-fusion` @ `c4bf965d0cf3ee51eb826ba33eefec90f00ae81f`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> SOO-style conceptual fusion fine-tuning (with a KL retention regularizer) at layer 18 increases refusal on a jailbreak-wrapped HarmBench prompt set from ~20% in the base Qwen 2.5 1.5B model to a little under 90%, outperforms comparable supervised fine-tuning at increasing jailbreak refusal, better preserves non-refusal on safe XSTest prompts than SFT, and generalizes to a held-out jailbreak wrapper never seen in training.

Supporting quote from the post: "the selection of 1/8th weight and layer 18 produces an increase in refusal behavior for jailbroken wrappers from around 20% in the base model to a little under 90% in the fine tuned model"

**Headline metric:** refusal rate on held-out jailbreak-wrapped HarmBench prompts
**Claimed value:** ~20% (base model) to a little under 90% (conceptual fusion, layer 18, 1/8 retention weight)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 5 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `02_soo_conceptual_fusion_training.ipynb` (confidence: high)
- Produces: Figure 3 (refusal rate vs. RETAIN_WEIGHT at layer 18) produced by running 01_refusal_behavior_testing.ipynb against the adapter saved by 02_soo_conceptual_fusion_training.ipynb, using the in-repo keyword refusal classifier (no LLM judge -- notebook explicitly notes keyword classifier outperformed same-model LLM-as-judge in the source study this is adapted from).
- Models: Qwen/Qwen2.5-1.5B-Instruct (1.5B)
- Estimated VRAM: 6 GB — bf16 1.5B model, LoRA rank 8 on q_proj/v_proj of layers below target layer, single-example forward passes (no batching) plus a KL retain-loss forward pass; trivially small.
- Data: walledai/HarmBench (standard split), walledai/XSTest, in-repo jailbreak_baseline_results_raw_Qwen.csv; availability: hf-hub
- Estimated runtime: minutes (3 epochs over a small set of jailbroken training pairs (subset of 50-holdout-excluded HarmBench 'Hypothetical' rows), one prompt at a time, no batching, 1.5B model -- well under an hour on a 3090.)
- Stated compute in the repo: none
- Known blockers: XSTest is a gated HF dataset requiring a one-time click-through acceptance (not an API-key blocker, just a manual step).
- Inspector's notes: Extremely clean, fully self-contained 4-notebook repo (train fusion adapter, train SFT baseline, test refusal behavior, analyze delta-W by layer). Refusal detection is a keyword classifier, not an LLM judge, so no closed API needed anywhere in the pipeline. This is one of the easiest repos to replicate in the batch.

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
