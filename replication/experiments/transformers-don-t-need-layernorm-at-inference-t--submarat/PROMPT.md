# Replicate: Transformers Don't Need LayerNorm at Inference Time: Implications for Interpretability

Source post: `KbFuuaBKRP7FcAADL` (2025-07-23, LW karma 31). Repo: `submarat/removing-layer-norm` @ `583a9e63ff639f17ee514c79a857f8d5a16728ff`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> LayerNorm can be removed from all GPT-2 models up to XL (1.5B parameters) via fine-tuning with only a small increase in cross-entropy loss (e.g. +0.0253 for XL), showing LN plays no substantial role in language modeling, though contrary to expectations attribution patching accuracy does not improve in LN-free models even as direct logit attribution becomes exact and entropy neurons stop functioning.

Supporting quote from the post: "Contrary to our expectations, we saw no improvement resulting from removing LayerNorm."

**Headline metric:** cross-entropy loss increase, LN-free vs vanilla fine-tuned model, on The Pile-filtered
**Claimed value:** Small +0.0858, Medium +0.0962, Large +0.0812, XL +0.0253
**Direction of the claim:** 0
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 4 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `eval_pile.py (invocations listed in eval_all.sh reproduce the README table exactly)` (confidence: high)
- Produces: README's cross-entropy loss table (OWT/Pile/Pile-filtered columns) for Small/Medium/Large/XL LN-free vs vanilla — matches target_value exactly
- Models: openai-community/gpt2 (0.124B), openai-community/gpt2-medium (0.355B), openai-community/gpt2-large (0.774B), openai-community/gpt2-xl (1.5B), schaeff/gpt2-small_LNFree300 (0.124B), schaeff/gpt2-medium_LNFree500 (0.355B), schaeff/gpt2-large_LNFree600 (0.774B), schaeff/gpt2-xl_LNFree800 (1.5B)
- Estimated VRAM: 8 GB — Inference-only fp32 forward pass of GPT-2 XL (1.5B params, ~6GB weights) with batch_size=8, seq_len=1024, computing CE loss on Pile-filtered; no gradients/training needed since the LN-free and vanilla checkpoints used for the headline table are already published on HF
- Data: Pile-filtered (lucabaroni/apollo-pile-filtered-10k), Pile (apollo-research/monology-pile-uncopyrighted-tokenizer-gpt2), OpenWebText; availability: hf-hub
- Estimated runtime: hours (README: 'This task is compute intensive and takes about 4h on an A100' for eval_all.sh across ALL models and datasets; a single model/dataset pair is much faster)
- Stated compute in the repo: You will need 80GB+ GPU memory for most schedules - typically A100. (for TRAINING new LN-free checkpoints). Separately, for evaluation: 'This task is compute intensive and takes about 4h on an A100.'
- Known blockers: Training new LN-free checkpoints from scratch needs 80GB+ GPU per README, but this is NOT required to reproduce the reported numbers since the exact checkpoints are already released on HF; python_version not pinned anywhere in the repo
- Inspector's notes: The paper's own headline CE-loss table is reproducible purely via inference on released HF checkpoints (eval_pile.py/eval_all.sh); the 80GB+ GPU requirement in the README applies only to re-deriving the LN-free checkpoints via training from scratch.

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
