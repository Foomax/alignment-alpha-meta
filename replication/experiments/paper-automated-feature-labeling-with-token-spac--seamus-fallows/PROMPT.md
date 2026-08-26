# Replicate: [Paper] Automated Feature Labeling with Token-Space Gradient Descent

Source post: `Eu96GFW6LKrQHCJbs` (2025-04-30, LW karma 4). Repo: `seamus-fallows/automated-feature-labeling` @ `f6f16747b57f81b9b91b6ebb1c4a9bd128477494`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Directly optimizing a feature label via token-space gradient descent, using an LLM as a differentiable discriminator rather than a hypothesis generator, converges to correct single-token labels for several synthetic toy features (animal, Chinese text, number, and mammal under balanced sampling), but defaults to broader categories under unbalanced sampling and fails when the base model cannot reliably classify the concept (e.g. palindromes).

Supporting quote from the post: "The method successfully labeled features like "animal," "mammal," "Chinese," and "number" in our proof-of-concept experiments"

**Headline metric:** label-convergence success across tested synthetic features
**Claimed value:** converged to the correct single-token label for animal, Chinese, number, and mammal (balanced sampling); failed to find the correct label for mammal under unbalanced natural-text sampling (defaulted to 'animal') and for palindrome detection (defaulted to 'a')
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is not a single scalar; judge by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/animals.py` (confidence: medium)
- Produces: trainings_logs.plot_final_token_accuracy / plot_top_tokens outputs from each experiments/*.py script (one script per concept: animals.py, chinese.py, numbers.py, mammals.py, mammals_words.py, palindromes.py), showing convergence (or failure) to the target single-token label
- Models: meta-llama/Meta-Llama-3-8B-Instruct (8B, gated)
- Estimated VRAM: 20 GB — No torch_dtype is specified anywhere in the codebase (AutoModelForCausalLM.from_pretrained(...).to(device) with no dtype arg), which loads Llama-3-8B-Instruct in fp32 by default: ~32GB of weights alone, exceeding 24GB. Switching to bf16 (a one-line fix, since only a soft concept-embedding is trained and the 8B model stays frozen) would bring this to roughly 18-22GB including backprop activations.
- Data: animals, mammals, chinese, numbers, palindromes text data; availability: in-repo
- Estimated runtime: unknown (No compute stated; batch_size=20, epochs=5, with sentence-activation caching (CachedDataset) to avoid repeated full-model forward passes.)
- Stated compute in the repo: none
- Known blockers: As coded, loads an 8B model in fp32 (~32GB) which does not fit a 24GB 3090 without a manual bf16/fp16 edit; Hardcoded HuggingFace token string ('llama_token') committed in multiple files (likely already revoked, but a code smell); No single unified entrypoint -- each concept/claim (animal, Chinese, number, mammal balanced/unbalanced, palindrome) is a separate standalone script
- Inspector's notes: Method itself is cheap (only a d_vocab-sized soft token vector is trained via gradient descent; the 8B model is frozen), so the VRAM issue is a trivial dtype fix, not a fundamental blocker. All text data for every claimed sub-experiment is already committed under data/text_data/.

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
