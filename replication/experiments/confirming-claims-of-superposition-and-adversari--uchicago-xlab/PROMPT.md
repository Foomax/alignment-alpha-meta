# Replicate: Confirming Claims of Superposition and Adversarial Examples in Toy Models

Source post: `rwu73dCE3uWjieijK` (2026-08-01, LW karma 28). Repo: `uchicago-xlab/superposition-replication` @ `d4aa6b7c2c2b5242e30b429d992fa2afc98b2fc7`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> This work replicates all three core claims of Stevinson et al. (arXiv:2510.11709) in toy superposition classifiers: PGD adversarial attacks align with the theoretically optimal interference-exploiting perturbation, robustness falls monotonically as superposition (k/m) increases and rises to 97.3% when k=m, and adversarial attacks transfer between independently-trained models in proportion to how much their feature geometries converge under correlated input regimes; it additionally finds that co-activating features can collapse onto a shared direction rather than orthogonalizing when bottleneck capacity is limited.

Supporting quote from the post: "We reproduce all three core claims of Stevinson et al. from their toy classifier setting"

**Headline metric:** PGD-attack vs optimal-perturbation cosine similarity; robust accuracy vs k/m
**Claimed value:** PGD·optimal cosine similarity = 1.00 across tested k/m (vs paper's 0.92-0.97); robust accuracy at k=m rises to 97.3% (m=5), falling monotonically as k/m increases (e.g. k/m=4, m=5: 30.1% ours vs 33.5% paper)
**Direction of the claim:** +
**Uncertainty the post reported:** se
**Tolerance for "reproduced":** `manual` — headline is a compound of 9 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `synth/run.py` (confidence: high)
- Produces: results/h1_alignment.json (PGD-vs-optimal cosine similarity), results/h2_control.json (robust accuracy vs k/m), results/h3_transfer.json (geometry-transfer correlation), assembled into report.html
- Models: ? (3e-05B)
- Estimated VRAM: 1 GB — Two-layer linear bottleneck classifier (d<=90, m<=30, k<=90 in the largest swept config); parameter count in the low thousands. Config default device is 'cpu'; on GPU this is far under 1GB.
- Data: none listed; availability: in-repo
- Estimated runtime: minutes (Each config trains 20,000 steps of a tiny linear bottleneck net with no dataloader overhead; the full `python -m synth.run all` pipeline sweeps ~2-10 seeds across 8 experiment scripts (h1,h2,h3,pairpred,pairangle,ssweep,normeps,coupling) — order minutes to tens of minutes total on CPU alone, let alone a 3090.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Fully self-contained toy replication with one CLI entrypoint that runs every sub-experiment and builds the comparison report; the repo's own README already documents an instability in the paper's own H3 seed-sampling result (N=10 seeds) as a finding, not a repro blocker.

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
