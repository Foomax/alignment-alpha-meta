# Replicate: Matryoshka NLAs: training activation verbalizers to frontload reconstruction-relevant information

Source post: `aWYQHh2pEFCLYh85C` (2026-08-06, LW karma 29). Repo: `syvb/natural_language_autoencoders` @ `85399df1cb1340875e45036e6a5432a029cfe07a`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A 'matryoshka' Natural Language Autoencoder, trained by randomly truncating verbalizer explanations during RL, frontloads reconstruction-relevant information relative to a standard NLA (captures most of its fraction-of-variance-explained in the first few bullet lines, and better predicts held-out suffix text under short truncations), and reveals higher-strength concurrently-applied steering vectors earlier in its explanation list, though there is no strong evidence it is significantly more useful than standard NLAs overall.

Supporting quote from the post: "We find that our matryoshka NLA frontloads claims that are important to reconstruction (more than standard NLAs), and that this can be used as a heuristic for saliency of the represented feature."

**Headline metric:** fraction of variance explained (FVE) vs. truncation length; suffix-prediction accuracy
**Claimed value:** matryoshka NLA captures most FVE within the first few bullet lines (marginal FVE decays roughly exponentially, negligible past line 3); outperforms standard NLA on suffix prediction under short (<16 token) truncations, roughly matches it for longer truncations
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/qwen2.5-matryoshka-warmstart-sonnet46/fve_truncation_sweep/setup_box.sh (download released checkpoints) -> sweep_fve.py (per-truncation-length round-trip FVE sweep) -> plot.py` (confidence: high)
- Produces: results/token_fve.csv and lines_fve.csv (front-loading FVE-vs-truncation curves for warm-start vs. RLed-truncation vs. kitft control), matching the assignment's claim about matryoshka NLA frontloading reconstruction-relevant information
- Models: Qwen/Qwen2.5-7B-Instruct (base) (7B), kitft/nla-qwen2.5-7b-L20-av / -ar (published control checkpoints) (7B), syvb/nla-qwen2.5-7b-L20-rltrunc-gradguard, syvb/nla-qwen2.5-7b-L20-{av,ar}-matryoshka-sonnet46 (author's own checkpoints, downloaded with the author's personal HF token in setup_box.sh) (7B)
- Estimated VRAM: 15 GB — README states explicitly: '7B bf16 inference ~=15GB; AV and AR loaded one at a time'; sweep_fve.py frees the AV model (del/gc/empty_cache implied by the 'auto-frees the AV after generation' note) before the AR critic is used, so the two 7B models are never resident simultaneously.
- Data: av_eval.parquet (100 held-out samples), hosted as an HF dataset: syvb/nla-qwen2.5-7b-L20-matryoshka-warmstart-sonnet46; availability: hf-hub
- Estimated runtime: ~15 minutes (stated) (README: "Whole thing is ~15 min of compute + downloads, ~$0.10-0.15" on a rented 48GB A6/A40.)
- Stated compute in the repo: "A 48 GB GPU is plenty (7B bf16 inference ~= 15 GB; AV and AR loaded one at a time). Whole thing is ~15 min of compute + downloads, ~$0.10-0.15." (fve_truncation_sweep/README.md)
- Known blockers: setup_box.sh downloads several 'syvb/...' checkpoints and the eval parquet using the repo author's own personal HF_TOKEN; it is unclear whether these specific repos (as opposed to the published 'kitft' control checkpoints) are actually public without requesting access; the RLed AR checkpoint's exported value_head.safetensors is documented as corrupt (~12% NaN weights) and requires a manual swap-in of a different checkpoint's clean head, per the README's own workaround
- Inspector's notes: The assignment's model field says 'Qwen 27B (3.6)', but the actual matryoshka-NLA experiment in this repo (directory qwen2.5-matryoshka-warmstart-sonnet46) is built on Qwen2.5-7B-Instruct at layer 20/28, not a 27B or 3.6-series model -- likely a metadata extraction error upstream, not a repo issue. This is otherwise an unusually well-documented repo: the README states exact VRAM (~15GB), runtime (~15min), and dollar cost (~$0.10-0.15) for reproducing the headline FVE-vs-truncation result from already-released checkpoints, with no GPU training or closed-API call needed for this specific figure.

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
