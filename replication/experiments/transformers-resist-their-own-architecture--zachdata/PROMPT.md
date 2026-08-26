# Replicate: Transformers Resist Their Own Architecture

Source post: `2dA7phbYZGPjhTj9q` (2026-07-09, LW karma 11). Repo: `zachdata/metastablestateanalysis` @ `4e9471d69cec1ea826ded94351cbc38c32ea3e5b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Trained transformers (GPT-2 family, ALBERT, BERT) exhibit the token-clustering dynamics predicted by Geshkovski et al.'s mathematical theory of attention as an interacting particle system, but unlike randomly-initialized transformers (which show monotonically increasing energy and collapse toward a single point, matching the theory's identity-matrix prediction), trained models' weights learn to resist total collapse -- energy does not rise monotonically, effective rank and cluster counts stay higher, and clusters remain smaller, more numerous, and farther apart -- indicating trained transformers actively counteract the collapse dynamics built into their own architecture.

Supporting quote from the post: "The trained models maintain effective rank, preventing the collapse the architecture is driving. The random models have not learned to resist this collapse."

**Headline metric:** energy monotonicity, effective rank, and HDBSCAN cluster count across layers, trained vs random-weight models
**Claimed value:** random-weight models show monotonically increasing energy and collapse toward a point (e.g. ALBERT base reaches near-total collapse by ~layer 20, all pairwise inner products -> 1); trained models show non-monotonic energy and sustain effective rank near ~250 dimensions regardless of true dimensionality (700-1600) and ~50 HDBSCAN clusters per model
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `p1_mstate_tracking/run_1.py --models blog1 bert-large-uncased --random-baseline (blog1 = albert-base-v2, albert-xlarge-v2, bert-base-uncased, gpt2, gpt2-medium, gpt2-large, gpt2-xl; bert-large-uncased is a separate registry key not in the default blog1 group)` (confidence: medium)
- Produces: p1_mstate_tracking results/<timestamp>/ verdict tables and figures for effective rank / cluster count / energy monotonicity, referenced from status-1.md
- Models: gpt2 (0.124B), gpt2-medium (0.355B), gpt2-large (0.774B), gpt2-xl (1.5B), albert-base-v2 (0.012B), albert-xlarge-v2 (0.06B), bert-base-uncased (0.11B), bert-large-uncased (0.34B)
- Estimated VRAM: 8 GB — core/config.py sets MODEL_DTYPE='float32'; these are inference-only forward passes (activation extraction across layers) with the largest model being GPT-2 XL (1.5B, ~6GB in fp32) plus per-layer activation caching, no training/backward pass
- Data: text prompts (in-repo, referenced by p1_mstate_tracking/design-1.md); availability: in-repo
- Estimated runtime: hours (No explicit wall-clock stated; inferred from CPU-bound eigenspectrum/HDBSCAN post-processing over 8 small-to-medium models x multiple prompts x layers ('Blog 1' run))
- Stated compute in the repo: pyproject.toml comment: install torch from the CPU index because 'nothing in CI needs a GPU'; no GPU sizing is stated anywhere for the actual analysis runs
- Known blockers: The exact GPT-2/ALBERT/BERT comparison in the post is the project's superseded 'Blog 1' run (dated 2026-04-23 in status-1.md); the repo's current active work/default model selection has moved to Pythia checkpoints, and status-1.md explicitly notes some GPT-2-era findings are 'marked as not reproducing' under the newer Pythia analysis. Re-running blog1 models is still supported in code but is not what current development is validating.; 'hdbscan' python package is imported directly (p1_mstate_tracking/clustering.py, core/functional_distance.py) but is not listed in pyproject.toml or requirements/*.txt — an undeclared dependency that would need to be pip-installed manually; INDEX.md's own 'Referenced, not present' section documents multiple files (MATH.md, DESIGN_pythia_frames.md) cited by live code that do not exist in the repository, indicating some documentation/reproducibility debt
- Inspector's notes: Code for the exact post claim (GPT-2 family + ALBERT + BERT, trained vs random-weight) is still present and runnable via the 'blog1' model group despite the project's pivot to Pythia checkpoints as the new default focus; VRAM/compute needs are trivial (largest model 1.5B, inference-only, float32).

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
