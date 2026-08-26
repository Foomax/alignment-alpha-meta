# Replicate: When Benchmarks Lie: Evaluating Malicious Prompt Classifiers Under True Distribution Shift

Source post: `2H6PAK7YELjEsHkEc` (2026-02-23, LW karma 1). Repo: `maxf-zn/prompt-mining` @ `2aadf4e6fe0dc47c6558e13ba8bdcc2c19141819`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A lightweight logistic-regression probe trained on Llama-3.1-8B-Instruct's internal activations to classify malicious agentic prompts substantially outperforms Meta's Prompt-Guard-2, Llama-Guard-3-8B, and prompting the same base model as a judge across most attack categories (e.g. 99.2% recall on agentic tool-use injections vs 21.5% for the LLM-judge baseline), but the model's true out-of-distribution generalization is much worse than standard train/test-split evaluation suggests, as revealed by leave-one-dataset-out (LODO) evaluation across 18 datasets.

Supporting quote from the post: "If someone were to show you a system with a test accuracy like the "Test Acc" above - you would buy it probably. But the "LODO Acc"? No way. Same exact model, different ways to measure."

**Headline metric:** recall (%) per attack category, FPR (%) on benign data, comparing standard test-split accuracy to LODO accuracy
**Claimed value:** recall: Agentic 99.2% (ours) vs 21.5% (Llama-Judge); Indirect 66.7% (ours) vs 27.4% (Llama-Guard); benign FPR 6.8% (ours, low threshold) vs 0.4% (Prompt-Guard); standard test accuracy much higher than LODO accuracy on the same model (qualitative, no numeric value given)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `prompt_mining/ingestion/run_ingestion.py (activation capture) + prompt_mining/classifiers/lodo.py (LODO evaluation) — a multi-step pipeline, not a single script` (confidence: medium)
- Produces: LODOResult (per-dataset and weighted-average accuracy/F1/ROC-AUC) from prompt_mining/classifiers/lodo.py, comparing the linear-probe classifier against PromptGuardEvaluator/LlamaGuardEvaluator/LlamaJudgeEvaluator labels captured via run_ingestion.py.
- Models: meta-llama/Llama-3.1-8B-Instruct (8.0B, gated), meta-llama/Llama-Guard-3-8B (8.0B, gated), meta-llama/Llama-Prompt-Guard-2-86M (0.086B, gated)
- Estimated VRAM: 16 GB — ModelWrapper's default dtype config is 'float32' (model_wrapper.py:37), which would need ~32GB for an 8B model (exceeds 24GB). bf16/fp16 are supported via a one-line config change (not the default), which brings an 8B model to ~16GB, comfortably fitting a single 3090.
- Data: ~15 HF-hosted prompt-injection/safety/instruction datasets (AdvBench, HarmBench, WildJailbreak, Dolly15K, OpenOrca, etc.), BIPIA and InjecAgent, which must be git-cloned separately (not bundled); availability: hf-hub
- Estimated runtime: unknown (ingestion_config.yaml shows optional per-dataset num_prompts limits (e.g. 1000), but no wall-clock or throughput figures are given anywhere in the README.)
- Stated compute in the repo: none
- Known blockers: No single 'run the headline experiment' script: reproducing the paper's exact numbers requires (1) an ingestion_config.yaml covering all ~18 datasets, 2 of which (BIPIA, InjecAgent) must be manually git-cloned first, (2) running the multi-GPU ingestion orchestrator to capture Llama-3.1-8B-Instruct activations plus PromptGuard/LlamaGuard/LlamaJudge labels for every dataset, then (3) training the classifier and running LODO — none of these steps ship with config values pinned to the paper's exact setup.; Default model dtype is float32 (~32GB for an 8B model); needs a config change to bf16 to fit a single 24GB 3090.; All three target/baseline models are gated on Hugging Face and require accepting Meta's Llama license plus an HF_TOKEN.
- Inspector's notes: This is a mature, well-documented general-purpose activation-mining platform (not a single-experiment script) built specifically to produce this paper's results. LlamaJudgeEvaluator uses a local Llama model as judge (not GPT-4/Claude), so the headline recall/FPR numbers need no closed API; Bedrock/Claude is used only optionally for SAE-feature-name interpretation, unrelated to the headline metric.

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
