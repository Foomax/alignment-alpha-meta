# Replicate: Selective Generalization: Improving Capabilities While Maintaining Alignment

Source post: `ZXxY2tccLapdjLbKm` (2025-07-16, LW karma 83). Repo: `arianaazarbal/selective-generalization` @ `f7f2e54e6b40da1a0fc307d741d6255bebf02798`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Across two model organisms (emergent misalignment from harmful medical advice, and math-induced sycophancy), simply including a limited proxy alignment dataset in the training mix is insufficient to prevent misaligned generalization, but a KL-divergence penalty on that alignment data (and DPO) pushes the capability-alignment Pareto frontier furthest among seven benchmarked mitigation methods.

Supporting quote from the post: "Merely including alignment data in training data mixes is insufficient to prevent misalignment, yet a simple KL Divergence penalty on alignment data outperforms more sophisticated methods."

**Headline metric:** Pareto frontier of task/capability performance vs general alignment across 7 mitigation methods
**Claimed value:** KL divergence penalty and DPO push the Pareto frontier furthest in both the emergent-misalignment and sycophancy settings; naive mixed fine-tuning on limited alignment data does not increase (and in the EM setting slightly decreases) general alignment
**Direction of the claim:** +
**Uncertainty the post reported:** seeds
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `projects/emergent_misalignment_trainers/emergent_misalignment.py` (confidence: high)
- Produces: results.json under each projects/emergent_misalignment_trainers/experiments/*/ (loss + MCQ-accuracy over epochs) for the EM/Qwen3-8B setting, and projects/gemma_gcd equivalents for the sycophancy/Gemma-2B setting; emergent_misalignment_plots.py assembles these into the Pareto-frontier figures.
- Models: Qwen/Qwen3-8B (8.0B), google/gemma-2b-it (2.0B, gated)
- Estimated VRAM: 20 GB — Qwen3-8B config.json for the EM experiment sets load_in_16bit=true (bf16, ~16GB weights), LoRA r=32/alpha=64 on all linear modules with use_gradient_checkpointing=true, per_device_train_batch_size=2, max_seq_length=2048 -- fits under 24GB with headroom; 4-bit/8-bit loading is also available in experiment_utils.py (load_in_4bit/load_in_8bit) if tighter. Gemma-2B-IT experiment (gemma_gcd) is smaller still.
- Data: projects/emergent_misalignment_trainers/data/sneaky_medical_diet_only.jsonl (in-repo), HHH/SAFETY alignment-proxy MCQ data, gemma_gcd GCD math dataset + capital-cities alignment proxy; availability: in-repo
- Estimated runtime: hours (Each individual run is 1 epoch over ~6000 examples at effective batch 16 (~375 steps) with an 8B LoRA model -- tens of minutes per run. The full Pareto frontier in the post benchmarks 7+ methods x multiple hyperparameter values (e.g. 9 beta_kl values) x multiple seeds (experiments/large_sweep* directories show dozens of pre-run configs), so reproducing the *entire* frontier is many sequential single-GPU runs (plausibly 1-2 days of wall-clock on one 3090), even though any single method/config is cheap.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Unusually well-organized multi-experiment benchmark repo with two independent self-contained sub-pipelines (EM/Qwen3-8B and GCD-sycophancy/Gemma-2B) matching both models named in the claim. `openai` is a listed dependency and an `openai_model` parameter exists in gemma_gcd/all_evals.py, but the actual sycophancy metric used (get_user_confirmation_score) and MCQ/MMLU evals are rule-based/local-logprob, not LLM-judge calls in the code path that was actually exercised (the GPT-judge tone-scoring call is commented out) -- so no closed API is required for the primary Pareto-frontier claim. Repo is large (559MB), mostly checkpoint/result PNGs from prior sweep runs; inspected via GitHub API tree + raw file fetches pinned to the exact head_sha (local clone was still transferring due to network contention from many concurrent inspection agents sharing this scratchpad).

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
