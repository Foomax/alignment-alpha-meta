# Replicate: Proof-of-Concept Debugger for a Small LLM

Source post: `rxR5p9Qha937wTTBp` (2025-03-17, LW karma 27). Repo: `peterlai/gpt-circuits` @ `1cf99ec0580f33e19c37099b02d37a01b284ba5f`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A prototype LLM 'debugger' using SAE features and a new ablation technique ('cluster resampling') automates interpretable circuit visualization for arbitrary prompts on a small character-level toy GPT-2 model, producing smaller/sparser circuits (e.g. 20-41 features) than conventional zero-ablation (31-138 features) or resample-ablation (70-96 features) at a comparable or better KL divergence target.

Supporting quote from the post: "Cluster resampling produces the best results, followed by zero ablation, then distantly by conventional resampling."

**Headline metric:** number of SAE features per extracted circuit at KL divergence threshold 0.25
**Claimed value:** cluster resampling circuits contain fewer features (e.g. 20-41 across example sequences) than zero ablation (31-138) and conventional resampling (70-96)
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/circuits/comparisons.sh` (confidence: medium)
- Produces: experiments/circuits/comparisons.ipynb, aggregating checkpoints/<model>/ablation-comparisons/<circuit_name>/{cluster,zero,random,...}.json into the per-config feature-count numbers quoted in the post (20-41 cluster vs 31-138 zero vs 70-96 resample)
- Models: GPT-2 216k params (toy)
- Estimated VRAM: 2 GB — shakespeare_64x4 config: n_embd=64, n_layer=4, n_head=4, block_size=128, char-level ASCII vocab — a ~200K-parameter GPT-2 trained from scratch in-repo, trivial VRAM even with a JumpReLU SAE bottleneck attached; no VRAM figure is stated because a model this size doesn't need one
- Data: tiny Shakespeare char corpus; availability: in-repo
- Estimated runtime: hours (comparisons.sh loops over 100 validation sequences x 5 ablation configs (cluster-nopos/cluster/random-pos/random/zero) = 500 circuit-search runs via experiments.circuits.circuit; no checkpoints are committed, so training the toy GPT-2 and SAE must happen first (config/training time not stated but toy-scale))
- Stated compute in the repo: none
- Known blockers: no model or SAE checkpoints are committed — the full chain (train GPT-2 toy model, train JumpReLU SAE, run comparisons.sh, run comparisons.ipynb) must be run from scratch; requirements.txt has zero version pins (not even torch), so exact reproduction depends on whatever the latest versions resolve to today
- Inspector's notes: The model itself (toy char-level GPT-2, ~216K params per the post) is cheap to train; the real cost is procedural — no pre-baked checkpoint to skip straight to the comparison step, and a 500-run ablation sweep to reproduce the table.

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
