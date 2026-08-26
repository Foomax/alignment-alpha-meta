# Replicate: Distillation Robustifies Unlearning

Source post: `anX4QrNjhJqGFvrBr` (2025-06-13, LW karma 240). Repo: `addiefoote/distillation-robustify-unlearning` @ `edbf11189155c6bae81f5942df928c6ec2c5ac34`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Distilling a conventionally unlearned model into a randomly initialized student model (Unlearn-and-Distill) produces a model that is robust to relearning attacks, unlike standard unlearning which only suppresses the behavior; a generalized, compute-efficient version (UNDO: Unlearn-Noise-Distill-on-Outputs) dominates other unlearning methods on the retain/forget Pareto frontier and approaches gold-standard data-filtering robustness at a fraction of the compute, including on the WMDP Proxy benchmark with Gemma-2-2B.

Supporting quote from the post: "Distilling a conventionally unlearned model into a randomly initialized model creates a student that is robustly incapable of the forget capability."

**Headline metric:** resistance to relearning attacks (forget-performance recovery after finetuning attack) on the retain/forget Pareto frontier
**Claimed value:** Unlearn-and-Distill more resistant to relearning than unlearned-only baseline across 3 unlearning methods (GradDiff, Maxent, RMU) in language and arithmetic settings, sometimes near gold-standard data-filtering robustness; UNDO dominates other methods on the Pareto frontier after moderate (40-step) and extensive (500-step) relearning, and increases resilience to relearning on WMDP with Gemma-2-2B
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 5 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `Language/arithmetic (fits): run_pretrain_language.py -> run_unlearn_language.py -> run_partial_distill_language.py -> run_relearn_language.py (README's 'Quick Start'). WMDP (does not fit / data missing): run_unlearn_wmdp.py -> run_partial_distill_wmdp.py -> run_relearn_wmdp.py` (confidence: high)
- Produces: Retain/forget Pareto-frontier plots after 40-step and 500-step relearning attacks (language/arithmetic run_relearn_*.py outputs); the WMDP Pareto point specifically needs the withheld dataset.
- Models: google/gemma-2-2b (2.61B, gated)
- Estimated VRAM: 28 GB — Language/arithmetic settings pretrain and unlearn custom randomly-initialized reduced Gemma-2 architectures as small as 0.1B params (hidden_size 320, 14 layers, built by src/prepare_models/reduce_gemma.py) — trivial VRAM, well under 24GB. The WMDP setting instead full-fine-tunes real google/gemma-2-2b (bf16 trainable model + bf16 frozen reference copy for KL, plus torch.optim.AdamW with no 8-bit optimizer in src/tools/unlearn_wmdp/rmu.py) — roughly params*(2+2+8 bytes) ≈ 28GB+ for optimizer state alone, likely exceeding 24GB.
- Data: Korean/English pretraining corpora and arithmetic data (auto-downloaded via src/prepare_data/download_datasets.py, download_arithmetic.py), WMDP bio/cyber question-answer datasets — NOT shipped; README: 'Contact us for the WMDP question-answer datasets that were generated via wmdp_question_extraction.py'; availability: download-script
- Estimated runtime: hours (Unlearning runs use max_steps in the 90-100 range at batch_size=4, gradient_accumulation_steps=10, but run_*.py scripts sweep multiple methods (GradDiff/MaxEnt/RMU) x learning rates x seeds via launch_in_parallel_one_per_gpu, implying a multi-hour sweep in aggregate even though individual runs are short.)
- Stated compute in the repo: README: 'Params set for H200s. For GPU's with less GPU memory, try reducing batch size and increasing gradient accumulation by the same factor.'
- Known blockers: The WMDP bio/cyber QA dataset is not in the repo and must be requested from the authors directly — the one headline number that names Gemma-2-2B explicitly (WMDP Proxy resilience) can't be reproduced without it; The WMDP setting's full fine-tune of real gemma-2-2b (unlike the tiny custom models used for language/arithmetic) uses plain AdamW with a frozen bf16 reference copy and no memory-saving optimizer, likely exceeding 24GB; README states hyperparameters were tuned for H200 GPUs (140GB) and only vaguely suggests reducing batch size / raising grad-accum for smaller cards
- Inspector's notes: The paper's core Pareto-frontier claim (Unlearn-and-Distill / UNDO dominance) is demonstrated mainly on tiny (0.1-0.9B) synthetic language/arithmetic models that trivially fit a 3090 and have their data auto-downloaded; only the WMDP corroboration point needs the real 2B model, gated weights, and withheld data.

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
