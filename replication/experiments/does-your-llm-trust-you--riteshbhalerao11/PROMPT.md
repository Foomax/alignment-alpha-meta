# Replicate: Does Your LLM Trust You?

Source post: `AExopgZ9Yj6qzTrxb` (2026-08-04, LW karma 8). Repo: `riteshbhalerao11/mats-summer-app` @ `582db85327d9b4c18f654cc87c5c2c781475f26e`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A linear 'Trustworthiness' direction extracted from Llama-3.2-3B-Instruct and Llama-3.1-8B-Instruct activations causally overrides safety guardrails when added via steering, reducing refusal on harmful prompts even more than Arditi et al.'s compliance/refusal direction, remains highly effective after orthogonalizing out the compliance-vector component, and (unlike steering against the compliance vector) does not cause excessive refusal on benign adversarial prompts.

Supporting quote from the post: "All of the trust vectors are very effective in reducing refusal on harmful prompts (even more than the compliance vector)."

**Headline metric:** compliance rate on harmful prompts under steering
**Claimed value:** all trust vectors (including orthogonalized) reduce refusal on harmful prompts more than the compliance vector; trust-vector steering does not increase refusal on benign WildJailBreak prompts, unlike negative-compliance steering
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/steering/steer_model.py -> src/evaluation/judge_outputs.py -> src/evaluation/visualize_judgments.py` (confidence: medium)
- Produces: outputs/judge_outputs/openai_gpt-oss-120b/{llama,llama_8b}/... judged compliance counts, aggregated/plotted by src/evaluation/visualize_judgments.py -- the compliance-rate-under-steering comparison across trust/compliance/orthogonalized vectors
- Models: meta-llama/Llama-3.2-3B-Instruct (3B, gated), meta-llama/Llama-3.1-8B-Instruct (8B, gated)
- Estimated VRAM: 18 GB — Activation collection / steering on Llama-3.1-8B-Instruct via nnsight, bf16 inference-only (no fine-tuning of the base model), plus linear probe training on cached activations.
- Data: JailbreakBench-derived harmful/xstest/wildjb_benign/user_description prompt sets, synthetic conversation datasets (trust-level scenarios); availability: in-repo
- Estimated runtime: hours (No compute stated; inferred from steering + judging over multiple layers/strengths/datasets on 3B/8B models.)
- Stated compute in the repo: none
- Known blockers: No requirements.txt or pyproject.toml anywhere in the repo (only an unrelated crosscoder_learning/requirements.txt); environment must be reconstructed from imports; The actually-used LLM judge (openai/gpt-oss-120b, per outputs/judge_outputs/) and the dataset-generation model (qwen/qwen3-235b-a22b-thinking-2507, per code default) are both open-weight but far too large to self-host on a single 3090, so re-running those two steps from scratch needs an OpenRouter API key/credits even though neither is a 'closed' proprietary model
- Inspector's notes: The causal steering experiment itself (trust-vector extraction, orthogonalization, steering) runs entirely on local Llama-3B/8B and fits a 3090 comfortably. Judge outputs (outputs/judge_outputs/) and generated conversation datasets (data/datasets/*.parquet) are already committed to the repo, so the compliance-rate plots can likely be regenerated from committed artifacts without new API calls; only a from-scratch redo of judging/data-gen would hit the OpenRouter dependency. CLI docstrings also show 'anthropic/claude-3.5-sonnet' as an example judge/generator model, but the artifacts actually checked into the repo used the open-weight gpt-oss-120b judge instead.

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
