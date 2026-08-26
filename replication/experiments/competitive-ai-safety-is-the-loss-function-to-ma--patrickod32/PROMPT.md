# Replicate: Competitive AI Safety is
the loss function to make sure AI goes well

Source post: `PagGF8roBJmjLunsX` (2026-07-16, LW karma 4). Repo: `patrickod32/seq2feature` @ `f0616acd25cdf88a3c8c50e5786df5c45072d327`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> seq2feature, a 5.3MB text-only probe distilled from a Gemma-2-9B SAE, recovers the SAE's concept readout from output text alone with 0.956 top-5 concept agreement and 0.90 per-concept AUC, beating bag-of-words (0.84/0.75) and zero-shot embedding (0.23/0.53) baselines, while running on CPU and degrading legibly out of distribution.

Supporting quote from the post: "My seq2feature 5.3MB text-only probe reproduces 90% of the capability of an SAE on held out text."

**Headline metric:** top-5 concept agreement with SAE ground truth / per-concept AUC
**Claimed value:** 0.956 top-5 agreement, 0.90 AUC (seq2feature int8, 5.3MB) vs 0.84/0.75 bag-of-words, 0.23/0.53 embedding baseline, 1.00/1.00 SAE teacher
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 12 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `notebooks/02_evaluate_probe.ipynb` (confidence: high)
- Produces: notebooks/02_evaluate_probe.ipynb primary figure and printed summary -- per-concept AUC (0.90) and top-5 agreement (0.956) vs bag-of-words (0.84/0.75) and zero-shot embedding (0.23/0.53) baselines
- Models: Gemma 9B
- Estimated VRAM: 0 GB — The headline-number notebook (02_evaluate_probe.ipynb) is explicitly CPU-only and needs neither the 9B base model nor the SAE -- it compares the shipped 5.3MB probe against pre-computed SAE ground-truth firings already saved in relabel_bundle/targets.npz. Probe training (01_train_probe.ipynb) needs a GPU but only for 'minutes' on a 1.5M-parameter probe.
- Data: relabel_bundle/ (SAE firings, spans, concept captions), golf_final/ (trained probe weights); availability: in-repo
- Estimated runtime: minutes (README/notebook comments state CPU scoring takes ~1-2 minutes and probe training takes 'minutes on a GPU' (Colab).)
- Stated compute in the repo: '01_train_probe.ipynb trains the probe from relabel_bundle/ (Colab, ~minutes on a GPU); 02_evaluate_probe.ipynb reproduces the baseline table and accuracy above on CPU, no GPU needed.' Notebook comment: '# 3 - load the probe, score every span (CPU ~1-2 min)'.
- Known blockers: none recorded
- Inspector's notes: Best case in this batch: the exact headline metrics reproduce on CPU in minutes from data already committed to the repo. The only compute/API-heavy step in the whole project -- running the Gemma-2-9B teacher + GemmaScope SAE to generate ground-truth labels (README: needs an A100/80GB) and captioning 2048 concepts via Gemini 2.5 Flash Lite (~$0.80, needs OPENROUTER_KEY) -- is a one-time upstream step whose outputs (relabels.jsonl, targets.npz) are already shipped and not required to reproduce the reported numbers.

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
