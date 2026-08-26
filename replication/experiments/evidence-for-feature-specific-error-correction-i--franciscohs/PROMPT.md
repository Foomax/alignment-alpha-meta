# Replicate: Evidence for feature-specific error correction in LLMs

Source post: `uDrsffSLzWD6cDnTt` (2026-07-14, LW karma 25). Repo: `franciscohs/fsec-paper` @ `32f4f12b4ce95b424fa475234c9db8566556c20f`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> LLMs exhibit feature-specific error correction (FSEC): perturbing residual-stream activations along candidate feature directions (contrastive, MELBO, top-activating SAE latents) produces a stronger downstream response than perturbing along mixtures of those directions, measured as a superellipse exponent p>2 (mean ~2.3 for contrastive, ~2.2 for MELBO/SAE), while non-feature baseline directions (PCA, random, random-difference) give p~2; this replicates across six LLM families and a toy model with ground-truth features (where p=3-3.4), providing the first empirical evidence for computation-in-superposition's predicted error-correction mechanism.

Supporting quote from the post: "We measure $p \approx 2.3$ for contrastive directions and $p \approx 2.2$ for MELBO and SAE directions, against $p \approx 2$ for PCA, random, and random-difference controls."

**Headline metric:** superellipse exponent p for candidate feature directions vs non-feature baselines
**Claimed value:** contrastive directions: mean p=2.42, 95% CI [2.29, 2.62]; MELBO: mean p=2.21, 95% CI [2.01, 2.42]; top-activating SAE latents: mean p=2.28, 95% CI [2.14, 2.47]; PCA baseline: mean p=2.03, 95% CI [1.94, 2.12]; random-difference baseline: mean p=2.05, 95% CI [2.00, 2.10]; random baseline: mean p=2.03, 95% CI [2.00, 2.07]; toy model with ground-truth features: p=3-3.4
**Direction of the claim:** +
**Uncertainty the post reported:** ci
**Tolerance for "reproduced":** `manual` — headline is a compound of 26 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `python scripts/sweep_2d.py --target <model> --layer <L> (per-model/layer 2D iso-response sweep) -> python scripts/refit_thrfixed_all.py --exact (fit superellipse exponents) -> render_figures.sh (plots); figure-only reproduction from the bundled results/ cache needs no GPU at all` (confidence: high)
- Produces: results/fits/fits_<target>_L<layer>*.pkl (per-condition fitted superellipse exponents p), aggregated into the paper's Fig 4/6 direction-family beeswarm plots via scripts/plotting/
- Models: google/gemma-2-9b (9.2B, gated), Qwen/Qwen3-1.7B (1.7B), meta-llama/Llama-3.1-8B (8.0B, gated), mistralai/Mistral-7B-v0.3 (7.0B), CohereForAI/aya-expanse-8b (8.0B), 01-ai/Yi-1.5-9B (9.0B)
- Estimated VRAM: 20 GB — Inference-only forward passes (no training) on the largest model in the sweep (gemma-2-9b / yi-1.5-9b, ~9B params); bf16 weights ~18GB plus per-pair 2D grid activation buffers from src/model.py's forward_from_layer utilities -- tight but should fit a 24GB 3090, comfortably fits for the smaller models (Qwen3-1.7B) in the set
- Data: data/*.py contrastive prompt sets (14 semantic concepts, 10 languages, 9 programming languages), FineWeb (anchor activations); availability: in-repo
- Estimated runtime: days (README states ~36h total on a single 80GB H100 for the full 6-cross-model + 3-cross-layer + 7-ablation sweep; a 3090 is slower and has less headroom for the 9B models, so the full ablation grid plausibly runs multiple days rather than the ~1.5 days on H100. Note: refitting exponents from the bundled sweeps_2d/ cache (no GPU) takes only minutes, and re-plotting every paper figure from bundled results/ takes about a minute end-to-end.)
- Stated compute in the repo: "Wallclock guidance (single 80 GB H100, ~40 s/pair): Single 528-pair canonical run (one model, one layer): ~6 h. All 6 cross-model + 3 cross-layer Gemma + 7 ablation variants: ~36 h total."
- Known blockers: Full ablation-grid reproduction (36h on an H100) is a multi-day undertaking on a single 3090; the repo itself flags this as the slow path.; Gemma and Llama checkpoints are gated -- need a HUGGINGFACE_HUB_TOKEN with license acceptance (not a hard blocker, just friction).
- Inspector's notes: Exceptionally reproducibility-conscious repo: ships ~1.6GB of cached intermediate results (results/sweeps_2d/, ~13k files) so every paper figure regenerates in about a minute with no GPU at all, and separately documents exact wallclock cost to regenerate from raw model weights. The three-tier reproduction path (figures-only / refit-from-cache / full re-sweep) is the clearest compute-tiering seen across this batch.

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
