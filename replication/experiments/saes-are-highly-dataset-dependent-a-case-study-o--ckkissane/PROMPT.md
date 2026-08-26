# Replicate: SAEs are highly dataset dependent: a case study on the refusal direction

Source post: `rtp6n7Z23uJpEH7od` (2024-11-07, LW karma 67). Repo: `ckkissane/sae-dataset-dependence` @ `2c991ba0cfa8d76a3e50ffd6b4fbc156052a6b64`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> An SAE trained on a chat-specific dataset (LmSys-Chat-1M) finds a significantly sparser, more faithful, and more interpretable reconstruction of the 'refusal direction' than an SAE trained on the Pile, and for this task the training dataset matters more than whether the SAE is trained on base vs. chat model activations

Supporting quote from the post: "Training a new SAE on a chat-specific dataset, LmSys-Chat-1M, finds a significantly sparser, more faithful, and interpretable reconstruction of the "refusal direction"."

**Headline metric:** cosine similarity between reconstructed and true refusal direction
**Claimed value:** LmSys-trained SAE reconstruction has significantly higher cosine similarity to the true refusal direction than the Pile-trained SAE (also achieves lower relative MSE and requires far fewer latents for equivalent reconstruction quality)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `refusal_dir_recons_fidelity_evals.py` (confidence: high)
- Produces: cosine similarity between each SAE's reconstruction and the true refusal direction, computed per-SAE in refusal_dir_recons_fidelity_evals.py
- Models: Qwen/Qwen1.5-0.5B-Chat (0.5B), Qwen/Qwen1.5-0.5B (0.5B)
- Estimated VRAM: 3 GB — Qwen1.5-0.5B (500M params) forward passes over 64 harmful + 64 harmless instructions plus small (32768-latent) SAE reconstructions on layer-13 residual activations; no training in this script
- Data: llm-attacks/harmful_behaviors.csv (raw GitHub download), harmless-instructions HF dataset, 4 pretrained SAEs as wandb artifacts under ckkissane/qwen-500M-*; availability: download-script
- Estimated runtime: minutes (single forward pass over ~128 short instructions through a 500M-param model plus loading 2 small SAEs; no training performed in this specific script)
- Stated compute in the repo: none
- Known blockers: no requirements.txt / pyproject.toml / setup.py anywhere in the repo, so exact sae_lens/transformer_lens/sae_dashboard versions are unstated and unpinned; the 4 pretrained SAEs are hosted only as wandb artifacts under specific project names (e.g. 'ckkissane/qwen-500M-chat-lmsys-1m-anthropic'), not a stable public model registry, so reproducing depends on those wandb projects staying public/reachable
- Inspector's notes: Despite having zero pinned dependencies, the actual compute footprint (500M-param model, small SAEs, a few hundred short instructions) is trivial; the real barrier is environment/artifact-access friction rather than hardware.

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
