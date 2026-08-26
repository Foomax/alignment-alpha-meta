# Replicate: Unpacking Multimodal Data Leakage, Broken Benchmarks, and the Hessian Fallacy

Source post: `oSAiKTpQjjKmeeTvT` (2026-04-18, LW karma 8). Repo: `ai-forever/data_leakage_detect` @ `dedaa5e53976fcaec6795fd23a72f3265983f700`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Most published multimodal and text membership inference attack (MIA) benchmarks are broken because a target-model-free classifier using only dataset features achieves near-100% AUC on most of them (e.g. ~98.6% AUC on VL-MIA-Flickr-2k), showing these benchmarks measure distribution shift rather than memorization, and the Hutchinson-Hessian-trace theory claimed to explain perturbation-based MIA success (DetectGPT, Min-K%++) empirically fails.

Supporting quote from the post: "a model-free baseline hits AUC ≈98.6% on VL-MIA-Flickr-2k, meaning “members” and “non-members” are trivially separable."

**Headline metric:** model-free (no model access) baseline AUC on VL-MIA-Flickr-2k
**Claimed value:** AUC ≈ 98.6%
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `shift_detection/run_attack.py` (confidence: high)
- Produces: AUCROC for bag_of_visual_words on VL-MIA Images / Flickr(_2k), reported in shift_detection/README.md's results table (Flickr AUCROC 99.0, close to the post's ~98.6%) and reproduced via 'shift-attack --dataset=vl_mia_img_Flickr_2k --attack=bag_of_visual_words'
- Models: GPT-J 6B, GPT-2 XL, LLaVA 1.5-7B
- Estimated VRAM: 0 GB — the bag_of_visual_words attack (shift_detection/bag_of_visual_feats.py) uses only OpenCV SIFT features, KMeans clustering, and sklearn classifiers on CPU; no neural network inference is required for this specific model-free baseline
- Data: JaineLi/VL-MIA-image (HF dataset, 'Flickr_2k' subset via load_dataset); availability: hf-hub
- Estimated runtime: minutes (classical feature extraction (SIFT/LBP/DCT) + KMeans clustering + a shallow classifier over a few thousand images is entirely CPU-bound and fast)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: By far the lightest repo in this batch: no GPU, no gated model, no closed API. The broader FiMMIA framework (fimmia/) does use large VLMs like Qwen2.5-VL for other, unrelated experiments in this repo, but the specific headline number assigned here needs none of that.

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
