# Replicate: Linear probes tell you where quantization will hurt

Source post: `oJJyYDgPD95jEfvQx` (2026-07-25, LW karma 29). Repo: `itsme-aniketghosh/probe-guided-quantization` @ `457ecfa2a5025310fe64e5ecc975d43d211011fc`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A per-layer linear-probe map of where a syntactic/semantic signal (POS, NER, chunking) is built in BERT-family encoders predicts where quantization damage lands, and using this map to guide per-layer bit allocation preserves 99-100% of full-precision accuracy at a 5-bit average budget on three datasets never used to build the map, versus 16-41% for uniform quantization and 2-41% for anti/opposite-layer allocation, with the same pattern replicating on a decoder LLM (Qwen2.5-3B), where the guided split preserves F1 down to about 3 bits per layer on average versus uniform needing about 8.

Supporting quote from the post: "a map built once on CoNLL news keeps 99–100% of full-precision accuracy at a 5-bit average on three unseen datasets, whereas Uniform kept 16–41% and opposite/anti layers kept 2–41%."

**Headline metric:** accuracy retained at a 5-bit average budget on unseen datasets, guided vs uniform vs anti/opposite layer allocation
**Claimed value:** guided: 99-100% (100% web-text POS, 99% tweet NER, 100% WSJ chunks); uniform: 16-41%; anti/opposite: 2-41%; on Qwen2.5-3B, guided split preserves F1 down to ~3 bits/layer average vs uniform needing ~8 bits
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 14 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `05_transfer.ipynb` (confidence: high)
- Produces: 05_transfer.ipynb's fig_transfer.png (100% web-text POS, 99% tweet NER, 100% WSJ chunks guided vs 16-41% uniform vs 2-41% anti/opposite); 06_decoder.ipynb's fig_decoder_recipe.png for the Qwen2.5-3B guided-vs-uniform bit budget
- Models: bert-base-uncased (0.11B), bert-large-uncased (0.34B), roberta-base (0.125B), distilbert-base-uncased (0.066B), Qwen/Qwen2.5-3B-Instruct (3.0B)
- Estimated VRAM: 6 GB — BERT-family models are all <350M params (trivial VRAM); Qwen2.5-3B-Instruct in fp16/bf16 needs ~6-7GB for weights + activations; README only claims a Colab GPU (typically a 16GB T4) suffices, well under a 3090's 24GB
- Data: CoNLL-2003 (build the map), WNUT-17 (NER transfer), Universal Dependencies EWT (POS transfer), CoNLL-2000 (chunk transfer); availability: hf-hub
- Estimated runtime: hours (TRAIN_SENTS/VAL_SENTS constants (3000/800 for BERT notebooks, 600/200 for the Qwen2.5-3B decoder notebook) imply modest feature-extraction + sklearn RidgeClassifier runs; README says each notebook fits a single Colab session)
- Stated compute in the repo: every notebook runs top to bottom on a Colab GPU
- Known blockers: notebooks call google.colab.drive.mount(...) for caching — needs a one-line swap to a local path to run outside Colab; no pinned dependency versions anywhere (only an inline 'pip install -q' with no version constraints)
- Inspector's notes: Best-documented repo in this batch: README prose walks through every headline number, all data is public HF datasets, and every model (BERT-family + Qwen2.5-3B) is small. Only friction is Colab-specific Drive-mount caching code.

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
