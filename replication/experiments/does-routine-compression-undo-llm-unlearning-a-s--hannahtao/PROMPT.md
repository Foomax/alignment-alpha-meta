# Replicate: Does routine compression undo LLM unlearning? A short project

Source post: `jXhHH658J4xzWjCu8` (2026-07-20, LW karma 19). Repo: `hannahtao/compression-unlearning` @ `ddf55e3a9572351615ec1425cabac7c873466bb1`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Standard post-training compression (quantization, magnitude pruning, SVD truncation) mostly does not reverse unlearning on TOFU forget10 / Llama-3.2-1B-Instruct across NPO, SimNPO, and IdkDPO unlearning methods, but the strongest reversal came from magnitude pruning in a narrow 10-20% sparsity window on NPO unlearning, recovering up to 42% of the ceiling-baseline gap.

Supporting quote from the post: "the strongest reversal came from magnitude pruning in a narrow 10-20% sparsity window on NPO unlearning (up to 42% of the ceiling–baseline gap recovered)"

**Headline metric:** recovery = (compressed - baseline) / (ceiling - baseline) on forget_Q_A_Prob
**Claimed value:** 4-bit quantization on NPO: 22% recovery; magnitude pruning at 20% sparsity on NPO: 42% recovery peak; SVD truncation: no significant recovery (-26% at 99% keep); SimNPO/IdkDPO: <=3% recovery in all non-destructive cells
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 7 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `run_sweep.sh (compress_model.py + OpenUnlearning's src/eval.py)` (confidence: high)
- Produces: results/sweep_results.csv normalized-recovery table (NPO/SimNPO/IdkDPO x quant/prune/SVD), specifically the NPO 20% pruning peak (42% recovery) and 4-bit quant (22% recovery) cells
- Models: open-unlearning/unlearn_tofu_Llama-3.2-1B-Instruct_forget10_NPO_lr1e-05_beta0.1_alpha1_epoch10 (1.0B, gated), open-unlearning/unlearn_tofu_Llama-3.2-1B-Instruct_forget10_SimNPO_lr5e-05_b4.5_a1_d1_g0.25_ep10 (1.0B, gated), open-unlearning/unlearn_tofu_Llama-3.2-1B-Instruct_forget10_IdkDPO_lr5e-05_beta0.05_alpha5_epoch10 (1.0B, gated)
- Estimated VRAM: 8 GB — bf16 inference/light-compression of a 1B-param Llama on TOFU forget10 eval; README explicitly states 'Requires an A100/A5000 (24 GB) GPU instance', the same VRAM class as an RTX 3090.
- Data: TOFU forget10 (via OpenUnlearning harness); availability: hf-hub
- Estimated runtime: hours (README: 'Run the full compression sweep -> results/sweep_results.csv (~2-3 hrs)'; baselines take less.)
- Stated compute in the repo: Requires an A100/A5000 (24 GB) GPU instance.
- Known blockers: Depends on an external harness (locuslab/open-unlearning) that must be cloned and installed separately -- not vendored in this repo; Llama-3.2-1B-Instruct and the pre-unlearned checkpoints are gated on HF (license acceptance needed)
- Inspector's notes: The repo itself has no requirements.txt/pyproject.toml -- its Python env comes entirely from the separately-cloned OpenUnlearning harness via 'bash setup.sh'. compress_model.py (prune/SVD) and the quantization flags are self-contained and easy to follow; no closed-API calls found.

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
