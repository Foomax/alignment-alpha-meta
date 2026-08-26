# Replicate: Minimal Prompt Induction of Self-Talk in Base LLMs

Source post: `tb7e2xARb6cfkJrAK` (2025-10-15, LW karma 2). Repo: `mduffster/null-loop-agent` @ `d4d5154c22a02fe6e807c8dd95d93cf7b28f71fe`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A base Llama-3-8B model produces no structured role- or goal-oriented language under empty or single-token prompts, but minimal instruction priming (e.g. 'You are a helpful assistant.') reliably induces structured role-based self-talk language, unlike the instruction-tuned version which shows such language immediately.

Supporting quote from the post: "Across ~20 iterations per condition, the base model produced no structured output under empty or single-token prompts, with structured role-based language appearing consistently only after minimal instruction priming."

**Headline metric:** regex-detected role/goal-language hit rate across prompt conditions
**Claimed value:** base model: 0 regex hits for role/goal patterns across 20 iterations under empty/single-token prompts; role-based language appeared consistently after minimal instruction priming
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `run-system-progression.py` (confidence: medium)
- Produces: README tables (SSR/TIAR/SRV for results_base/ and results_instruct/; RAR/IOI/PFI/CTA table for results_system_progression/) and null_loop_analysis.ipynb / system_progression_analysis.ipynb
- Models: QuantFactory/Meta-Llama-3-8B-GGUF (Q4_K_M) (8.0B), QuantFactory/Meta-Llama-3-8B-Instruct-GGUF (Q4_K_M) (8.0B)
- Estimated VRAM: 6 GB — Q4_K_M-quantized 8B GGUF via llama.cpp, n=256 generation, no chat template/no KV cache buildup beyond short feedback loop; ~4.7GB weights + small context
- Data: none listed; availability: in-repo
- Estimated runtime: hours (No wall-clock stated. Scale: Phase1 20 seeds x 20 steps x2 models, tipping-point 14 triggers x5 seeds x20 steps, system-progression 6 messages x20 steps, each generation up to 256 tokens on a quantized 8B via llama.cpp -- plausibly 2-6 hours total on a 3090, well within budget.)
- Stated compute in the repo: Apple M4 Pro (Metal acceleration) per EXPERIMENT_SETUP.md; llama.cpp also runs on CUDA so a 3090 is a straightforward substitute
- Known blockers: Requires building llama.cpp locally (not pip-installable, not pinned to a commit) with CUDA support since the repo's own build was for Apple Metal; download-models.sh points at third-party GGUF re-uploads (QuantFactory) rather than the gated meta-llama HF repos directly
- Inspector's notes: Very lightweight repo: quantized 8B GGUF models via llama.cpp completion mode, all metrics are local regex hit-rate over generated text, no external judge or API. Primary claim spans three scripts (run-loop-llama-cpp.py for base 0-hit, run-loop-instruct.py for instruct, run-system-progression.py for the minimal-priming tipping point) rather than one; I picked the system-progression script as entrypoint since it most directly tests the 'minimal instruction priming induces role language' claim.

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
