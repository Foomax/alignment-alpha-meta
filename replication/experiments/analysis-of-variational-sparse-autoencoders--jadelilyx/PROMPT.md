# Replicate: Analysis of Variational Sparse Autoencoders

Source post: `nPxdHt8k4bMuaC46M` (2025-08-23, LW karma 13). Repo: `jadelilyx/v-sae_mech-interp-spar2025` @ `42bb7b792074a717a6876f28e9193bb62f6a2d74`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Adding a KL-divergence variational term (vSAE) to a TopK sparse autoencoder does not improve interpretability and degrades reconstruction performance relative to a standard TopK SAE, primarily because the KL pressure kills a large fraction of features (e.g. only about half alive at k=256), though the vSAE shows somewhat improved robustness on spurious-correlation-removal and targeted-probe-perturbation metrics

Supporting quote from the post: "We ultimately find that this addition does not benefit the interpretability of the language model and degrades performance."

**Headline metric:** SAEBench quality metrics (KL divergence, cross-entropy loss, explained variance, cosine similarity) and fraction of living features, TopK vs. vSAE TopK
**Claimed value:** TopK consistently outperforms vSAE TopK on reconstruction/quality metrics across all K tested; vSAE has a low fraction of living features (e.g. only ~half alive at k=256); vSAE shows somewhat better Spurious Correlation Removal (SCR) and Targeted Probe Perturbation (TPP) robustness scores
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `train_sae_1lgelu.py (TopK baseline) and train_isovsae_1lgelu.py (vSAE) train the two dictionaries; no script in the repo computes the SAEBench SCR/TPP/living-features comparison itself` (confidence: low)
- Produces: SAEBench SCR/TPP/fraction-living-features comparison between TopK and vSAE TopK -- this table/figure is not produced by any script in this repository
- Models: gelu-1l (TransformerLens canonical toy model, not a standard HF repo) (0.03B)
- Estimated VRAM: 3 GB — gelu-1l is TransformerLens's 1-layer toy GELU model (a few million params); SAE dictionary size is 8x d_mlp with out_batch_size=1024 -- trivially small for a 24GB card.
- Data: NeelNanda/c4-tokenized-2b (HF hub, SAE training), NeelNanda/c4-code-20k (HF hub, visualization); availability: hf-hub
- Estimated runtime: hours (trainer_config['steps'] = 20000 in both train_isovsae_1lgelu.py and train_sae_1lgelu.py for a 1-layer toy model; no wall-clock figure stated, but should be fast given model size.)
- Stated compute in the repo: none
- Known blockers: The repo trains the two dictionaries (TopK, VSAE-Iso) but contains no SAEBench integration, no SCR/TPP evaluation code, and no living-features computation -- the headline metrics would require wiring up the separate SAEBench toolkit (github.com/adamkarvonen/SAEBench, not vendored here) by hand; requirements.txt is unpinned, and the checked-in pyproject.toml still identifies the package as the upstream 'dictionary-learning' fork (by Marks/Karvonen/Mueller) rather than this project, suggesting packaging wasn't fully adapted
- Inspector's notes: This is an internal SPAR-program writeup repo (the README says so explicitly). It provides working SAE/vSAE training code for a trivially small model that fits a 3090 easily, but the actual headline SAEBench quality-metric comparison in the post is not implemented anywhere in the repo -- reproducing the reported numbers (not just training some SAEs) would need substantial additional work outside what's checked in.

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
