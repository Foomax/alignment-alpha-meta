# Replicate: AntiPaSTO: Self-Supervised Honesty Steering via Anti-Parallel Representations

Source post: `nWiwv4GN8aYqpnZKE` (2026-01-13, LW karma 6). Repo: `wassname/antipasto` @ `5e0f8517f360751220bf0348586952ff0e240907`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> AntiPaSTO, a gradient-optimized self-supervised steering method trained only on two contrastive words, achieves a Steering F1 of 31.2 on Gemma-3-1B for honesty steering on out-of-distribution moral dilemmas, versus 4.5 for prompting and 0.0 for arithmetic mean-difference steering (ActAdd/RepEng).

Supporting quote from the post: "AntiPaSTO on Gemma 3 1B achieves a Steering F1 of 31.2, beating the prompting baseline of 4.5."

**Headline metric:** Steering F1
**Claimed value:** 31.2±5.3 (AntiPaSTO) vs 13.0 (engineered prompting) vs 4.5 (prompting) vs 0.0 (RepEng/ActAdd mean-diff)
**Direction of the claim:** +
**Uncertainty the post reported:** seeds
**Tolerance for "reproduced":** `manual` — headline is a compound of 5 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `nbs/train.py gemma1b-24gb (training) + nbs/eval_baseline_prompting.py / nbs/eval_baseline_repeng.py (baselines) -> antipasto/eval.py + antipasto/metrics.py (Steering F1 table)` (confidence: high)
- Produces: README Results table (Steer F1 by method) reproduced by antipasto/metrics.py::compute_steering_f1, called from antipasto/train/daily_dilemas.py and the nbs/eval_baseline_*.py scripts
- Models: google/gemma-3-1b-it (1.0B, gated)
- Estimated VRAM: 8 GB — Repo ships a named config preset explicitly targeting a 24GB GPU for exactly this model ('gemma1b-24gb' in antipasto/config.py); a 1B model in bf16/4bit uses only a few GB, well inside a 3090
- Data: 800 synthetic honesty contrast pairs (self-generated), kellycyy/daily_dilemmas (HF dataset, 1360 dilemmas); availability: hf-hub
- Estimated runtime: minutes (README states training takes ~1 hour on Gemma-3-1B; evaluation on DailyDilemmas (1360 dilemmas x n=3 seeds) is inference-only on a 1B model, plausibly well under an hour.)
- Stated compute in the repo: README: 'Train a single adapter (~1 hour on Gemma-3-1B).' pyproject/config.py has a named preset 'gemma1b-24gb': 'Gemma 3 1B on 24GB GPU'.
- Known blockers: none recorded
- Inspector's notes: Cleanest repo in this batch: the repo literally ships a config preset named for a 24GB GPU running exactly the headline model (Gemma-3-1B). One historical use of GPT-4o-mini (nbs/eval_baseline_prompting_engineered.py) only generated a fixed prompt string once, back in 2024 -- that text is now hardcoded in the repo, so no live API call is needed to reproduce the table.

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
