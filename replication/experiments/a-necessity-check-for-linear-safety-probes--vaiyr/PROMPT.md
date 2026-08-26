# Replicate: A necessity check for linear safety probes

Source post: `jauWv9BEbdCYcRy2d` (2026-04-28, LW karma 2). Repo: `vaiyr/probe-necessity` @ `31017ee29feb54bff026ad42f400c86384638635`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Linear safety probes that successfully detect (AUROC≥0.91) and steer a feature often fail to 'silence' it via causal projection, showing that detect/steer success is not evidence of a true causal handle; a calibration-time cosine diagnostic between plain and within-class-whitened difference-of-means directions predicts silencing success across 4-5 model families and 2 features, recovering all 17 existing causal handles and correctly alarming on the remaining 5 in a 22-cell battery.

Supporting quote from the post: "Probe accuracy is not evidence of a causal handle."

**Headline metric:** necessity-check protocol recovery of true causal handles vs. correct alarms, 22-cell battery
**Claimed value:** recovers all 17 causal handles that exist and correctly alarms on the remaining 5
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/run_autopicker_battery.py` (confidence: high)
- Produces: results/monitor/autopicker_battery.json -- 'auto 22/27, dom 15/27, lr_cv 18/27' aggregate, i.e. the 17 recovered + 5 correctly-alarmed NECESSITY_LOST cells in the 22-cell body battery cited in target_value
- Models: Llama 3-8B, Gemma 2-9B, Mistral 7B-v0.3, OLMo 2-7B, Qwen 2.5-7B
- Estimated VRAM: 0 GB — scripts/run_autopicker_battery.py is pure CPU: it reads the already-shipped per-cell results/**/result.json files and runs the necessity-check decision rule; no model is loaded, no GPU touched.
- Data: results/ablation_refusal*/**/result.json and results/paper/raw/*_whitening.json (all shipped in-repo); availability: in-repo
- Estimated runtime: minutes (README states this step 'Takes < 1 second, no GPU.')
- Stated compute in the repo: README: 'CPU is enough to reproduce every paper number from the shipped results.' / 'GPU (H100 via Modal; 1x for extraction/ablation, 2x for SFT) required only to regenerate the raw data from scratch.'
- Known blockers: This CPU replay recomputes the decision rule over PRE-COMPUTED per-cell ablation results already checked into the repo; it is not a re-derivation from raw model weights.; Fully-from-scratch regeneration of those per-cell results (README Steps 3-4: freeze buffer -> base eval -> extract -> fit probes -> SFT rounds -> ablation battery) needs 1-2x H100 GPUs via Modal (not a single 3090) at ~$60-80/family and 12-24h wall-clock each, across 5 (model, feature) conditions.; From-scratch regeneration also needs an Anthropic API key (Claude Haiku for the refusal judge, Claude Sonnet for the sycophancy judge) -- a hard blocker under a no-closed-API-keys budget.; Llama-3-8B-Instruct, Gemma-2-9B-it, and Mistral-7B-Instruct-v0.3 are gated on HF (OLMo-2 and Qwen2.5 are not).
- Inspector's notes: A genuinely two-tier repo: the exact headline aggregate (17/5 recovery in the 22-cell battery) is trivially reproducible on any machine, even without a GPU, because the per-cell ablation results ship in the repo -- but reproducing those underlying per-cell numbers from raw model weights is well beyond a single 3090 (needs H100s plus a closed Anthropic API key).

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
