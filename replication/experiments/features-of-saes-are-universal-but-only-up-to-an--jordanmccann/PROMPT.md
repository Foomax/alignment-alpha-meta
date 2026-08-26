# Replicate: Features of SAEs are universal - but only up to an unknown random rotation

Source post: `JZK2xkedJwA7njKmN` (2026-05-31, LW karma 9). Repo: `jordanmccann/polymorphism-is-rotation` @ `483a40a92f5aace73aff7d7041a34726e974aa79`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Independently trained sibling transformers compute the same function but their residual-stream activation bases differ by a rotation statistically indistinguishable from a uniform (Haar) draw on SO(d): applying one seed's SAE to another seed's activations catastrophically fails (negative explained variance) despite high (~0.9) decoder-column cosine similarity, while a single orthogonal Procrustes rotation restores reconstruction to 0.85-0.99 EV with no retraining.

Supporting quote from the post: "Reconstruction score drops to negative explained variance - worse than ignoring the input entirely and predicting the mean activation."

**Headline metric:** post-rotation SAE reconstruction explained variance (EV)
**Claimed value:** 0.976-0.990 on toy model (vs worst-case -6.56 pre-rotation); 0.85-0.99 on Pythia-70m (vs -2.11 to 0.75 pre-rotation)
**Direction of the claim:** +
**Uncertainty the post reported:** seeds
**Tolerance for "reproduced":** `manual` — headline is a compound of 8 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `python -m replicate run-fast (replicate/run_fast.py; e.g. polymorphism.experiments.scale.pythia_panel_c_fast and polymorphism.experiments.scale.eigenvalue_spectrum for the Pythia-70m headline numbers)` (confidence: high)
- Produces: docs/PAPER_NUMBERS.md 'Section 8.3 — Pythia rotation audit (the headline)' table -> artifacts/scale/pythia_rotation/panel_c_fast.json (post-rotation EV 0.85-0.99) and artifacts/scale/pythia_rotation/eigenvalue_spectrum.json (KS stat/p vs Haar SO(d))
- Models: EleutherAI/pythia-70m (0.07B), toy 2-layer ReLU transformer, 104k params (custom-trained, not on HF) (0.0001B)
- Estimated VRAM: 4 GB — README's own troubleshooting section documents the OOM-mitigation path (batch size 256 sequences x 256 tokens by default) and states everything runs comfortably on an RTX 2060 (6GB), which is far below a 3090's 24GB.
- Data: Pythia-70m residual activations across 9 seeds x 7 sites, trained SAEs, Cohort A/B trained models -- downloadable via `python -m replicate fetch-artifacts` from HF dataset Jordanfmccann/polymorphism-is-rotation; availability: hf-hub
- Estimated runtime: minutes (Explicitly stated: run-fast (13 analysis steps, using pre-fetched ~11GB cached artifacts) takes ~30 minutes on an RTX 2060; full retrain from public weights takes ~14 hours on the same card.)
- Stated compute in the repo: Total time on RTX 2060: ~30 minutes (run-fast, cached artifacts); Total ~14 h on an RTX 2060 (run-full, retrain from scratch)
- Known blockers: none recorded
- Inspector's notes: Best-documented repo in this batch: a docs/PAPER_NUMBERS.md maps every paper number to its exact producer script and output JSON path, a `python -m replicate verify` command checks reproduced numbers against tolerances automatically, and stated compute (RTX 2060, ~30 min fast-path / ~14h full retrain) is well under a 3090's budget with margin to spare. No closed-API usage anywhere in the codebase.

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
