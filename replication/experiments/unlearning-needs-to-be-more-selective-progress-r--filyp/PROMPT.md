# Replicate: Unlearning Needs to be More Selective [Progress Report]

Source post: `QYzofMbzmbgiwfqy8` (2025-06-27, LW karma 24). Repo: `filyp/mudman` @ `227eaea432b10243be8196de902293e51ddd6a59`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> MUDMAN, which combines a selective update rule (Disruption Masking) with MAML-based meta-learning, outperforms the current state-of-the-art unlearning method TAR by 40% in robustness to fine-tuning attacks.

Supporting quote from the post: "Our method (MUDMAN) which combines these insights, outperforms the current state-of-the-art unlearning method (TAR) by 40%."

**Headline metric:** attack-robustness improvement over TAR
**Claimed value:** 40%
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/study_runner.py --config-path "configs/ablations_and_loss2,llama32,pile-bio.yaml"` (confidence: high)
- Produces: Figure 'Ablation study of MUDMAN' (built by src/plotting/ablations_and_loss.py) from the ablations_and_loss2,{model},{dataset}.yaml runs, whose TAR2 variant is the TAR baseline compared against MUDMAN for the 40% claim
- Models: meta-llama/Llama-3.2-1B (1.0B, gated), HuggingFaceTB/SmolLM-135M (0.135B), EleutherAI/pythia-14m (0.014B)
- Estimated VRAM: 4 GB — Llama-3.2-1B fine-tuning with PEFT/LoRA-scale updates, batch_size 16, plus a MAML adversary copy of the model -- comfortably fits 24GB; SmolLM-135M and Pythia-14M are trivial.
- Data: pile_bio_retain/forget corpora; availability: download-script
- Estimated runtime: days (README states ~35h (5*7h) on an L40 for just the Llama-3.2-1B/pile-bio yaml (which contains the TAR2 variant behind the 40% claim); reproducing the full 'Ablation study of MUDMAN' figure needs 6 such yaml configs (2 datasets x 3 models). A 3090 is roughly comparable in throughput to an L40 for this workload, so similar order of magnitude.)
- Stated compute in the repo: On an Nvidia L40 GPU, experiments for one Llama-3.2-1B yaml should take around 5*7h (5 methods inside), for SmolLM-135M 5*9h, and for pythia-14m 5*4h. ... On an Nvidia L40 GPU, [wmdp7.yaml] should take around 5*24h. (Note that this experiment only supports remote runs.)
- Known blockers: 500-trial Optuna hyperparameter search per variant/yaml makes wall-clock very long (tens of hours) even though VRAM is not a constraint; Full ablation figure needs 6 separate yaml configs across 2 datasets x 3 models; The separate 'Accuracy on WMDP-Bio' figure (configs/wmdp7.yaml) is explicitly remote-only per README and needs ~120h on an L40 -- not something a solo 3090 could run in reasonable time
- Inspector's notes: The specific TAR-vs-MUDMAN 40% robustness claim is reproducible on a single GPU (Llama-3.2-1B, SmolLM-135M, Pythia-14M all fit easily), but at very long wall-clock time (tens of hours per config) due to the 500-trial Optuna search, not VRAM. Training/eval data is fetched from a public GitHub raw URL (a static, pre-generated corpus), not the closed API originally used to generate it.

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
