# Replicate: Harmfulness Directions in OLMo

Source post: `nKfmimhTKCsDM2Hwh` (2026-06-09, LW karma 33). Repo: `harmfulness-exploration/harmfulness_direction_entanglement` @ `9bb700e7a9df67ca94cd8bfa8732aafe5b874ed1`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Across 39 OLMo-3-7B training checkpoints, harmfulness subcategories do not converge into a single unified direction but occupy a structured, entangled geometric space that forms mostly early in training; in-distribution AUROC for linear harmfulness probes is often misleadingly high (even near initialization) due to superficial lexical and structural cues rather than learned semantic structure; and directions only become stable, transferable, and effective as steering vectors from mid-to-late pretraining onward, with post-training checkpoints steering the Instruct model far more effectively than pretraining-derived directions.

Supporting quote from the post: "Harmfulness subcategories do not converge to a single direction, but instead occupy a shared yet structured geometric space."

**Headline metric:** AUROC of general-harmfulness direction under a random-label control (20 repeated label-randomizations)
**Claimed value:** mean AUROC 0.5120 (chance level)
**Direction of the claim:** 0
**Uncertainty the post reported:** seeds
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported spread

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/run_random_labels_20.sh (loops scripts/main_extraction_random_labels.py -> src/main_extraction_random_labels.run_extraction_random_labels, config config/main_extraction/1/drug_abuse.json) + scripts/aggregate_random_labels.py` (confidence: high)
- Produces: results/random_labels_runs/drug_abuse/run_*/results.json -> train_auroc_random_labels, aggregated by scripts/aggregate_random_labels.py into the reported mean AUROC 0.5120 under 20 label-randomizations
- Models: allenai/OLMo-3-1025-7B (7.0B), allenai/Olmo-3-7B-Instruct-SFT (7.0B), allenai/Olmo-3-7B-Instruct-DPO (7.0B), allenai/Olmo-3-7B-Instruct (7.0B)
- Estimated VRAM: 18 GB — 7B model, dtype='auto' (bf16) full load to CUDA, single-layer (layer 15) last-token residual hook only, batch_size 16 -- weights ~14GB + small activation buffer; comfortably under 24GB
- Data: datasets/safe/1/drug_abuse_weapons_banned_substance (train/test csv), datasets/drug_abuse_weapons_banned_substance/1 (train/test csv); availability: in-repo
- Estimated runtime: days (Not compute-bound but bandwidth-bound: hf_utils.load_model() shutil.rmtree()s and force-redownloads the full checkpoint on every single load, and the random-labels script deletes the local copy again after every checkpoint. The drug_abuse config lists 39 checkpoints x 20 repeated runs = 780 fresh 7B-model downloads (~14GB each, ~11TB total transfer) with no caching across runs -- this dominates wall-clock far more than the GPU forward passes do.)
- Stated compute in the repo: none
- Known blockers: Model cache is deliberately wiped and redownloaded per checkpoint per run (no caching), turning a 39-checkpoint x 20-run sweep into ~11TB of redundant HF downloads -- the practical blocker is network time/bandwidth, not VRAM or disk (disk footprint stays ~15GB at a time since old copies are deleted).; Only the drug_abuse category has the automated 20-run random-labels script; other subcategories seen in centroids/ would need the same driver adapted (straightforward, not a hard blocker).
- Inspector's notes: Very clean, well-organized repo with in-repo config for exactly the 39-checkpoint OLMo-3-7B sweep matching the post's claim, plus a committed centroids/ tree of prior outputs across all checkpoints/categories showing the pipeline was actually run end-to-end. The single surprising design choice is the aggressive delete-and-redownload-every-checkpoint behavior in hf_utils.load_model, which makes literal replication of the full 20x39 sweep a bandwidth marathon rather than a compute one.

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
