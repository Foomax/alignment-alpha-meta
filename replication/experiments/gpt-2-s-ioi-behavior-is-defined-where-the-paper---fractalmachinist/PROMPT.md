# Replicate: GPT-2's IOI behavior is defined where the paper's algorithm isn't

Source post: `zKyKDre78napvtrEo` (2026-08-18, LW karma 7). Repo: `fractalmachinist/ioi` @ `1571259a3a8e713abd4cdd3758613f41769304ba`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In GPT-2 small's IOI circuit, incidentally duplicating the indirect-object name in an unrelated modifier slot causes Duplicate Token Heads to fire on it almost as strongly as on a genuine subject duplicate, yet this produces only a small drop in the IO/S logit difference (mean 0.23, Cohen's d=0.27) and accuracy barely changes (95.4% to 94.5%), because S-Inhibition heads mostly continue attending to the real S2 token rather than the incidental duplicate

Supporting quote from the post: "The drop in IO/S logit difference is small: mean 0.23, SD 0.84 pair-to-pair (n = 128), paired t = 3.09, p = 0.0024... A real effect, but not a big one. The model's accuracy (how often it predicts IO as more likely than S) moves from 95.4% ("

**Headline metric:** drop in IO/S logit difference between control and test (incidental duplicate) conditions; task accuracy
**Claimed value:** mean drop 0.23, SD 0.84 (n=128 matched pairs), paired t=3.09, p=0.0024, Cohen's d=0.27; accuracy 95.4% (control) vs 94.5% (test)
**Direction of the claim:** 0
**Uncertainty the post reported:** se
**Tolerance for "reproduced":** `manual` — headline is a compound of 8 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments.ipynb` (confidence: high)
- Produces: experiments.ipynb, Experiment 1 (cell 12-15): paired scatter of test vs. control IO/S logit difference + stats cell (cell 13: ttest_rel, cohen's d implicit) matches target_value's mean drop 0.23, SD 0.84, n=128, paired t=3.09, p=0.0024
- Models: gpt2 (gpt2-small via transformer_lens HookedTransformer.from_pretrained) (0.124B)
- Estimated VRAM: 2 GB — GPT-2 small (124M params) loaded via TransformerLens with full attention-pattern caching for batched forward passes; trivially small model, negligible VRAM even with activation caching for hundreds of prompts.
- Data: templated sentences generated in-repo from ioi_dataset.py (NAMES, OBJECTS, PLACES, NAMEABLE_PLACE_NAMES/WORDS, BABA_TEMPLATES); availability: in-repo
- Estimated runtime: minutes (SIZE='medium' in experiments.ipynb -> n_templates=8 x n_pairs=16 = 128 matched pairs (matches assignment's stated n=128), run as a handful of same-length batched forward passes through GPT-2 small plus statistical tests (paired t-test, Wilcoxon, KS, Mann-Whitney, permutation) on cached logit diffs -- this is a light workload for one small model.)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: No requirements.txt/pyproject, but deps are unambiguous from imports (transformer_lens, torch, scipy, matplotlib). README.md is a single line ('# IOI'); all documentation lives in the notebook's markdown cells, which are unusually thorough and directly state the falsifiable hypothesis and n. SIZE='medium' in cell 4 is exactly the config that reproduces the assignment's n=128 pairs; 'full' (n=360 pairs) or 'quick' (n=32) are also one-line switches.

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
