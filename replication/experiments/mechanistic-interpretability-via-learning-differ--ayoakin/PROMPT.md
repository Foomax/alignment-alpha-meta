# Replicate: Mechanistic Interpretability Via Learning Differential Equations: AI Safety Camp Project Intermediate Report.

Source post: `qdxNsbY5kYNqcgzFb` (2025-05-08, LW karma 8). Repo: `ayoakin/mivlde` @ `36046d46cbf23995f72b7cd3e55db22d5dca1696`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Studying ODEFormer (an 86M-parameter transformer that infers symbolic ODEs from numerical trajectories) via probing, attention/logit lens, and SAEs, we find preliminary evidence that the encoder computes something resembling a numerical derivative (an attention head tracks high-derivative regions, and linear probes can predict the time-point of maximum derivative), but find no evidence that the model performs the hypothesized R^2-based comparison against candidate functions or infers eigenvalues for 2D linear systems.

Supporting quote from the post: "we observed a pattern similar to numerical computation of the input data derivative"

**Headline metric:** linear probe accuracy for derivative time-point, R^2 score, and eigenvalues from encoder/decoder activations
**Claimed value:** probes successfully predicted the time-point of maximum derivative but not its value; R^2-score probes performed poorly overall (best layer index 7, Spearman coefficient 0.75); eigenvalue-prediction probes performed worse than coefficient-prediction probes, evidence against the eigenvalue hypothesis
**Direction of the claim:** 0
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `subteams/LLMProbing/experiments/run_experiment.py` (confidence: medium)
- Produces: subteams/LLMProbing/notebooks/derivatives_exp.ipynb, r2_experiment.ipynb, and 2D_Linear.ipynb -- derivative-timepoint probe accuracy, R^2-score probe Spearman coefficient (0.75, layer 7), and eigenvalue-vs-coefficient probe comparison
- Models: odeformer (pip package, CompML/ODEFormer) (0.086B), huggingface/time-series-transformer (small) (NoneB)
- Estimated VRAM: 2 GB — 86M-parameter transformer; probing/activation-extraction and small linear/regression probes only, no fine-tuning of the base model. Would run fine on CPU too.
- Data: synthetic ODE trajectory / time-series data; availability: in-repo
- Estimated runtime: minutes (Not stated, but inferred from an 86M-parameter model plus linear probes on cached activations -- inherently cheap.)
- Stated compute in the repo: none
- Known blockers: subteams/LogitLens/ contains only a one-line empty README -- the logit-lens portion of the claim has no committed code; No single unified entrypoint; findings are spread across ~10 separate per-subteam notebooks (LLMProbing, SAEs, ActivationMaximization, SHAP) with only per-subteam requirements.txt files, no top-level one
- Inspector's notes: Compute is a non-issue (86M-param model, linear probes) -- this is a laptop-class experiment. Reproducibility of the probing sub-claims (derivative time-point, R^2, eigenvalues) is good; the SAE and especially logit-lens sub-investigations mentioned in the post are far less complete in the repo.

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
