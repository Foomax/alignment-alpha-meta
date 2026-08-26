# Replicate: The imposters among us: function vectors that ace every check and do the wrong task (in search of circularity)

Source post: `aFyir2PaoCHK5prAu` (2026-08-21, LW karma 7). Repo: `star2vec/tarcle` @ `37831a330ec5d4339d6946c1a2e51732ce8fce00`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Shift-by-k-months function vectors extracted from low-diversity few-shot prompts (Llama-3.2-3B) pass all three classic validation checks (behavioral gate, stability, causal effect) yet encode a completely different task (outputting an adjacent month, ignoring k), with margin scores as low as -1.000 in the most extreme case, and lower example diversity simultaneously makes the checks look better (few-shot accuracy 0.38 to 0.83) while making the vector's true identity worse

Supporting quote from the post: "The culprit is the number of distinct example inputs. Lower diversity makes the model perform the few-shot task better (from 0.38 to 0.83) even though the function vector changes identity, so the checks actually favor the imposters."

**Headline metric:** margin (correct shift-by-k occurrences minus neighbor-task occurrences, among cases where they differ) across month-diversity sets
**Claimed value:** margin +0.35 (12 months) and +0.34 (9 months) down to -0.31, -0.46, -0.70, -0.94 (6- and 4-month range sets), with -1.000 for the September-December subset; behavioral gate rises from 0.38 to 0.83 as diversity drops
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 13 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `tarcle/extract.py (Stage 1, GPU: causal-head identification + FV extraction) then python -m tarcle.stage2 / floors / measure_corr / margin_split / offset_audit / support_gate (Stage 2, numpy-only, reads results/ artifacts)` (confidence: high)
- Produces: results/fv/*.npz (extracted function vectors) + committed stage-2 artifacts consumed by tarcle/margin_split.py and tarcle/support_gate.py, which reproduce the reported margins (+0.35 down to -1.000) and the 0.38->0.83 behavioral-gate accuracy shift
- Models: meta-llama/Llama-3.2-3B (3.2B, gated)
- Estimated VRAM: 8 GB — Explicitly engineered and documented to run on an 8GB consumer GPU: left-padding + explicit position_ids to keep logits_to_keep=1, and single-position (not full-sequence) activation hooks, specifically to avoid OOM on an 8GB card. Comfortably fits a 24GB 3090.
- Data: synthetic month/day few-shot prompts generated in-code (tarcle/prompts.py) -- no external dataset; availability: in-repo
- Estimated runtime: hours (Extraction batches all 24 attention heads of a layer in one forward pass by replicating the prompt; the injection sweep covers 672 (layer x strength) settings, each a lightweight forward/generation on a 3B model -- plausibly under a few hours on a 3090. Stage 2 (fitting margins/thresholds from saved artifacts) is numpy-only and near-instant.)
- Stated compute in the repo: "Two conventions hold everywhere in here, and both are load-bearing on an 8GB card (docs/decisions.md D6)" -- extract.py docstring; README: "Original runs on CUDA bf16; later runs on MPS bf16 after passing a registered cross-device validation (D50-D53)."
- Known blockers: none recorded
- Inspector's notes: The most reproducibility-forward repo in the batch: 'every number in the post regenerates from results/ without a GPU' via the committed artifacts, so the headline claim can be independently checked with zero compute at all, and full Stage-1 re-extraction is explicitly documented as designed to fit an 8GB card. Preregistration docs (docs/preregistration*.md) and an append-only decision log (docs/decisions.md) are committed alongside the code, which is unusual rigor for a solo LessWrong-style project.

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
