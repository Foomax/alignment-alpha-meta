# Replicate: Activation Plateaus: Where and How They Emerge

Source post: `WMfSbt7AAcJdHzysB` (2025-10-17, LW karma 41). Repo: `mshinkle/activation_plateau_mechanisms` @ `4222c3efb77fe7983676cf96b3254dc000e8a0bc`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Activation plateaus in GPT-2 Large emerge and sharpen gradually across layers, are produced specifically by MLP blocks rather than attention blocks, persist without LayerNorm, and correspond to areas of high MLP input-output Jacobian sensitivity at their boundaries.

Supporting quote from the post: "activation plateaus emerge and sharpen gradually across model layers, with later layers having a slightly weaker—but similar—effect."

**Headline metric:** relative (L2) distance of model outputs across activation-space interpolation, and component-freezing effect on plateau formation
**Claimed value:** freezing MLP block outputs completely eliminates plateaus; freezing attention block outputs has relatively small effect
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `full_experiment.sh (runs scripts/interpolate_and_record_activations.py plain / --freeze_attention / --freeze_mlp, then all scripts/*_plots.py and jacobians_*.py)` (confidence: high)
- Produces: plots/ directory: step-size, relative-distance, and Jacobian plots comparing normal vs. attention-frozen vs. MLP-frozen interpolation runs (the 'freezing MLP eliminates plateaus, freezing attention does not' result)
- Models: gpt2-large (0.774B)
- Estimated VRAM: 3 GB — gpt2-large (774M params) loaded via transformer_lens HookedTransformer for SLERP interpolation between token-pair activations plus per-component Jacobian computation — small model, activation-only/per-layer-Jacobian memory footprint, comfortably under 24GB.
- Data: none — uses a single hardcoded shared_context prompt ('The house was') and two hardcoded token pairs from config.yaml; availability: in-repo
- Estimated runtime: minutes (n_steps=50 interpolation steps x 2 token pairs x 3 freeze-mode variants (normal / attention-frozen / MLP-frozen) on a 774M model, plus several Jacobian/plotting scripts — no gradient-based training, should complete well under an hour on a single GPU.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Cleanest and cheapest repo in this batch: small pretrained model, fully pinned dependencies (exact versions incl. CUDA build tags), no external data, and a single shell script (full_experiment.sh) reproduces the entire pipeline exactly as configured in config.yaml (model_name: gpt2-large).

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
