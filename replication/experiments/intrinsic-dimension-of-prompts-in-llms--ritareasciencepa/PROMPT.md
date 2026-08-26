# Replicate: Intrinsic Dimension of Prompts in LLMs

Source post: `oBpjE4BDJf6qzz4E5` (2025-02-14, LW karma 3). Repo: `ritareasciencepark/token_geometry` @ `02148974cd39ff7f186e734dd1e9113ed42ee614`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> The intrinsic dimension of token representations within a prompt correlates positively with next-token surprisal (cross-entropy loss) across layers in GPT-2, Pythia, Llama, and OPT, and correlates positively with TunedLens latent-prediction entropy in GPT-2 and Pythia, though Llama shows a moderate negative correlation around layer 20 instead.

Supporting quote from the post: "All four models have a high positive correlation across the layers of the model, implying that prompts with a higher average surprisal have a higher intrinsic dimension."

**Headline metric:** Pearson correlation (rho) between intrinsic dimension and TunedLens latent prediction entropy
**Claimed value:** rho > 0.5 for GPT-2 (early layers) and Pythia (middle layers onward); rho ~ -0.5 for Llama around layer 20; no positive correlation for Llama/OPT until late layers
**Direction of the claim:** 0
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 4 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/extract_id.py (ID vs. loss); src/benchmarks/compute_entropy.py (TunedLens entropy, undocumented in README)` (confidence: medium)
- Produces: results/Pile-Structured/<model>/gride.npy (intrinsic dimension per layer) correlated against loss.npy via post_process/plot_id_loss_correlation.py; TunedLens entropy specifically comes from src/benchmarks/compute_entropy.py (not documented in the README, hardcoded to meta-llama/Meta-Llama-3-8B only, and appears to contain a bug: `benign, jailbreak = []` will raise on unpacking).
- Models: gpt2 (0.124B), gpt2-large (0.774B), gpt2-xl (1.5B), EleutherAI/pythia-160m-deduped (0.16B), EleutherAI/pythia-410m-deduped (0.41B), EleutherAI/pythia-1.4b-deduped (1.4B), EleutherAI/pythia-2.8b-deduped (2.8B), EleutherAI/pythia-6.9b-deduped (6.9B), facebook/opt-6.7b (6.7B), mistralai/Mistral-7B-v0.1 (7.0B), meta-llama/Meta-Llama-3-8B (8.0B, gated)
- Estimated VRAM: 28 GB — load_model() in extract_id.py calls AutoModelForCausalLM.from_pretrained(model_name).to(device) with no torch_dtype specified, so it loads fp32. GPT-2/small Pythia trivially fit; the 7-8B models (Llama-3-8B, Mistral-7B, OPT-6.7b, Pythia-6.9b) need ~26-32GB in fp32, exceeding 24GB.
- Data: Pile-10K (NeelNanda/pile-10k), filtered to 2244 prompts of >=1024 tokens; indices bundled as filtered_indices.npy / subset_indices.npy; availability: hf-hub
- Estimated runtime: unknown (README states an A100 64GB was used but gives no wall-clock time; GRIDE computation does an O(N^2) pairwise-distance matrix per 1024-token prompt per layer, which is CPU/dadapy-heavy independent of the GPU forward pass.)
- Stated compute in the repo: All experiments were run on an NVIDIA A100 GPU with 64 GB memory.
- Known blockers: No requirements.txt/pyproject.toml/environment.yml anywhere in the repo — dependency versions (torch, transformers, dadapy, skdim, tuned_lens) are entirely unpinned.; The 7-8B models used for the headline Llama-3-8B correlation need a one-line dtype change (fp32→bf16) to fit a single 24GB 3090, since the repo's default load is fp32.; compute_entropy.py, the only script referencing TunedLens (needed for the specific rho vs. TunedLens-entropy metric in the assignment), is not mentioned in the README, is hardcoded to Llama-3-8B only (not GPT-2/Pythia/OPT), and has an apparent bug on the line `benign, jailbreak = []`.
- Inspector's notes: The published, README-documented pipeline (extract_id.py + post_process/) reproduces the ID-vs-loss-surprisal correlation cleanly and ships precomputed .npy results for all listed models. The TunedLens-entropy correlation specifically (part of this assignment's target metric) relies on a separate, undocumented, buggy, Llama-3-8B-only script.

## Budget

**90 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
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
