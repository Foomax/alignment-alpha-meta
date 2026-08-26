# Replicate: Mechanistic estimation for wide random MLPs

Source post: `fsG4m6sRMpomd7Rk6` (2026-05-07, LW karma 85). Repo: `alignment-research-center/mlp_cumulant_propagation` @ `93d091a4c26c042bfffa28f2e76a81bc0aba94bb`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A new mechanistic ('cumulant propagation') algorithm for estimating the expected output of wide random-initialization MLPs under Gaussian input outperforms Monte Carlo sampling both in theory (mean squared error O(epsilon^2) in time O(n/epsilon^2) vs. Theta(n^2/epsilon^2) for sampling) and in practice, achieving equal MSE with under 1/100th the FLOPs on 4-hidden-layer width-256 ReLU MLPs, and extends to low-probability estimation and a proof-of-concept 'mechanistic distillation' training loss.

Supporting quote from the post: "For ReLU MLPs with 4 hidden layers and width 256, our best algorithms outperform Monte Carlo sampling at FLOP budgets spanning 7 orders of magnitude, in some cases achieving the same mean squared error using fewer than 1/100 as many FLOPs."

**Headline metric:** mean squared error vs. FLOPs for estimating expected output; relative error at low probability
**Claimed value:** outperforms Monte Carlo sampling across 7 orders of magnitude of FLOP budget, in some cases matching MSE with <1/100 the FLOPs; achieves under 30% relative error for probabilities 100x lower than 1/N using similar FLOPs to N-sample Monte Carlo
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/kprop_by_width.py` (confidence: high)
- Produces: plots/mse_vs_flops_main_relu.pdf (MSE vs FLOPs, kprop vs Monte Carlo sampling)
- Models: ? (0.001B)
- Estimated VRAM: 18 GB — kprop_by_width.py hardcodes SAMPLES=2**34 (~17B) and BATCH_SIZE=2**19 for its Monte Carlo ground-truth baseline; at width n=256 the returned (pre, act) tensors are each shaped (524288, num_layers, 256) float32, ~8.6GB apiece (~17GB combined) for a single minibatch of the ground-truth sampling step alone. Tight against a 24GB card, though batch_size is a tunable knob that trades VRAM for more (still cheap) minibatches.
- Data: none listed; availability: in-repo
- Estimated runtime: days (SAMPLES=2**34 Monte Carlo ground-truth samples per (width, trial, config); the default sweep is ALL_WIDTHS=(8..256) x trials=5 x 4 augment/avg_metric combos x k_maxs=range(5), repeated per nonlinearity (relu/sigmoid/gelu/tanh + critical variants). The comparison is against sampling specifically because sampling is expensive by design, so generating the ground-truth baseline used for the headline plots is the actual heavy cost; the kprop estimator itself is cheap.)
- Stated compute in the repo: none
- Known blockers: Reproducing the full 7-orders-of-magnitude FLOP-budget comparison at the repo's hardcoded SAMPLES=2**34 ground-truth scale, across the full width/trial/nonlinearity sweep, is a multi-day job on one GPU. A reduced-scale run (fewer widths, smaller SAMPLES, single trial) would validate the algorithm's qualitative behavior but would not reproduce the exact headline MSE/FLOPs numbers.
- Inspector's notes: The mechanistic estimator (mlp_kprop) itself is cheap and the model is tiny; nearly all runtime and VRAM pressure comes from generating a sufficiently low-variance Monte Carlo ground truth to compare against, which the default experiment configs bake in at very large sample counts.

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
