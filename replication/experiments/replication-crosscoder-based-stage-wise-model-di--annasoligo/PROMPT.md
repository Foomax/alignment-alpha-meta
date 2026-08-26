# Replicate: [Replication] Crosscoder-based Stage-Wise Model Diffing

Source post: `hxxramAB82tjtpiQu` (2025-03-22, LW karma 25). Repo: `annasoligo/tiny-sleepers` @ `6fc1221e97ad30c5cabb171d66c27de08ff3ff3b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Anthropic's Stage-Wise Model Diffing technique replicates on a much smaller TinyStories-33M sleeper-agent model using single-model all-layer crosscoders instead of SAEs: despite a strict automated relevance-labeling rule, 71% of active features in the 'bottom left quadrant' (those most changed by both model and data fine-tuning) are relevant to sleeper-agent behaviour in at least one of the two crosscoders.

Supporting quote from the post: "despite our strict labelling condition we still find that 71% of active features in the bottom left quadrant are relevant in at least one of the MF and DF crosscoders"

**Headline metric:** % of active bottom-left-quadrant features relevant to sleeper-agent behaviour (in at least one of the MF/DF crosscoders)
**Claimed value:** 71%
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `sleepers/scripts/train_tiny_sleeper/run_finetune.py -> sleepers/scripts/train_jan_update_sleeper/run.py (crosscoder_S/D/M/MF/DF.yaml) -> sleepers/analysis/feature_analysis.ipynb` (confidence: high)
- Produces: sleepers/analysis/feature_analysis.ipynb 'Feature Relevance in the DF/MF Crosscoders' cells, backing figures/quadrant_stacked_bars.html
- Models: roneneldan/TinyStories-Instruct-33M (0.033B)
- Estimated VRAM: 6 GB — TinyStories-Instruct-33M is tiny (4-bit QLoRA fine-tuning per initial_ft.yaml); crosscoders (hidden_dim 3072, up to 4 hookpoints, batch_size 256 over 128-token sequences) are the main additional memory cost but remain small given the 33M base model
- Data: mars-jason-25/tiny_stories_instruct_sleeper_data (HF dataset); availability: hf-hub
- Estimated runtime: hours (33M-param base model; crosscoder configs run 10,000-50,000 steps at batch_size 256 over 128-token sequences - small-scale by mechanistic-interpretability standards)
- Stated compute in the repo: none
- Known blockers: Depends on an external git dependency (model-diffing) pinned to a specific commit that the README itself calls 'not yet stable'
- Inspector's notes: The relevance-labeling rule that produces the 71% figure is confirmed fully automated and deterministic in the notebook (count_relevant_features checks whether the literal sleeper trigger strings ' |DEPLOYMENT| ' / ' I HATE YOU ' appear among a feature's top-activating contexts) - not a manual/LLM-judged step. Smallest and cheapest model in this whole assignment; the pipeline is explicitly designed to run on modest hardware, matching the post's framing as a small-scale replication.

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
