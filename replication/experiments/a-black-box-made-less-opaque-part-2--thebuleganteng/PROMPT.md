# Replicate: A Black Box Made Less Opaque (part 2)

Source post: `Qnm6gAFnCPaJsbhSS` (2026-02-04, LW karma 6). Repo: `thebuleganteng/interpretability-prototyping` @ `5ef40554b9a1d7056ea3cfcd94319af0a8eedb3c`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In GPT-2 Small, pretrained residual-stream SAE 'specialist' features are primarily selective for syntax/surface form rather than semantics (mean Jaccard similarity of only 0.13 among top-5 specialist features across matched surface-form variants of the same meaning), whereas the overall SAE activation profile across all 24,576 features clusters primarily by semantic topic (within-topic cosine similarity 0.50 vs cross-topic 0.14), suggesting a two-tier syntax/semantics representational structure.

Supporting quote from the post: "the overall mean Jaccard similarity was a very modest 0.13. This limited specialist feature overlap is indicative of syntax-focused specialist features."

**Headline metric:** Jaccard similarity of top-5 specialist SAE features across matched surface forms; cosine similarity of overall SAE activation within-topic vs cross-topic
**Claimed value:** mean Jaccard similarity across surface forms = 0.13; within-topic cosine similarity = 0.50 vs cross-topic cosine similarity = 0.14
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `notebooks/phase_2_semantics_vs_ideas_v2.ipynb` (confidence: high)
- Produces: Jaccard similarity of top-5 specialist SAE features across matched surface-form pairs, and within-topic vs. cross-topic cosine similarity of the full SAE activation vector, both computed directly in phase_2_semantics_vs_ideas_v2.ipynb.
- Models: gpt2 (0.124B)
- Estimated VRAM: 1 GB — requirements.txt pins torch==2.9.0+cpu (a CPU-only build); the notebook explicitly loads HookedTransformer.from_pretrained('gpt2-small', device='cpu'). No GPU is used at all for this phase (Phase 3, Gemma-2-9B, is a separate Colab notebook not part of this post).
- Data: hardcoded matched-pairs text dataset (Python/math/etc. surface-form variants), written in notebook cells, jbloom/GPT2-Small-SAEs-Reformatted SAEs via sae_lens; availability: in-repo
- Estimated runtime: minutes (GPT-2-small forward passes plus SAE encoding over a small hardcoded set of matched-pair prompts; cached intermediate activations are already committed in notebooks/phase2_master_cache/*.pt (each well under 1MB).)
- Stated compute in the repo: none
- Known blockers: none recorded
- Inspector's notes: Cleanest repo of the batch: exact pinned pip freeze, explicit CPU-only torch, a 124M-parameter model, and cached intermediate activations already committed. Trivially reproducible even without a GPU.

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
