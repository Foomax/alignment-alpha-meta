# Replicate: Weight-diff SVD for LLM Monitoring

Source post: `EPri6M2tMedbyahLq` (2025-08-05, LW karma 2). Repo: `fjzzq2002/weightwatch` @ `8d3874fb90a0aad5478514f96d71779d2aedf5aa`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Top singular vectors of weight differences between base and fine-tuned models correspond to fine-tuned behaviors, enabling near-perfect backdoor-utilization detection at inference time by monitoring activation alignment with these vectors

Supporting quote from the post: "In 9 out of the 13 models we tested, backdoor utilization is detected with 100% accuracy on first sight, effectively neutralizing the backdoor attack."

**Headline metric:** first-backdoor-utilization detection accuracy
**Claimed value:** 44% to 100% accuracy, FPR ~1%; 9 of 13 models detected at 100% accuracy on first sight
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/example.py` (confidence: low)
- Produces: 44-100% first-sight backdoor-detection-accuracy / ~1% FPR table across 13 models (9/13 at 100%) -- this specific evaluation harness/table is NOT in the repo.
- Models: meta-llama/Llama-3.2-3B-Instruct (3.0B, gated), meta-llama/Meta-Llama-3.1-8B-Instruct (8.0B, gated), Qwen/Qwen2.5-7B-Instruct (7.0B), allenai/OLMo-7B-Instruct-hf (7.0B), ethz-spylab/poisoned_generation_trojan1..5 (7.0B)
- Estimated VRAM: 20 GB — load_model_and_tokenizer loads BOTH the fine-tuned model and its base-model comparison target in fp16 simultaneously (base_model deleted only after SVD extraction). For the 3B model this is ~12GB combined (fits easily); for the 7-8B models (Qwen-2.5-7B, OLMo-7B, Llama-3.1-8B, trojan1-5 which are Llama2-7B-based) this is ~28-32GB combined, which does not fit natively in 24GB -- device_map='auto' would need to offload part of one model to the 31GB system RAM, which works but is slow.
- Data: no external eval dataset checked in; calibration uses generic chat data via CalibrationDataLoader; availability: unknown
- Estimated runtime: hours (calibrate() defaults to up to 50,000 samples (example.py uses 5,000) of full forward-pass activation extraction across all layers per model, times up to 13 models in the paper's full benchmark -- non-trivial but bounded per-model.)
- Stated compute in the repo: none
- Known blockers: The repo ships the reusable MonitoredModel library plus a 2-prompt demo (src/example.py), but not the actual multi-model benchmark script/eval loop that produced the 44-100%-accuracy, ~1%-FPR, 9-of-13-models table in the post -- that harness and its exact backdoor-trigger prompt set are absent.; For the larger (7-8B) models in the target list, base+fine-tuned model pair must be held in GPU memory simultaneously during SVD direction extraction, which is tight-to-over budget on a single 24GB card without CPU offload.
- Inspector's notes: The library (worker.py/latent_extractor.py/calibrate.py) genuinely implements the detection mechanism the paper describes, including threshold/FPR calculation (LatentStats.set_threshold), so a competent engineer could rebuild the missing eval loop -- but as shipped, the headline number's producing script is not in the repo.

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
