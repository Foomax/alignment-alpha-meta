# Replicate: Weight-Sparse Circuits May Be Interpretable Yet Unfaithful

Source post: `sHpZZnRDLg7ccX9aF` (2026-02-09, LW karma 138). Repo: `jacobcd52/sparse_pretrain_public` @ `1c1da8695552ee8015f9ca4b96a3ccfd793a2d74`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Pruned circuits extracted from weight-sparse transformers via Gao et al's method can be small and appear interpretable while being unfaithful to the model's true computation, e.g. achieving low loss on a nonsense task, missing important attention patterns, repurposing nodes, and failing to generalize like the original model.

Supporting quote from the post: "Overall, these results suggest that circuits extracted from weight-sparse models, even when interpretable, should be scrutinized for faithfulness."

**Headline metric:** task CE loss / circuit node count
**Claimed value:** ~30 nodes achieve task loss < 0.05 on a nonsense task; ordinary pronoun task needs ~10 nodes for similar loss
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/pruning/run_pruning.py --model <HF repo, e.g. jacobcd52/ss_bridges_d1024_f0.015625> --task dummy_pronoun_iswhen (or similar nonsense/pronoun task variants under scripts/)` (confidence: medium)
- Produces: Node-count vs. task cross-entropy-loss curves per task (nonsense/pronoun), produced by src/pruning/run_pruning.py and aggregated by scripts like scripts/regenerate_pareto_plots.py
- Models: jacobcd52/ss_d128_f1 and related jacobcd52/ss_bridges_* checkpoints referenced in configs_bridges/ (0.4B)
- Estimated VRAM: 4 GB — Custom 2-layer transformer, d_model up to 4096 (~400M params at the largest configured size, configs_bridges/ss128/d4096.yaml); pretrained checkpoints are loadable directly from HuggingFace Hub repo IDs in run_pruning.py, so circuit-discovery/pruning analysis does not require rerunning the 2B-token pretraining.
- Data: SimpleStories pretraining data (HF hub: jacobcd52/simplestories-tokenized or SimpleStories/SimpleStories), synthetic pronoun/nonsense task prompts generated in code (src/pruning/tasks.py); availability: hf-hub
- Estimated runtime: hours (PruningConfig.num_steps defaults to 2000 optimization steps per task/model-size; several scripts (run_100_seeds_*.py) repeat pruning 100x per config for seed-robustness plots.)
- Stated compute in the repo: none
- Known blockers: No single canonical script maps directly onto the post's specific 'nonsense task ~30 nodes vs. pronoun task ~10 nodes' comparison -- would require identifying the right task name(s)/config among ~15 near-duplicate run_*.py scripts; If the specific pretrained checkpoint used in the post isn't the one hosted on HF, pretraining a sparse model from scratch is a 2B-token run per configs_bridges/ss128/*.yaml -- a much larger compute ask than the pruning step itself
- Inspector's notes: The underlying model and pruning method are tiny and clearly fit a 3090 with room to spare; the main friction is repo sprawl (~50 near-duplicate scripts) rather than compute. Whether the exact headline node counts require a specific pretrained checkpoint or a fresh 2B-token pretrain is not resolvable from the README alone.

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
