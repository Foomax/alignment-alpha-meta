# Replicate: Matryoshka Sparse Autoencoders

Source post: `zbebxYCqsryPALh8C` (2024-12-14, LW karma 100). Repo: `noanabeshima/matryoshka-saes` @ `7b80f5fe36598f43f3181c5466a0365c7ce07807`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Matryoshka SAEs, trained with a sum of SAE losses computed on random prefixes of the latents, completely avoid the feature-absorption holes seen in vanilla SAEs on a toy model, and when trained on a 4-layer TinyStories language model achieve higher Mean Max Correlation with small reference-SAE features than vanilla SAEs at the same L0 (across most model locations), at the cost of a slightly worse Fraction of Variance Unexplained.

Supporting quote from the post: "My results demonstrate that Matryoshka SAEs reduce feature absorption while preserving abstract features."

**Headline metric:** Mean Max Correlation (MMC) with reference SAE latents; Fraction of Variance Unexplained (FVU)
**Claimed value:** Matryoshka SAEs have higher MMC than vanilla SAEs at the same L0 across most locations (exceptions: residual stream before first block, first attention-layer output); at fixed L0, Matryoshka has slightly worse FVU, comparable to a vanilla SAE ~0.4x its size
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `train_saes_on_toy.ipynb` (confidence: medium)
- Produces: figures/matryoshka_decoder_gt_cosine.png / vanilla_decoder_gt_cosine.png (toy-model cosine-similarity heatmaps showing presence/absence of feature-absorption holes)
- Models: ? (2e-05B)
- Estimated VRAM: 1 GB — Toy Matryoshka/vanilla SAE trained on synthetic tree-structured features (D_MODEL = tree.n_features, small); negligible GPU memory footprint.
- Data: tree.json synthetic feature-tree definition (in-repo), TinyStories-trained 4-layer LM, its activations, and a small reference SAE (not in repo); availability: in-repo
- Estimated runtime: minutes (train_saes_on_toy.ipynb trains a vanilla and a Matryoshka SAE side-by-side on a small synthetic tree-feature dataset; comparable toy SAE setups of this size train in well under an hour, CPU-feasible.)
- Stated compute in the repo: none
- Known blockers: No code in this repo trains or evaluates SAEs on the 4-layer TinyStories LM, computes Mean Max Correlation against a 'small reference SAE', or computes Fraction of Variance Unexplained on real LM activations. The entire second half of the primary claim (the TinyStories comparison, which is where the quantitative MMC/FVU headline numbers come from) has no entrypoint anywhere in the repo.
- Inspector's notes: The repo fully supports reproducing the toy-model half of the claim (no feature-absorption holes) via train_saes_on_toy.ipynb; the TinyStories LM / reference-SAE comparisons that back the MMC and FVU headline numbers have no corresponding code, data, or checkpoints here.

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
