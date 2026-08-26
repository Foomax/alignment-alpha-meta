# Replicate: Probing is not enough; a validity audit for any probe

Source post: `wASHN8guJag7NhhJJ` (2026-07-07, LW karma 7). Repo: `ratnaditya-j/sieve-audit` @ `23ba7f5b53b3274bb84f9a6f364dc1217e78efc3`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A monitoring-awareness probe achieving AUROC 1.00 collapsed to 0.50 when a single leakage-inducing prompt tag was removed (versus only 0.88 for a random-span-removal control), showing the probe was reading a surface-level cue rather than internal model state; motivated by this and similar cases, the author builds SIEVE, a framework that audits any probe for decodability, necessity (ablation), and causal sufficiency (steering) before it can be trusted as a safety signal.

Supporting quote from the post: "the AUROC dropped to 0.50... Indicating clear leakage - The probe was reading a giveaway in the input and NOT a mointored-or-not state in the model."

**Headline metric:** AUROC of a monitoring-awareness probe under targeted vs random text removal
**Claimed value:** AUROC 1.00 -> 0.50 when the <is_free_tier_user> tag is removed; AUROC only drops to 0.88 when a random span of equal length is removed
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `examples/vlaf_alignment_faking/pod_run.sh, steps 1 (decode-lofo) and 6 (leakage) via src/sieve_audit/adapters/hf_steering_runner.py` (confidence: high)
- Produces: examples/vlaf_alignment_faking/reports/REPORT.md, Table 2.2 (Leakage): full text AUROC 1.000 -> tag removed 0.500 -> random equal-length span removed 0.917
- Models: allenai/OLMo-2-1124-7B-Instruct (7.0B)
- Estimated VRAM: 16 GB — repo's own stated figure: ~14GB BF16 weights for the 7B model used in this exact experiment, plus activation overhead for batched forward passes
- Data: VLAF moral-dilemma scenarios (launchnlp/VLAF, arXiv 2604.20995, fetched at runtime by prepare_prompts.py), Sorry-Bench (off-distribution eval, optional for the headline number); availability: download-script
- Estimated runtime: minutes-hours (decode-lofo and leakage are forward-pass-only over a few hundred short prompts on a 7B model; no walltime is stated but this is small relative to the full 9-stage pod_run.sh pipeline)
- Stated compute in the repo: pod_run.sh comment: 'Model: allenai/OLMo-2-1124-7B-Instruct (~14 GB BF16; fits A40 48 GB)'
- Known blockers: Model mismatch: assignment/post attributes this result to a monitoring-awareness probe but does not name a model in the post text; the assignment metadata says Qwen2.5-1.5B-Instruct while the actual in-repo experiment reproducing the exact <is_free_tier_user>-tag claim runs on allenai/OLMo-2-1124-7B-Instruct; The repo's own random-span-control AUROC (0.917) differs from the post's stated figure (0.88) - re-running as scripted would not reproduce the exact 0.88 number cited in the post; prepare_prompts.py fetches VLAF scenarios from GitHub at runtime, requiring internet access
- Inspector's notes: This is one of the cleaner repos in the batch: the specific headline claim (tag-removal leakage collapse) is fully scripted, GPU-light, and needs no closed-model API on its own, even though the surrounding SIEVE causal-sufficiency pipeline does. Either candidate model (7B or 1.5B) comfortably fits a 3090.

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
