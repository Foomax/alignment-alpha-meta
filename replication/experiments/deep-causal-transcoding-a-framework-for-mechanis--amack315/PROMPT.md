# Replicate: Deep Causal Transcoding: A Framework for Mechanistically Eliciting Latent Behaviors in Language Models

Source post: `fSRg5qs9TPbNy3sm5` (2024-12-03, LW karma 109). Repo: `amack315/melbo-dct-post` @ `c0b76b746c38de3a4b38b01974c128b3790949c8`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Deep causal transcoders (DCTs) with an exponential activation function learn diverse, interpretable, and generalizable steering-vector directions that can jailbreak a representation-rerouted (robustified) Mistral-7B-Instruct-v2 with a 62% latent-space attack success rate and recover 32% of password-locked capability on DeepSeek-Math-7B (MATH accuracy 3% locked to 23% steered), outperforming linear and quadratic DCT variants

Supporting quote from the post: "I use exponential DCTs to jailbreak a [representation-rerouted](https://arxiv.org/abs/2406.04313) version of Mistral-7B-Instruct-v2, achieving a latent-space attack success rate of $62\%$."

**Headline metric:** latent-space jailbreak attack success rate; password-locked capability recovery (MATH accuracy)
**Claimed value:** 62% ASR on robustified Mistral-7B-Instruct-v2; MATH accuracy 3% (locked) to 23% (steered), recovering 32% of unlocked performance
**Direction of the claim:** +
**Uncertainty the post reported:** seeds
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `runs/train_mistral_rr.ipynb + runs/eval_mistral_rr.ipynb (jailbreak ASR); runs/train_deepseek.ipynb + runs/score_deepseek.py (MATH recovery)` (confidence: medium)
- Produces: runs/eval_mistral_rr.ipynb (ASR computed locally via cais/HarmBench-Mistral-7b-val-cls) and runs/score_deepseek.py / deepseek_eval_*.csv (MATH accuracy with vs without password)
- Models: GraySwanAI/Mistral-7B-Instruct-RR (7.0B), redwoodresearch/math_pwd_lock_deepseek_math7b_on_weak_pythia1b (7.0B), deepseek-ai/deepseek-math-7b-instruct (7.0B), cais/HarmBench-Mistral-7b-val-cls (7.0B), Qwen/Qwen1.5-7B-Chat (7.0B)
- Estimated VRAM: 16 GB — All models involved in the two headline numbers are 7B-class, loaded one at a time in bf16 (~14GB each); no README states this but the notebooks show standard from_pretrained(..., device_map='auto') with no quantization needed at this scale
- Data: hendrycks/competition_math (HF dataset, for the MATH recovery eval); availability: hf-hub
- Estimated runtime: hours (No timing stated. DCT training (NUM_ITERS=10, NUM_FACTORS=512, FACTOR_BATCH_SIZE=128) plus generation for jailbreak ASR (behaviors set) and 32-problem MATH eval x2 conditions (with/without password) on 7B models -- plausibly 1-3 hours on a 3090.)
- Stated compute in the repo: none
- Known blockers: No README/requirements.txt; procedure has to be reconstructed from bare notebooks and scripts (a demo_32b.ipynb exists for a separate Qwen1.5-32B cross-model demo not needed for the two headline numbers, which are both 7B-scale)
- Inspector's notes: Fully local and reproducible on a single 3090: jailbreak ASR is graded by a local HarmBench classifier model (cais/HarmBench-Mistral-7b-val-cls), not an LLM API, and MATH correctness is checked by string/regex matching against hendrycks/competition_math. Lack of any README/docs is the main friction, not compute.

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
