# Replicate: The AI Safety Puzzle Everyone Avoids: How To Measure Impact, Not Intent.

Source post: `3KTgeXBfhvRKfL5kf` (2025-07-22, LW karma 6). Repo: `patrickod32/landed_writes` @ `a3bc2a852cc701b0ab6467bd6c168ddaebfa384e`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A new interpretability attribution method ('landed writes') that measures RMSNorm-scaled, post-normalization contributions of neurons and attention heads to the residual stream shows that early-layer writes are amplified by up to 176x while late-layer writes are compressed, and that logit predictions in LLaMA-3.1-8B and Mistral-7B rely on a sparse set of just 11-90 coordinates.

Supporting quote from the post: "Experiments show that 98.8% of all writes get amplified by more than 2×, with 81.2% amplified by more than 10×."

**Headline metric:** RMSNorm write-scaling amplification factor by layer depth; sparsity of coordinates driving logit predictions
**Claimed value:** early layers amplify writes up to 176x (Mistral) / 10-16x (Llama); late layers compress to 0.55-6.8x; 98.8% of writes amplified >2x, 81.2% amplified >10x; logit predictions rely on just 11-90 coordinates out of thousands
**Direction of the claim:** na
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 11 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `Llama-3.1-8B-Instruct_scaling.ipynb` (confidence: medium)
- Produces: Per-layer amplification-factor tables/plots (Llama-3.1-8B and Mistral-7B *_scaling.ipynb) and the logit-sparsity coordinate-count analysis (Llama-3.1-8B-Instruct_logit_sparsity.ipynb).
- Models: meta-llama/Meta-Llama-3.1-8B-Instruct (8.0B, gated), meta-llama/Llama-3.2-1B-Instruct (1.0B, gated), mistralai/Mistral-7B-Instruct-v0.2 (7.0B, gated)
- Estimated VRAM: 32 GB — As literally written, `AutoModelForCausalLM.from_pretrained(model_name, ...)` is called with no `torch_dtype`/`dtype` argument anywhere in any of the 4 notebooks, which loads the 8B models in fp32 (~32GB weights alone) -- would NOT fit a 24GB 3090 unmodified. A one-line fix (`torch_dtype=torch.bfloat16`) drops this to ~16GB, which fits comfortably; this is a trivial, well-understood modification for inference-only forward passes with hooks, not a fundamental blocker.
- Data: small hand-written prompt lists (in-notebook, not a formal dataset); availability: in-repo
- Estimated runtime: minutes (Forward passes only (no training) over a handful of hand-written prompts per notebook, computing per-layer RMSNorm coordinate statistics and doing top-k ablation/coverage analysis; no batching or large-scale sweep evident.)
- Stated compute in the repo: none
- Known blockers: No README, no requirements.txt/pyproject/environment file -- dependencies inferred only from notebook pip-install cells.; Default fp32 model loading as literally written won't fit 24GB for the 8B models unless the engineer adds a dtype argument (trivial fix, noted above).
- Inspector's notes: 4 independent, single-purpose notebooks (no shared entrypoint script); the post's numbers are split across the *_scaling notebooks (amplification factors) and the *_logit_sparsity notebook (coordinate count). No stated compute anywhere in the repo -- had to infer VRAM purely from model sizes and default HF loading behavior.

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
