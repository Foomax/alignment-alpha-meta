# Replicate: The Termination Circuit (how reasoning models stop thinking).

Source post: `ajhzc6ktEKyFeJFBS` (2026-07-11, LW karma 12). Repo: `chandram-dutta/the-termination-circuit` @ `4e68ee5a412dc51ad84ff49f256d1c73654f36bf`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In Qwen3-1.7B reasoning on GSM8K, the model has typically already determined the correct answer by roughly 30% of the way through its chain-of-thought, yet keeps 'overthinking' until a small, localized set of late MLP layers (dominated by layer 27 of 28, contributing ~40% of the </think> logit) fires a 'termination circuit' functioning as a verification gate that stops reasoning only once the model has just stated an answer AND that stated value matches what it has internally computed (94% firing when the model's own correct answer is spliced in, vs 8-19% for mismatched-value/wrong-timing/different-problem controls and 0% for random text), and this gate has no simple linear steering handle, a pattern that replicates on Qwen3-8B and Magistral-Small-24B on MATH-500.

Supporting quote from the post: "When the spliced answer is the model's own correct answer, the circuit fires `</think>` as the greedy next token 94% of the traces... A different problem's answer fires it 19% of the time and a random non answer fires it 0% of the time."

**Headline metric:** </think>-emission (greedy) firing rate under causal splicing of the answer sentence into the CoT, and CoT fraction at which the answer is settled
**Claimed value:** 94% firing rate when the model's own correct final-answer sentence is spliced in after the sufficiency point; 8% with a different number in the same sentence; 16% if spliced before the sufficiency point; 19% for a different problem's answer; 0% for random non-answer text; best single steering direction recovers only ~20% of the effect of full-state patching; median sufficiency point is reached at ~30% of CoT length
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 7 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/exp01_predictive_probing/probing.py -> exp02_logit_attribution/logit_attribution.py -> exp03_causal_patching/causal_patching.py -> exp04_targeted_steering/steering.py` (confidence: high)
- Produces: 94%/8%/16%/19%/0% </think>-emission firing rates under splicing conditions (exp03 causal_patching.py); median ~30% sufficiency point (exp01 probing.py); ~20% steering-direction recovery (exp04 steering.py)
- Models: Qwen/Qwen3-1.7B (1.7B), Qwen/Qwen3-8B (8B), mistralai/Magistral-Small (24B) (24B)
- Estimated VRAM: 24 GB — README states directly: 'Qwen3-1.7B experiments fit comfortably on a 24 GB card' -- the primary model plus per-layer/per-head activation caching for causal patching.
- Data: openai/gsm8k (HF dataset), MATH-500 (HF dataset, exp05 generalization); availability: hf-hub
- Estimated runtime: hours (exp01 defaults to --n-traces 500 full generations; exp03 performs layer-scan and splice-test causal patching (hundreds of ablation runs) across the trace set; no wall-clock figure given.)
- Stated compute in the repo: Qwen3-1.7B experiments fit comfortably on a 24 GB card, the Qwen3-8B replication wants 40 GB or more, and the Magistral-24B experiments are sized for a 96 GB card.
- Known blockers: Qwen3-8B and Magistral-Small-24B cross-model replication claims explicitly need 40GB+ and a 96GB card per the README -- not reproducible on a single 3090; only the primary Qwen3-1.7B/GSM8K result is.
- Inspector's notes: Unusually well-documented repo: explicit per-experiment VRAM requirements, a script-to-paper-section table, and staged checkpointing so later stages reload in seconds. The primary headline numbers (Qwen3-1.7B, GSM8K) are fully in-budget on a 3090; only the cross-scale/cross-family generalization claims are out of reach.

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
