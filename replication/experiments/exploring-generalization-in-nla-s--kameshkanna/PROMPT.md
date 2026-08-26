# Replicate: Exploring Generalization in NLA's

Source post: `tkiSQBuA8yj2tHNdv` (2026-06-25, LW karma 14). Repo: `kameshkanna/nla-train` @ `0380fd87e7f3081558fd98478e7662e758f167ed`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A Natural Language Autoencoder's Activation Verbalizer trained only at layer 20 of Qwen2.5-7B generalizes without retraining to reconstruct activations from layers 10-25, beating both a random-noise baseline and a shuffled-correspondence baseline on cosine similarity, Recall@10, FVE, and nRMSE, while early layers (0-1) and late layer 27 fail to generalize.

Supporting quote from the post: "From L10 to L25 cosine similarity stays above 0.50, Recall@10 above 0.40, FVE positive, and nRMSE well below the baselines."

**Headline metric:** cosine similarity / Recall@10 / FVE / nRMSE for layer-20-trained AV reconstructing activations across layers, vs random and shuffled baselines
**Claimed value:** cosine similarity >0.50 and Recall@10 >0.40 from L10-L25; every layer significant vs random baseline (Wilcoxon signed-rank + Benjamini-Hochberg); L0, L1, L27 fail against the shuffled baseline
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 8 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/run_generalization.sh (extract_all_layers.py -> run_av_sweep.py -> run_ar_sweep.py -> compute_metrics.py -> plot_results.py)` (confidence: high)
- Produces: experiments/results/metrics.json + wilcoxon_results.json (per-layer cosine similarity / Recall@10 / FVE / nRMSE, Wilcoxon+BH significance) -> MODEL_CARD.md: 'layers 10-25 all achieve CS > 0.50 and Recall@10 > 0.40'
- Models: Qwen/Qwen2.5-7B-Instruct (7.6B), Kameshr/nla-qwen2.5-7b-L20-av (LoRA adapter, public) (7.6B)
- Estimated VRAM: 18 GB — Qwen2.5-7B-Instruct in bf16 (~15GB weights) plus KV-cache for batched generation (AV sweep default batch=256, tunable via --av-batch-size); inference-only for the generalization pipeline, no optimizer-state overhead.
- Data: HuggingFaceFW/fineweb (sample-10BT), wikimedia/wikipedia, ccdv/pubmed-summarization, iamtarun/python_code_instructions_18k_alpaca, Reddit domain (source not confirmed in repo); availability: hf-hub
- Estimated runtime: hours (56,000 AV inferences (2000 texts x 28 layers x 2 arms) plus AR reconstructions and 3 baselines, batched on one 7B model; wall-clock not stated for this stage (training stages are 1-7h each on H100).)
- Stated compute in the repo: Training env: 'Reproduces the Fraser-Taliente et al., 2026 pipeline on a single H100 for ~$35.' Model card: '1x H100 80GB, Lambda Labs' for the 3-stage training (AR SFT ~1h, AV SFT ~1.5h, RL GRPO ~7h). No compute stated for the generalization/inference pipeline itself.
- Known blockers: The AV checkpoint (Kameshr/nla-qwen2.5-7b-L20-av) is published on HF and directly downloadable, but the AR checkpoint the pipeline expects at checkpoints/ar_sft/final is NOT published under this project's namespace -- it must be retrained via scripts/run_ar_sft.sh, which first needs the multi-stage datagen pipeline (FineWeb extraction + a 'kitft' reference model as an oracle labeler).; AR SFT's H100-tuned settings (per_device_train_batch_size=64, gradient_checkpointing=false) assume ~64GB+ VRAM; would need a smaller batch size and gradient checkpointing enabled to fit a 24GB 3090.; Two separate, mutually-incompatible Python environments are required (nla-rl-env for training, nla-val-env for inference) due to a vLLM/transformers version conflict.
- Inspector's notes: The config references a 'kitft/nla-qwen2.5-7b-L20-ar' reference checkpoint (upstream paper release) as a validation baseline; if that happens to be public, a replicator could sidestep AR retraining, but that would substitute a different AR model rather than reproducing this project's own trained one. No closed-API calls found anywhere in the repo.

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
