# Replicate: Avoiding jailbreaks by discouraging their representation in activation space

Source post: `5XjzmxcZFm3BJrNmn` (2024-09-27, LW karma 8). Repo: `guidobergman/jailbreak_direction` @ `ef6fe41788fa3a35da420d0df3b6d70d76364128`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In Gemma 2 2B IT, subtracting a difference-in-means 'jailbreak direction' from residual-stream activations (activation addition) drops the jailbreak attack success rate from about 60% to 0% on a held-out test set including unseen jailbreak communities, while directional ablation of the same direction instead makes the model much more vulnerable (ASR rising to 85-97%); both interventions increase refusal on harmless prompts from 3.15% to about 18.88%.

Supporting quote from the post: "the attack success rate dropped from 60% to 0%. Additionally, that indicates that a direction representing jailbreaks might exist and disabling it could make all jailbreaks unsuccessful."

**Headline metric:** jailbreak attack success rate (ASR, via Llama Guard 2 / HarmBench)
**Claimed value:** baseline 60.55%/59.38% -> activation addition 0.00%/0.00%; directional ablation 96.88%/84.77%
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `pipeline/run_pipeline.py` (confidence: high)
- Produces: pipeline/runs/gemma-2-2b-it/completions/*_evaluations.json — per-intervention, per-methodology ASR values matching the post's headline percentages; results for this exact model+sha are already committed
- Models: google/gemma-2-2b-it (2.0B, gated), cais/HarmBench-Mistral-7b-val-cls (7.0B), meta-llama/Meta-Llama-Guard-2-8B (8.0B, gated)
- Estimated VRAM: 16 GB — Gemma-2-2B-IT generation is trivial (~5GB bf16); the harmbench eval stage separately loads the 7B HarmBench-Mistral classifier via vLLM (~14-16GB with default KV-cache reservation), but the two stages run sequentially, not concurrently
- Data: jailbreak_prompts (verazuo/jailbreak_llms), alpaca (harmless baseline), JailbreakBench-derived harmful/harmless splits; availability: download-script
- Estimated runtime: hours (not stated; inferred from workload (train_size_successful=256, test_size_unsuccessful=100, test_size_harmless=32, max_new_tokens=512) x 3 intervention conditions (baseline/actadd/ablation) x eval methodologies, on a 2B model)
- Stated compute in the repo: none
- Known blockers: the 'llamaguard2' eval methodology (one of the two named judges in the target_value) calls Together AI's hosted Meta-Llama-Guard-2-8B via litellm and needs a TOGETHER_API_KEY plus paid credits — not a closed frontier-model API, but still an external paid service outside a no-cloud-credits budget; the 'harmbench' methodology (local vLLM, no key) can stand in as it's the other named judge
- Inspector's notes: Small target model (Gemma-2-2B-IT) makes the core steering pipeline cheap; results for this exact commit are already checked into pipeline/runs/gemma-2-2b-it/. Gemma and Llama Guard 2 weights are gated (free HF licence click-through).

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
