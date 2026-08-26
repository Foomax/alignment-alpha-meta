# Replicate: Do k-Sparse Autoencoders Reveal Thinking Patterns? Interpretable Features in a Small Reasoning Model

Source post: `nKRvp7LKgjJxbpykq` (2026-06-15, LW karma 8). Repo: `artmtt/sae-interpretability-small-reasoning-model` @ `50c2b40be1f3e8a2bd1f5bbede75ac88bc1d197b`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Pre-trained k-sparse autoencoders applied to DeepSeek-R1-Distill-Qwen-1.5B's hidden states (on GSM8K reasoning traces) successfully extract interpretable features, including several features in layer 10 that strongly and repeatedly activate on tokens characteristic of the model's reasoning process.

Supporting quote from the post: "The trained k-Sparse Autoencoders that were used effectively extracted features from DeepSeek R1 Distill Qwen 1.5B."

**Headline metric:** frequency a feature is a top feature across 32 model inferences (layer 10)
**Claimed value:** feature 32456: top feature in 28/32 inferences; feature 6252: 14/32; feature 31146: 10/32
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 9 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `interp_experiments_deepseek_r1_distilled_qwen.ipynb` (confidence: high)
- Produces: Top-feature frequency counts for layer-10 features 32456/6252/31146 across 32 GSM8K inferences, computed in interp_experiments_deepseek_r1_distilled_qwen.ipynb's load_and_analyze_model_inferences / get_top_k_encoder_out_by_acts pipeline.
- Models: deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B (1.5B)
- Estimated VRAM: 4 GB — 1.5B causal LM (bf16 ~3GB) plus a single-layer 65k-width k-sparse SAE (EleutherAI/sae-DeepSeek-R1-Distill-Qwen-1.5B-65k, ~a few hundred MB) applied to layers 5/10/20 one at a time, plus KV cache for 32 x 400-token generations; trivially small workload.
- Data: GSM8K (openai/gsm8k); availability: hf-hub
- Estimated runtime: minutes (32 model inferences with max_new_tokens=400 on a 1.5B model, plus SAE encoding of 3 layers; no runtime figure stated in the repo but trivial given model/data size.)
- Stated compute in the repo: none
- Known blockers: No requirements.txt/pyproject.toml/environment.yml anywhere in the repo -- exact dependency versions must be inferred from notebook imports; sparsify is wired in as a git submodule (.gitmodules -> EleutherAI/sparsify) that must be fetched separately
- Inspector's notes: Clean, small, inference-only SAE analysis; both the base model and the pretrained k-sparse SAE are public on Hugging Face, so this fits comfortably on a single 3090 with a lot of headroom.

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
