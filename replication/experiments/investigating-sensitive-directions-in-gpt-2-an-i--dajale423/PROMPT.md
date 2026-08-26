# Replicate: Investigating Sensitive Directions in GPT-2: An Improved Baseline and Comparative Analysis of SAEs

Source post: `dS5dSgwaDQRoWdTuu` (2024-09-06, LW karma 28). Repo: `dajale423/error_pathology` @ `a963531eaf1752c57bc6d6f9384a73136d4ab471`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Using an improved 'mixture' sensitive-direction baseline that excludes the original activation, GPT2-small's SAE reconstruction errors are no longer pathologically higher in KL divergence than the baseline (as previously reported by Gurnee 2024), though variability remains across layers, and SAE feature directions' impact on model output depends on SAE type and L0, with end-to-end SAE features showing no greater influence on model output than traditional SAE features.

Supporting quote from the post: "SAE errors are no longer pathologically large when compared to more realistic baselines."

**Headline metric:** KL divergence of next-token predictions under SAE(x) reconstruction vs cov-random/real 'mixture' baseline directions
**Claimed value:** SAE(x) KL comparable to cov-random-mixture baseline at Layer 6, variable across layers
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/sensitive_direction.py` (confidence: medium)
- Produces: KL divergence of SAE(x) reconstructions vs. 'mixture' baseline directions, produced by scripts/sensitive_direction.py and plotted in notebooks/plotting/proper_baseline.ipynb / sensitive_directions.ipynb
- Models: openai-community/gpt2 (loaded via transformer_lens as 'gpt2-small') (0.124B)
- Estimated VRAM: 4 GB — GPT2-small (124M) forward pass with hooked SAE reconstruction/perturbation over a pre-tokenized tensor; SLURM job only requests 30GB system RAM, not VRAM, and no VRAM figure is stated
- Data: token_tensor.pt (included in repo, 16MB, pre-tokenized), e2e SAE checkpoint pulled from wandb artifact 'sparsify/gpt2/h9hrelni', traditional SAEs via hf_hub_download; availability: download-script
- Estimated runtime: minutes (run_sensitive_directions.sh requests only 1 hour of SLURM wallclock for a single-layer run)
- Stated compute in the repo: run_sensitive_directions.sh: '#SBATCH -c 2', '#SBATCH -t 0-1:00', '#SBATCH -p gpu_requeue', '#SBATCH --gres=gpu:1', '#SBATCH --mem=30G' (no GPU model named)
- Known blockers: the exact --direction_type/--subtraction flag combination that reproduces the post's 'cov-random-mixture' baseline isn't spelled out as a single ready-to-run command (run_sensitive_directions.sh only has one example, plus commented-out variants); sensitive_direction.py hardcodes args.e2e = 'h9hrelni', so every run pulls a specific end-to-end SAE checkpoint from a wandb artifact path rather than a stable public registry
- Inspector's notes: Very lightweight compute (single GPU-hour SLURM job on GPT2-small); the practical friction is entirely about which flag combination and which of several notebooks reproduce the exact headline figure, not hardware.

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
