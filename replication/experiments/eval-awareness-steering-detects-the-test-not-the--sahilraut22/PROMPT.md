# Replicate: Eval-Awareness Steering detects the Test, Not the Sabotage

Source post: `ogvyWqJtSrpgXfc7t` (2026-06-25, LW karma 2). Repo: `sahilraut22/eval-research` @ `274bb55d6f185a1f854d1b6ffca3d125d50c9420`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In Llama-3.1-8B-Instruct, the internal difference-of-means 'eval-awareness' direction is a genuine detector of evaluation framing (~0.81 AUROC on novel format-matched framings) but steering with it does not causally drive sandbagging (flat dose-response that fails to beat an empirical null of 24 random directions) nor predict which individual items get sandbagged (per-item probe AUROC ~0.54, at chance).

Supporting quote from the post: "I found that direction is a valid detector of evaluation framing (~0.81 AUROC under novel, format matched framings) but is neither a causal drive of sandbagging nor a per-item predictor of it."

**Headline metric:** swing in sandbagging accuracy from steering dose alpha=-2 to alpha=+2 at headline layer 12, vs empirical null of 24 random directions
**Claimed value:** -1.77pp swing, sub-threshold Spearman rho=-0.53 (p=0.08), does not beat empirical null (p=0.20)
**Direction of the claim:** 0
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 4 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `steering/run_e3b.py --layers 12 14 24 (causal steering dose-response sweep, RQ1)` (confidence: high)
- Produces: results/e3b_steering/sweep.json + manifest.json (dose-response table, Spearman rho, empirical-null p-value); currently only an unfilled scaffold ('STATUS: STAGED / not-yet-run') in this checkout, unlike E1 which has real pod_run results checked in.
- Models: meta-llama/Meta-Llama-3.1-8B-Instruct (8.0B, gated)
- Estimated VRAM: 18 GB — The repo's own real run log for this exact model/pipeline (E1) states RTX 4090 (24GB), fp16, single device, no 8-bit -- an RTX 3090 is the same VRAM class.
- Data: WMDP, MMLU, Alpaca, repe_honesty__plain; availability: hf-hub
- Estimated runtime: hours (E1's real run (same model/harness) generated ~2000 rollouts at up to 512 tokens plus probe fitting on a full pod run; E3b adds a 9-point coefficient sweep x 3 layers of similarly generation-heavy evals.)
- Stated compute in the repo: results/e1_replication/pod_run/RUN_LOG.md: 'Hardware: RunPod, single RTX 4090 (24 GB), fp16, single device (device_map {\'\':0}, no sharding, no 8-bit).'
- Known blockers: Depends on an external harness (ApolloResearch/deception-detection @ f8ec401) that must be cloned separately and patched with the 7 patches in apollo_patches/; Llama-3.1-8B-Instruct is gated on HF (license acceptance needed); E3b's own RUN_LOG.md is an unfilled scaffold in this checkout -- the dose-response numbers backing the assigned target_value are not yet present as artifacts here, only the (already 4090-validated) E1 pipeline is filled in
- Inspector's notes: A different experiment in this repo (E4, predictive per-item probe vs black-box baseline, RQ3, mentioned in the post's primary_claim narrative) DOES require a closed-API grader (patch 0006: DD_GRADER=anthropic claude-3-5-sonnet-20241022 or openai gpt-4o-2024-08-06) for its behavioural-baseline arm. That is not the assigned target_value metric (the E3b steering swing at layer 12), which is fully objective/local (MCQ accuracy, no LLM judge).

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
