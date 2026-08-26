# Replicate: Probing Knowledge Recovery in Unlearned Models

Source post: `LLebzjrxuRzji6zhk` (2026-08-11, LW karma 7). Repo: `fathmamehnoor/unlearning-recovery-probes` @ `bc10cf3e745a8e5aa6936490a9bbf0e76ac2906c`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Across six WMDP-Bio-unlearned Llama-3-8B-Instruct checkpoints (RMU, ILU-RMU, NPO, GradDiff, NPO-ILU, IDK-AP), forget-set representation-targeted direction ablation and unrelated fine-tuning on GSM8K each recover substantial WMDP-Bio accuracy for several methods (up to 64% gap recovered and +41.4 accuracy points respectively), while refusal-direction ablation recovers no knowledge in the one checkpoint (ILU-RMU) where a clean refusal direction could be extracted, and qualitative inspection shows only 40-47% of 'recovered' answers reflect genuinely correct reasoning rather than contradictory or degenerate generations, showing that WMDP forced-choice accuracy alone overstates genuine knowledge recovery.

Supporting quote from the post: "A clean refusal direction was obtained only from the ILU-RMU checkpoint, reducing the refusal rate from 98% to 0% when ablated."

**Headline metric:** WMDP-Bio forced-choice accuracy recovery via different probes
**Claimed value:** forget-set representation ablation: 57-64% gap recovered for RMU/ILU-RMU/NPO, 19% for IDK-AP; unrelated GSM8K fine-tuning: +41.4pp (RMU), +23.8pp (ILU-RMU), +22.5pp (NPO) with MMLU flat; refusal-direction ablation: no recovery (95% CI excluded improvements >1.4pp) in ILU-RMU; only 40-47% of recovered answers showed genuine correct reasoning on qualitative review
**Direction of the claim:** +
**Uncertainty the post reported:** ci
**Tolerance for "reproduced":** `manual` — headline is a compound of 11 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/extract_refusal_direction.py + scripts/wmdp_bio_lm_eval_ablation.py (refusal/representation-direction ablation arms); wmdp_sft_recovery/train_gsm8k_qlora.py + eval_recovery_lm_eval.py (unrelated-SFT recovery arm)` (confidence: high)
- Produces: results.md tables (WMDP-Bio direction-ablation accuracy by method/model) and wmdp_sft_recovery/results/wmdp_sft_recovery/recovery_table.md
- Models: meta-llama/Meta-Llama-3-8B-Instruct (8.0B, gated), OPTML-Group/{GradDiff,IDK-AP,ILU-RMU,NPO,NPO-ILU}-WMDP-llama3-8b-instruct (8.0B, gated), ScaleAI/mhj-llama3-8b-rmu (8.0B, gated)
- Estimated VRAM: 20 GB — repo's own '4090' profile caps GPU memory at 22GiB for bf16 8B-model lm_eval runs; a 24GB 3090 has the same VRAM as the 4090 the authors profiled for
- Data: WMDP-Bio (via lm_eval's wmdp_bio task), MMLU, GSM8K (openai/gsm8k), AdvBench + Alpaca (refusal-direction contrast prompts); availability: hf-hub
- Estimated runtime: days (multi-session) (wmdp_sft_recovery/README.md: 'Run one model per session and clear its cache before the next (~40 GB disk...'; the design (6 checkpoints x 2 selection methods x baseline/selected/matched/8-random-control conditions on lm_eval WMDP-bio n=1273, plus separate GSM8K QLoRA SFT at 3 checkpoint sizes x 6 models x 2 arms) is explicitly built to span multiple GPU-rental sessions, with merge_results.py to combine them)
- Stated compute in the repo: multiple scripts define a '4090' hardware profile as their default: {'batch_size': 'auto:2', 'dtype': 'bfloat16', 'gpu_memory': '22GiB', 'cpu_memory': '64GiB'} (ablation_lib.py, extract_junk_directions.py, sweep_extract_base_activations.py, etc.)
- Known blockers: 6 gated Llama-3-8B-derived checkpoints must each be individually requested/accepted on HF across two different orgs (OPTML-Group, ScaleAI); Explicitly multi-day, multi-GPU-rental-session compute budget by the authors' own account, even though any single run fits a 3090; The qualitative 40-47% 'genuine correct reasoning' classification of recovered answers has no automated classifier or LLM-judge script found in the repo - appears to be manual/human review, so the exact figure is not push-button reproducible
- Inspector's notes: The most rigorously engineered repo in this batch: explicit hardware profiles matched to a 24GB consumer card, shared seeds/QLoRA recipes across arms, and detailed methodology docs (direction_extraction.md, results.md). The scale of the sweep across 6 checkpoints, not any single run's VRAM, is the main obstacle to full reproduction.

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
