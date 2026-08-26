# Replicate: What is the functional role of SAE errors?

Source post: `WzHPpMz2kRongsA7q` (2025-06-20, LW karma 12). Repo: `ambitious-mechinterp/sfc-errors` @ `38b10a17077c99dadac190ae9120c052d9ed8a8b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In a sparse feature circuit for subject-verb agreement in Gemma-2 2B, ablating residual SAE error nodes destroys circuit faithfulness (down to 0.13), but this effect can be completely mitigated by restoring a narrow group (as few as 3, up to ~25) of late-mid-layer (16-21) SAE features, consistent with the hypothesis that SAE error terms partly encode intermediate feature representations arising from cross-layer superposition, though this does not explain all error-node functionality.

Supporting quote from the post: "we found that this effect can be completely mitigated by restoring a narrow group of late-mid SAE features."

**Headline metric:** faithfulness score (circuit performance recovery relative to full model)
**Claimed value:** ablating all residual error nodes: faithfulness 0.13; restoring top-25 features from layers 18-19: faithfulness 0.6-0.9; restoring as few as 3 features from layers 16-21: faithfulness fully restored (up to ~1.0 under zero ablation)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 10 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `notebooks/main/compute_mean_activations.ipynb -> notebooks/main/ablation_restoration_main.ipynb (evaluate_circuit_faithfulness.ipynb validates against the original SFC paper first)` (confidence: high)
- Produces: faithfulness curves from ablation_restoration_main.ipynb (residual-error-node ablation vs. top-K SAE-feature restoration by layer), replicating Figure-3-style faithfulness plots
- Models: google/gemma-2-2b (2.61B, gated)
- Estimated VRAM: 10 GB — gemma-2-2b loaded explicitly in bf16 (dtype=torch.bfloat16) via HookedSAETransformer.from_pretrained in every main notebook; multiple Gemma-Scope-2b canonical SAEs (resid/attn/mlp) are attached simultaneously with attribution-patching activation+gradient caching, but the base model is small enough that this stays well under 24GB.
- Data: data/rc_test_confident_model.json, rc_train_processed.csv, rc_test_processed.csv (all shipped in-repo); availability: in-repo
- Estimated runtime: hours (No runtime stated; AtP-score computation at batch_size=256 plus several ablation/restoration sweeps over a ~2.6B-param model with multiple attached SAEs is plausibly a multi-hour, single-GPU job.)
- Stated compute in the repo: none
- Known blockers: gemma-2-2b and Gemma-Scope SAEs are gated on HF Hub (license acceptance required); Notebooks hardcode multi-GPU device indices from the authors' workstation (caching_device='cuda:2', GPU_TO_USE=3) — a trivial one-line edit for a single-GPU 3090, not a real blocker
- Inspector's notes: The best-documented repo in this batch: explicit reproduction order in the README, all data shipped in-repo, exact model size/dtype stated in every notebook. Only friction is hardcoded multi-GPU indices left over from the original setup.

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
