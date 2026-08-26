# Replicate: Investigating echo tasks in Qwen 2.5-1.5B Instruct - part 1

Source post: `rs2BmwXWJEaEfNr2v` (2026-04-27, LW karma 1). Repo: `mild-rgb/qwen-2.5-1.5b-echo_repeat-investigation` @ `3c0bf77bcddb3dec0f23ddca7d0dc85ffa3068ed`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In Qwen-2.5 1.5B Instruct, echo/repeat tasks are resolved through an MLP-heavy circuit rather than late attention, with attention head 2 at the token-emergence layer consistently ranking among the top-3 most important heads across ablation experiments on 44 words and both prompt phrasings, and attending strongly (~90%) to the BOS token, likely as an attention sink.

Supporting quote from the post: "My most interesting discovery is that ablation results and DLA results disagree strongly in this task."

**Headline metric:** consistency of head 2 ranking top-3 in zero-ablation logit-drop experiments
**Claimed value:** head 2 always in top-3 heads across 44 words and both 'repeat'/'echo' prompt phrasings
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `2_copy_circuit_survey.ipynb` (confidence: high)
- Produces: 2_copy_circuit_survey.ipynb cell 7 (top3_head_frequency): tallies how often each attention head appears in the top-3 by direct-logit-attribution and by zero-ablation logit-drop, across all 44 COMMON_ENGLISH words and both echo/repeat conditions; cell 9 computes head-2's attention pattern (~90% to BOS) at each word's emergence layer.
- Models: Qwen/Qwen2.5-1.5B-Instruct (1.5B)
- Estimated VRAM: 6 GB — 1.5B-parameter model loaded via TransformerLens' TransformerBridge/HookedTransformer for cached forward passes and per-head zero-ablation; fp32 weights ~6GB, activations for single short prompts are negligible.
- Data: none listed; availability: in-repo (44-word list COMMON_ENGLISH is hardcoded in the notebook)
- Estimated runtime: minutes (44 words x 2 prompt phrasings (echo/repeat), each requiring a handful of cached forward passes plus per-head ablation on a 1.5B model — small workload for a single GPU.)
- Stated compute in the repo: none
- Known blockers: no requirements.txt — relies on inline !pip install transformer_lens / circuitsvis in Colab, versions unpinned; notebooks were authored for Google Colab and 'render weirdly outside of that environment' per the README, though the code itself has no Colab-specific dependencies beyond the install cell
- Inspector's notes: Small, self-contained, and the code directly matches the claim's specifics (44 words, both prompt phrasings, head 2, ~90% BOS attention). Straightforward to reproduce exactly on a single 3090 with no external data or API dependencies.

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
