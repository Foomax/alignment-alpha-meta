# Replicate: The Self-Hating Attention Head: A Deep Dive in GPT-2

Source post: `wxPvdBwWeaneAsWRB` (2025-07-04, LW karma 12). Repo: `mamiglia/deep-dive-l1h5` @ `6c45e47dbb0dc63b5a62ba7eb5bec3d152a6bdb8`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> GPT2-small's attention head L1H5 attends to semantically similar tokens while actively suppressing self-attention, a mechanism driven by negative eigenvalues in the symmetric part of its QK circuit, and this self-suppression can be causally steered by scaling those negative eigenvalues.

Supporting quote from the post: "gpt2-small's head L1H5 directs attention to semantically similar tokens and actively suppresses self-attention."

**Headline metric:** negative eigenvalues in the symmetric QK matrix W_sym
**Claimed value:** 33 of 64 eigenvalues negative
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `skew_analysis.py (symmetric/skew-symmetric decomposition of L1H5's W_QK, eigenvalue sign count)` (confidence: high)
- Produces: Eigenvalue-sign plot/printout from decomposing W_sym (symmetric part of L1H5's QK circuit) -- '33 of 64 eigenvalues negative'
- Models: gpt2 (gpt2-small) (0.124B)
- Estimated VRAM: 2 GB — GPT2-small (124M) plus a 768x768 eigendecomposition of one head's QK circuit -- negligible.
- Data: GPT2 vocabulary / hand-picked token groups (GROUP_TOKENS constant); availability: in-repo
- Estimated runtime: minutes (Single small model, vocabulary-sized matrix ops, no training and no large corpus.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: requirements.txt lists package names only (unpinned versions). Otherwise a clean, self-contained, small-GPU repo with no external data or model-gating issues; no closed-API usage found.

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
