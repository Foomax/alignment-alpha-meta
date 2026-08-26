# Replicate: Most of the residual stream forgets within a token. A compact subspace doesn't.

Source post: `jkEnRkokmzvvKNzzB` (2026-06-06, LW karma 30). Repo: `fodenthal/residual-geometry-experiment` @ `2529e3257e0453c806fb65764c0225b7ca4f75e3`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In layer 12 of Gemma-2-2B, most residual-stream directions lose predictive signal within a single token, but a compact ~31-dimensional subspace has much longer autocorrelation timescales (90th percentile 17 tokens vs 1 for random/PCA directions); this slow subspace accounts for essentially all cross-token persistence (projecting it out collapses held-out timescale to near-null), depends on sequential token order rather than token composition alone, and aligns with attention-output geometry more than chance.

Supporting quote from the post: "most residual directions are fast, as their projected values stop being predictive after just one token. But a small set of directions is much slower."

**Headline metric:** 90th-percentile within-document autocorrelation timescale (tokens, 1/e crossing)
**Claimed value:** 17 tokens for time-lagged probes vs 1 token for random/PCA directions
**Direction of the claim:** +
**Uncertainty the post reported:** ci
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported spread

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `bash scripts/run_residual_geometry.sh pilot (drives 00_validate_env.py .. 07_make_residual_report.py, esp. 02_compute_residual_probes.py and 03_compute_residual_autocorr.py, config configs/persistent_state/residual_geometry/pilot.yaml)` (confidence: high)
- Produces: docs/pilot_run_summary.md, Stage B1 table: time-lagged Q90 tau = 17.0 vs random Q90 = 1.0 and PCA Q90 = 1.0 (exact match to the post's target values)
- Models: google/gemma-2-2b (2.6B, gated)
- Estimated VRAM: 10 GB — HookedTransformer.from_pretrained(..., dtype=bf16) on CUDA for gemma-2-2b (residuals/provider.py); batch_size 32, chunk_documents 128, 1024-token contexts, residual caching stored as float16 to disk rather than kept resident -- weights ~5GB bf16 + modest activation/cache overhead per batch
- Data: allenai/c4, English validation split; availability: hf-hub
- Estimated runtime: hours (Stage B1 pilot config: 5,000 docs x 1024 tokens through a 2.6B model, batch 32 -- the GPU forward-pass stage is likely well under an hour on a 3090; downstream bootstrap CIs / probe-fitting / subspace analysis stages add additional CPU time but docs/method.md's own guidance ('forward pass and storage cost are ~2x the 512-token equivalent, budget accordingly') implies single-digit hours total for the full pilot+report pipeline.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Unusually well-documented research artifact: pinned dependency versions, numbered pipeline stages, a config-hash-tracked pilot_run_summary.md whose Stage B1 table reproduces the post's exact headline numbers (Q90 17.0 vs 1.0), and an explicit 17-stage 'Compute Plan' in docs/method.md specifying doc counts and probe counts per stage. Gemma-2-2b requires accepting the HF license (gated) but that is a one-click formality, not a technical blocker.

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
