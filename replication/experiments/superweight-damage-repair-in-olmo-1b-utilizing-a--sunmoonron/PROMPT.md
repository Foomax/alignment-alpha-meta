# Replicate: Superweight Damage Repair in OLMo-1B utilizing a Single Row Patch (CPU-only Experiment) 

Source post: `ifbNtv8QbNBrYFSSv` (2025-12-13, LW karma 12). Repo: `sunmoonron/super-weight-circuit-patching` @ `dbc14761cd4510b6996de75491e085637cce9c2c`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Ablating a single 'superweight' in OLMo-1B causes perplexity to spike from 17.4 to 2884.3 with pathological outputs, but training a single trainable row-vector patch via KL distillation from the original model recovers approximately 93% of the lost performance while learning a new, largely orthogonal distributed direction rather than relearning the original weight (cosine similarity to the original row ~0.13).

Supporting quote from the post: "Surprisingly, it worked! Perplexity dropped drastically(i.e 2884.3 to 25.2) nearing the original model's values, and the Tokyo prompt was fixed... I observed approximately 93% recovery."

**Headline metric:** Perplexity on Wikitext-2 slice
**Claimed value:** 17.4 (original) -> 2884.3 (ablated) -> 25.2 (patched); ~93% recovery
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 4 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `07_compare_patch.py` (confidence: high)
- Produces: results/07_compare_results.txt and results.png — BASE/BROKEN/PATCHED NLL/PPL table plus cosine-similarity stats for delta_row vs base_row, produced by 07_compare_patch.py
- Models: allenai/OLMo-1B-0724-hf (1.0B)
- Estimated VRAM: 4 GB — Repo is designed CPU-only (fp32, ~16GB system RAM), but OLMo-1B in fp32 for inference/training a single trainable row easily fits a 24GB GPU if one wanted to move it there; base model weights alone are ~4GB in fp32.
- Data: wikitext-2-raw-v1; availability: hf-hub
- Estimated runtime: minutes (Training loop (03_train_patch.py) hard-caps at i>200 steps per epoch, 2 epochs, batch_size=2, 128 max_len, single trainable row-vector; eval (07_compare_patch.py) caps at NUM_EVAL_BATCHES=30, batch_size=1. All on a 1B model.)
- Stated compute in the repo: Run this on CPU (requires ~16GB RAM) [01_make_checkpoints.py comment]; config.py: DEVICE = "cpu"  # Because too poor MPS :(; README title: '(CPU-only Experiment)'
- Known blockers: none recorded
- Inspector's notes: Extremely reproducible: results/07_compare_results.txt already committed in the repo contains the exact target numbers (PPL 17.41->2884.33->25.24, cos(base,delta)=0.1336), i.e. the repo's own prior run reproduces the post's headline claim verbatim. Ungated model, all-CPU by design, trivial compute.

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
