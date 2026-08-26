# Replicate: Machine Unlearning in Large Language Models: A Comprehensive Survey with Empirical Insights from the Qwen 1.5 1.8B Model

Source post: `zmfXZEsiycGLP9YZW` (2025-02-01, LW karma 9). Repo: `saketh11111/rwku` @ `8400ae02b25735ab6c3a274fd4611f21fba4ca5b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In an empirical case study applying Gradient Ascent and DPO unlearning to Qwen 1.5 1.8B on the RWKU benchmark, both methods erased targeted ('Mia') knowledge (e.g. raising forget loss to -2.807 vs -2.547 retain) but caused catastrophic collateral damage to general capabilities (TriviaQA EM collapsed to 0.0 from 0.61; BBH EM dropped to 0.037 from 0.45), while residual knowledge traces remained detectable via mink++ distance metrics, undermining claims of complete/GDPR-compliant erasure.

Supporting quote from the post: "GA successfully raised the loss on the "Mia" dataset portion but also collapsed performance on factual retrieval (TriviaQA EM = 0.0) and reasoning tasks (BBH EM = 0.037). This underscores GA's raw power yet risky side effects."

**Headline metric:** TriviaQA EM / BBH EM / forget-retain loss and mink++ gap
**Claimed value:** GA: Forget loss -2.807 vs Retain -2.547; TriviaQA EM 0.0 (forget) vs 0.61 (retain); BBH EM 0.037 (forget) vs 0.45 (retain); mink++_1.0 -0.033 (forget) vs -0.019 (retain); DPO: BBH EM 0.037 down from 0.45 baseline
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 11 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `LLaMA-Factory/scripts/full/run_ga.sh (Qwen1.5-1.8B, GA); LLaMA-Factory/scripts/full/run_dpo.sh does NOT match the claimed model (see blockers)` (confidence: medium)
- Produces: LLaMA-Factory/src/llmtuner/eval/{eval_triviaqa,eval_bbh,eval_forget,eval_mia}.py outputs, aggregated per target
- Models: Qwen/Qwen1.5-1.8B (1.8B)
- Estimated VRAM: 8 GB — 1.8B full-parameter fine-tune with --gradient_checkpointing, per_device_train_batch_size=1, gradient_accumulation_steps=4 - small model, modest footprint
- Data: RWKU benchmark (jinzhuoran/RWKU on HF: forget/neighbor/mia/utility sets, train_positive/train_pair/train_refusal corpora); availability: hf-hub
- Estimated runtime: hours to a day for the full 100-target sweep (run_ga.sh loops over all 100 RWKU targets, each training Qwen1.5-1.8B full-parameter for 3 epochs; a single target on a 1.8B model is fast, but the 100-target loop plus evaluation (TriviaQA, BBH, mink++ MIA) is the multi-hour/day-scale part)
- Stated compute in the repo: none
- Known blockers: run_dpo.sh (and every script under LLaMA-Factory/scripts/batch/) hardcodes --model_name_or_path meta-llama/Meta-Llama-3-8B-Instruct, not Qwen1.5-1.8B - reproducing the claimed Qwen1.5-1.8B DPO result requires manually editing the script; only the GA script actually targets Qwen1.5-1.8B; No 'Mia'-specific single-target case-study script or output file exists in the repo; the post's specific numbers (forget loss -2.807, TriviaQA EM 0.0, mink++ deltas) are not shipped as artifacts and must be produced by running the (partially mismatched) generic pipeline; Repo is an unmodified fork of the original RWKU/LLaMA-Factory codebase vendored wholesale, with no repo-specific results or notebook committed
- Inspector's notes: GA-on-Qwen1.5-1.8B is directly runnable and cheap on a 3090. DPO-on-Qwen1.5-1.8B, despite being central to the post's claim, is not actually scripted here - only DPO-on-Llama-3-8B is - a real gap between the primary claim and the shipped code.

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
