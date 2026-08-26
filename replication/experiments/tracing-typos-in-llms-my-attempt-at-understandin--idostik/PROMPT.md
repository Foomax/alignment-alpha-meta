# Replicate: Tracing Typos in LLMs: My Attempt at Understanding How Models Correct Misspellings

Source post: `523bkuMjSjKjG8jn6` (2025-02-02, LW karma 12). Repo: `idostik/llm-typos-interpretability` @ `4f52a47ac2de5851051a68de1bc4a7864fe5be13`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A single attention head (L0H3) in Llama-3.2-1B, a 'subword merging head' that moves information between subword tokens of the same word, is the primary component responsible for typo correction when no surrounding context is available; ablating it breaks typo correction (measured via logit difference) while leaving normal text and general MLP-driven performance unaffected.

Supporting quote from the post: "With this setup, only the subword merging head (L0H3) shows a significant impact. That suggests, that the previous plot with loss was a bit misleading and that the loss was probably influenced by other factors."

**Headline metric:** logit difference change upon single-head ablation
**Claimed value:** only the subword merging head (L0H3) showed a significant impact on logit difference when ablated one-by-one across all attention heads
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `llm-typo-experiment.ipynb (per-head ablation loop / logit-difference cells)` (confidence: high)
- Produces: Notebook cells computing logit-difference before/after ablating each attention head one-by-one, identifying L0H3 as the only head with significant impact
- Models: meta-llama/Llama-3.2-1B (1.2B, gated)
- Estimated VRAM: 4 GB — 1.2B-param model, forward-only ablation passes over short hand-written sentences -- trivial for 24GB.
- Data: hand-written sentence lists embedded directly in the notebook; availability: in-repo
- Estimated runtime: minutes (Small model, small hand-curated prompt sets, per-head ablation sweep over ~16 heads x few layers -- no large corpus or training loop.)
- Stated compute in the repo: none
- Known blockers: No requirements.txt/environment file -- dependency versions are entirely unpinned (%pip install with no version numbers); the notebook appears Colab-authored (login("Your hf token") placeholder, inline package installs).
- Inspector's notes: Single unpolished exploratory notebook (README calls it 'rough, unpolished'), 104 cells, no separate scripts. Cheap to rerun; main risk is environment drift from unpinned transformer_lens/circuitsvis versions, not compute. No closed-API usage found.

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
