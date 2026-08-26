# Replicate: What We Learned Trying to Diff Base and Chat Models (And Why It Matters)

Source post: `xmpauEXEerzYcJKNm` (2025-06-30, LW karma 106). Repo: `science-of-finetuning/diffing-toolkit` @ `e0b84a591f5184d69a65082e4366ccfe36f47661`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Standard L1-trained crosscoders hallucinate most of their apparent 'chat-only' latents due to shrinkage and latent-decoupling artifacts; switching to BatchTopK crosscoders and, further, diff-SAEs trained on chat-base activation differences recover far more of the true behavioral difference between base and chat models (88% of the KL gap for diff-SAEs vs 60% for crosscoders).

Supporting quote from the post: "Crosscoders leave significant behavioral differences on the table: when we use the crosscoder's full reconstruction of the difference, we only recover 60% of the KL gap."

**Headline metric:** % of behavioral KL gap recovered
**Claimed value:** 60% (crosscoder reconstruction) vs 88% (diff-SAE reconstruction)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `uv run python main.py diffing/method=kl (and diffing/method=crosscoder, diffing/method=sae_difference) organism=chat model=<gemma-2-2b config> -- no ready-made gemma-2-2b model/organism config exists at this SHA, would need to be authored from an existing configs/model/*.yaml template` (confidence: low)
- Produces: KL-divergence-recovery outputs of diffing/method=kl run against crosscoder vs. sae_difference reconstructions (the post's 60% vs 88% KL-gap-recovered numbers); no committed artifact at this SHA reproduces those exact numbers
- Models: google/gemma-2-2b (2.6B, gated), google/gemma-2-2b-it (2.6B, gated)
- Estimated VRAM: 14 GB — Base + chat-tuned gemma-2-2b loaded simultaneously for activation-difference extraction (~10GB bf16 combined) plus a small dictionary-learning model (crosscoder / diff-SAE) trained on cached activations; preprocessing pipeline caches activations to disk for large corpora rather than holding them all in VRAM
- Data: large text corpus for preprocessing activation caching (dataset unspecified for this exact experiment at current SHA); availability: unknown
- Estimated runtime: hours (README describes the preprocessing pipeline as 'compute-intensive' (extracting/caching activations over millions of samples) but gives no concrete wallclock; crosscoder/SAE training on cached 2B-model activations is typically a few-hour job on a single consumer GPU)
- Stated compute in the repo: none
- Known blockers: The toolkit has moved on since the June 2025 post: configs/model/ at this SHA only has gemma2_9B_it, gemma3_1B(_pt), gemma3_4B_it, gemma3_27B_it -- no gemma2_2B config remains, so a competent engineer would need to reconstruct the original base-vs-chat gemma-2-2b experiment config themselves (feasible, since the framework is generic, but not turnkey).; The separate agentic-evaluation feature (LLM agent + LLM grader, e.g. GPT-4/Claude) does need a closed API key, but it is not required for the specific KL-gap-recovery headline metric.
- Inspector's notes: This is a general, actively-developed toolkit (the linked publication is one of several) rather than a frozen paper-specific repo, so entrypoint confidence is low: the code paths (kl, crosscoder, sae_difference methods) clearly exist and match the post's method names, but the exact gemma-2-2b base/chat config used for the original blog post is not preserved at the given head_sha. A separate, unrelated 'Narrow Finetuning' paper reproduction in the same repo explicitly assumes a SLURM cluster.

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
