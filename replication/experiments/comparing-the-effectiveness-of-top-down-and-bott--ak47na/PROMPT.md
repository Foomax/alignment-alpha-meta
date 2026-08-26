# Replicate: Comparing the effectiveness of top-down and bottom-up activation steering for bypassing refusal on harmful prompts

Source post: `boB3hJiZijxM3J6Ed` (2025-02-12, LW karma 7). Repo: `ak47na/top_down_vs_bottom_up_mi` @ `24b2cb90ebb7b08d68fb1106c37a3af17c12378b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Top-down activation steering (contrastive refusal-direction) outperforms bottom-up SAE-based steering at bypassing refusal on harmful prompts in Qwen 1.5 0.5B, but a hybrid method combining both further outperforms top-down alone, at some cost to benign capabilities.

Supporting quote from the post: "experiments show that top-down methods outperform bottom-up ones in behaviour steering (93% relative improvement), but a hybrid approach is even more effective (~35% relative improvement compared to top-down)."

**Headline metric:** relative improvement in bypassing refusal on HarmBench
**Claimed value:** top-down ~93% relative improvement over bottom-up (~1.93x more effective); hybrid ~35% relative improvement over top-down (~1.85x), 85% for harmful instructions only
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 5 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `evals.ipynb` (confidence: medium)
- Produces: evals.ipynb's get_refusal_scores() comparison across top-down/bottom-up/hybrid steering completions (harmbench methodology), producing the relative-improvement percentages quoted in the post
- Models: Qwen/Qwen1.5-0.5B-Chat (0.5B), cais/HarmBench-Mistral-7b-val-cls (7.0B)
- Estimated VRAM: 4 GB — Qwen1.5-0.5B-Chat is tiny (~1GB bf16) with a 32768-wide SAE hook adding negligible VRAM; the separate HarmBench-Mistral-7b-val-cls judge (~14GB via vLLM) comes from a different, cloned repo's eval code, not this repository itself
- Data: harmful/harmless instruction datasets (via utils.get_harmful_instructions/get_harmless_instructions, source not fully inspected), SAE checkpoint via W&B artifact ckkissane/qwen-500M-chat-lmsys-1m-anthropic:v11; availability: unknown
- Estimated runtime: minutes (n_inst_train=128 on a 0.5B model with SAE hooks; not stated but trivially small given model size)
- Stated compute in the repo: none
- Known blockers: README's 'pip install -r requirements.txt' references a file that does not exist anywhere in the repo; dependencies must be inferred from imports (transformer_lens, sae_lens, wandb, einops, vllm); evals.ipynb's early cells run '!git clone .../refusal_direction.git' then '%cd sae-dataset-dependence/refusal_direction' — a path that clone would not create — suggesting stale/copy-pasted cell paths from a sibling project that need manual fixing before the notebook runs; SAE is pulled from one specific W&B artifact version; requires a (free) W&B account and that artifact remaining available
- Inspector's notes: Model under test (Qwen1.5-0.5B-Chat) is trivially small and fits any GPU; risk is glue code, not compute — README's stated entrypoint (main.py) is wrong (actual path is aisf/main.py), and evals.ipynb has apparent leftover paths from a sibling repo (sae-dataset-dependence).

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
