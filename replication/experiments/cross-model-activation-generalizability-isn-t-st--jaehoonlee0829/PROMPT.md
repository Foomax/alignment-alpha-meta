# Replicate: Cross-Model Activation Generalizability Isn't Strong (Yet)

Source post: `S9xyqRAziRMCcJQmz` (2026-04-06, LW karma 7). Repo: `jaehoonlee0829/cross-model-alignment-geometry` @ `bfacecff2e21872a839ab4fb1dc54ed901d684f6`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Cross-architecture activation similarity between small LLMs (1-3B, Llama/Gemma/Qwen/Pythia) is statistically significant (debiased CKA up to ~0.22, p<0.002 by permutation test) but weak, 4-9x lower than within-family similarity (up to 0.91), and linear bridges built on this cross-architecture structure transfer only coarse binary-classification signal and largely fail at next-token prediction, challenging the Platonic Representation Hypothesis at this scale.

Supporting quote from the post: "Cross-architectural activation similarity is statistically real, but weak. Within-family activations are much stronger (4~9x)... Not enough for fine grained auditing tools."

**Headline metric:** debiased CKA / linear-bridge probe transfer accuracy
**Claimed value:** cross-family max debiased CKA ~0.18-0.22 (mean 0.05-0.11) vs within-family max 0.914 (mean 0.605); within-family binary classification transfer reaches >90% of target-native accuracy at high rank, cross-family transfer plateaus below target-native and is inconsistent across tasks; cross-family next-token top-1 transfer caps at 4.9% vs within-family 93% of oracle
**Direction of the claim:** 0
**Uncertainty the post reported:** ci
**Tolerance for "reproduced":** `manual` — headline is a compound of 10 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/run_corrected_permutation_tests.py` (confidence: high)
- Produces: README tables 'Cross-family CKA is weak, within-family is strong' and 'Permutation tests confirm statistical significance' (max/mean debiased CKA per eval, p<0.002); probe-transfer tables for binary/NTP/POS transfer
- Models: meta-llama/Llama-3.2-1B (1.0B, gated), meta-llama/Llama-3.2-3B (3.0B, gated), google/gemma-2-2b (2.0B, gated), Qwen/Qwen2.5-1.5B (1.5B), EleutherAI/pythia-1.4b (1.4B), EleutherAI/pythia-2.8b (2.8B)
- Estimated VRAM: 10 GB — Models loaded one at a time in fp16 (src/activation_extraction.py: torch_dtype=torch.float16) for activation extraction; largest is 3B (~6GB weights) + batch=32 (16 for 3B) x seq_len=128 hidden-state activations. CKA/alignment fitting afterward is CPU/GPU numpy-scale linear algebra on cached activations, not model-resident.
- Data: NeelNanda/pile-10k, AG News, ToxiGen, SST-2; availability: hf-hub
- Estimated runtime: hours (5 model-pair evals x activation extraction (10k prompts, 9 layers) + 500-permutation CKA null + multi-method (Procrustes/ridge/LASSO/low-rank at 7 ranks) alignment fits; stated compute was a single A40, no wall-clock time given, but this is a full day's worth of small-model inference-only work, not multi-day.)
- Stated compute in the repo: All experiments were run on a single NVIDIA A40 (48 GB) GPU via RunPod, with random seed 42.
- Known blockers: Gemma-2-2b and Llama-3.2 require accepting gated licenses on HuggingFace and an HF_TOKEN; Headline number is spread across ~6 scripts (run_cka.py, run_corrected_permutation_tests.py, run_dual_probe_transfer.py, run_pos_probe_transfer.py, run_probing.py) rather than one entrypoint; a full replication means running all of them and matching README's reported values
- Inspector's notes: Very thoroughly documented (README + RESEARCH_REPORT.md with explicit compute/method/limitations sections). All 6 models are 1-3B scale, fp16 inference only (no training), so the whole pipeline is well within a 24GB card despite being run on a 48GB A40 in practice.

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
