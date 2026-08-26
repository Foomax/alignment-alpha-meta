# Replicate: LLM Self-Reference Language in Multilingual vs English-Centric Models

Source post: `kCCsrJeJiZRsgGbWt` (2025-10-22, LW karma 5). Repo: `mduffster/self-referent-test` @ `3c5ca9a739c20bd1cca1b4d6848575610b84751c`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Instruction tuning compresses attention-entropy-based self-referent processing toward neutral fact-retrieval processing in English-centric models (Llama, Mistral), while a multilingual model (Qwen) largely preserves the distinct attention pattern between self-referent and neutral prompts after instruction tuning.

Supporting quote from the post: "English-centric models (Mistral, Llama) show compression of layer-wise self-referent processing attention patterns toward neutral fact-retrieval patterns, while a multilingual model (Qwen) preserves the distinct attention patterns"

**Headline metric:** mean change in Role-Focus Coefficient (ΔRFC) from base to instruct, by model
**Claimed value:** Llama 3.1 8B: -0.023 (68.8% of layers compress); Mistral 7B: -0.093 (81.2% compress); Qwen 2.5 7B: +0.048 (28.6% compress, 50% near zero)
**Direction of the claim:** na
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 12 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `run_pipeline.py (drives activation_analysis.py then compare_base_instruct.py per model family)` (confidence: high)
- Produces: Delta-RFC (mean, % layers compressing) table per model family, produced by compare_base_instruct.py from the NPZ attention-pattern dumps written by activation_analysis.py.
- Models: mistralai/Mistral-7B-v0.1 (7B), mistralai/Mistral-7B-Instruct-v0.1 (7B), Qwen/Qwen2.5-7B (7B), Qwen/Qwen2.5-7B-Instruct (7B), meta-llama/Llama-3.1-8B (8B, gated), meta-llama/Llama-3.1-8B-Instruct (8B, gated)
- Estimated VRAM: 30 GB — activation_analysis.py hardcodes HookedTransformer.from_pretrained(..., dtype=torch.float32); models are loaded one at a time (not simultaneously), but fp32 weights for an 8B model alone are ~28-32GB, which exceeds a single 3090's 24GB. Author's own hardware notes are CPU-only (MacBook M4); no GPU run is reported anywhere in the repo.
- Data: none listed; availability: in-repo
- Estimated runtime: minutes (README: '~10-15 minutes per model for activation analysis (30 prompts/category)' on a MacBook M4 CPU.)
- Stated compute in the repo: README 'Hardware Requirements': 'Tested on: MacBook Pro M4 (48GB RAM)'; 'Expected runtime: ~10-15 minutes per model for activation analysis (30 prompts/category)'; 'Memory: ~16GB RAM needed for Mistral-7B model loading'
- Known blockers: dtype hardcoded to torch.float32 in activation_analysis.py -- must be edited to bf16/fp16 for an 8B model to fit in 24GB VRAM; meta-llama/Llama-3.1-8B(-Instruct) are gated models; Repo only verified on CPU (Mac); no GPU run reported anywhere to sanity-check the VRAM estimate
- Inspector's notes: Six model loads (3 families x base/instruct) are needed to reproduce the full cross-model table; each load is single-model, inference-only attention-pattern extraction, so a one-line dtype fix (fp32 -> bf16) makes this comfortably fit a 3090.

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
