# Replicate: An Induction Head in Disguise: Chasing Grammar in a Character-Level Transformer

Source post: `x2ZdCoqAaLedpjDk3` (2026-07-10, LW karma -1). Repo: `ameya-bit/quotesbyniche` @ `135fa8933d67af546aec18f045831cb300fbdc73`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In a small character-level transformer trained on Nietzsche texts, a single attention head (Block 5 Head 0) is a copying/induction head whose OV circuit already encodes a latent bracket-completion mechanism (attending to '(' boosts the ')' logit by +0.556, attending to ')' suppresses '(' by -0.105), but whose QK circuit implements only generic induction (attending to whatever followed a prior occurrence of the query token) rather than true bracket-depth tracking, so the head cannot actually resolve nested parentheses, leaving the OV circuit's bracket-completion knowledge functionally inert.

Supporting quote from the post: "As we said initially, this is a copying head with an OV circuit that knows how to handle parentheses, but the QK circuit is blind to bracket structure, and thus can't utilize it properly."

**Headline metric:** copying score (OV circuit eigenvalue-based) and qualitative bracket-tracking behavior on hand-written test prompts
**Claimed value:** B5H0 copying score 0.615 vs next-highest head 0.35; OV circuit shows attending to '(' boosts ')' logit by +0.556 and attending to ')' suppresses '(' by -0.105, but the QK circuit fails to distinguish an already-closed bracket from a still-open one in nested test prompts, instead always attending to the most recent bracket
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `interp/niche_attention_analysis.ipynb` (confidence: high)
- Produces: interp/evidence.md (per-head copying scores, OV bracket-completion logit deltas) and interp/figures/fig2_spike_copying_score.*, fig1_make_ov_diagonal.*
- Models: ? (0.0049B)
- Estimated VRAM: 1 GB — 4.9M-param, 6-layer/4-head/d_model-256 char-level transformer; the interp notebook explicitly sets device='cpu' and only does forward passes + eigen-decompositions on a committed checkpoint. Negligible memory, no GPU required at all.
- Data: niche_model.pt (committed checkpoint, needed and included), Nietzsche corpus from Project Gutenberg (only needed to retrain from scratch, not to reproduce the interp analysis); availability: in-repo
- Estimated runtime: minutes (Notebook loads one small committed checkpoint and computes OV-circuit eigen-copying scores over 6x4=24 heads plus a handful of hand-written bracket-nesting test prompts on CPU — seconds to low minutes.)
- Stated compute in the repo: Training runs on CUDA -> MPS -> CPU (whichever is available)... On Apple Silicon (MPS) ~1000 steps takes ~2-2.5 minutes. (this describes the training notebook, not the interp entrypoint, which explicitly hardcodes device='cpu')
- Known blockers: none recorded
- Inspector's notes: Cleanest repo of the batch: the exact weights the writeup analyzes are committed (training is stochastic so a retrain would not reproduce the per-head findings), and the interp notebook is self-contained, CPU-only, with no external data downloads or API calls needed.

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
