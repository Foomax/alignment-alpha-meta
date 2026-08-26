# Replicate: Can we teach a model to encode a semantic feature on a chosen manifold in just three channels?

Source post: `ZwEer94AefjdW4933` (2026-07-27, LW karma 5). Repo: `phusroyal/phu-bluedot_1st_puzzle` @ `27a8be7ed55fb4917065f7d84de567ccd3883914`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A five-layer MLP can be trained to encode a binary semantic feature (country) on a pre-chosen 3-channel nonlinear manifold (sphere shell or helix tube) such that the manifold is causally used by the classifier (causal delta rising from ~0.02-0.04 to 1.9-3.5, swap-test specificity ratios of 47-92) while becoming much harder to read as an ordinary linear direction (linear probe AUC falling from ~0.9998 to 0.57-0.67), though some leakage through complement channels remains.

Supporting quote from the post: "This experiment shows that a small MLP can encode a semantic feature through a pre-chosen nonlinear manifold in only three channels while preserving task performance."

**Headline metric:** Linear probe AUC on country feature / causal delta
**Claimed value:** linear probe AUC falls from 0.9996-0.9998 (ClassOT) to 0.57-0.67 (GFAL); causal delta rises from 0.02-0.04 to 1.9-3.5
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 8 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/predefined_manifold (run via `uv run python -m src.predefined_manifold run --device cuda`, i.e. src/predefined_manifold/__main__.py)` (confidence: high)
- Produces: geometries/<geometry>/stages/<stage>/metrics.json and runs/<run_id>/metrics.json under .artifacts/predefined_manifold, produced by `python -m src.predefined_manifold run` for Question 3 (sphere_shell / helix_tube geometries, classot vs gfal stages) -- these are exactly the linear-probe-AUC-drop and causal-delta numbers in the post.
- Models: sentence-transformers/all-MiniLM-L6-v2 (0.022B)
- Estimated VRAM: 2 GB — Frozen 22M-param MiniLM encoder producing 384-dim embeddings feeding a custom 5-layer MLP head (152KB model.pt); train/test sets are 7000/1500 short synthetic sentences (1.1MB/236KB jsonl). Everything here is orders of magnitude under 24GB even in fp32.
- Data: data/train.jsonl (in-repo, 7000 rows), data/test.jsonl (in-repo, 1500 rows); availability: in-repo
- Estimated runtime: minutes (README example commands all run with --device cpu by default; training schedule (src/predefined_manifold/training.py TrainSchedule) is base_epochs=14 plus per-geometry stages totaling ~118 more epochs over only 7000 rows with a tiny MLP -- this is CPU-fast, so on a 3090 it is trivial.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: This is the cleanest repo of the batch: fully self-contained (data, model, training pipeline, CLI, tests all included), pinned deps via uv.lock, and the README documents the exact commands and output paths for every stage of the claim (ClassOT baseline through GFAL/GFAL+ and causal-use validation). No GPU is even strictly required; a 3090 makes it faster still.

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
