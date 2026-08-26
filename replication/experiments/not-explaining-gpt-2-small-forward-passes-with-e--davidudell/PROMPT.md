# Replicate: (Not) Explaining GPT-2-Small Forward Passes with Edge-Level Autoencoder Circuits

Source post: `2CoLkSdwirr2WnNH6` (2025-07-22, LW karma 23). Repo: `davidudell/sparse_circuit_discovery` @ `85114b1e6a1e2607c66d566e761c01c0c532b1b6`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A replication of a gradient-based unsupervised sparse-autoencoder circuit discovery algorithm in GPT-2-small produced a negative result: only 2 of 5 top proximal-cause SAE features correctly predicted the model's actual top next token, and the upstream edges/nodes feeding into them remained largely uninterpretable, so localistic SAE circuits could not be strung together into fully explanatory circuits.

Supporting quote from the post: "A replication of an unsupervised circuit discovery algorithm in GPT-2-small, with a negative result."

**Headline metric:** fraction of top proximal-cause SAE features correctly predicting the model's actual top next-token completion, across 5 example prompts
**Claimed value:** 2 of 5
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `sparse_coding/fast.py` (confidence: high)
- Produces: grads_graph.svg/.dot edge-level cognition graph from fast.py; the post's '2 of 5' figure comes from manually checking whether each graph's top proximal-cause features predict the model's actual top next token, across 5 separately-run prompts
- Models: openai-community/gpt2 (0.124B)
- Estimated VRAM: 9 GB — repo's own runtime VRAM self-check (fast.py) states ~8924 MiB for the default central_config.yaml ACTS_LAYERS_SLICE of '9:12'; the full 12-layer slice '0:12' needs ~30712 MiB, which would exceed a 3090
- Data: jbloom/GPT2-Small-OAI-v5-128k-resid-post-SAEs, jbloom/GPT2-Small-OAI-v5-128k-attn-out-SAEs, jbloom/GPT2-Small-OAI-v5-128k-mlp-out-SAEs (all via hf_hub_download); availability: hf-hub
- Estimated runtime: unknown (no wall-clock stated; script only self-checks VRAM before running a single forward+backward pass per layer pairing on GPT-2 small)
- Stated compute in the repo: fast.py comment: '30712 was my benched VRAM draw for the full model slice "0:12", with 6538 for the slice "10:12" and 8924 for the slice "9:12"'
- Known blockers: reproducing across the full 12-layer model (slice '0:12') exceeds a single 3090's VRAM per the repo's own benchmark; must restrict to narrower layer slices (author explicitly suggests halving) to fit; the post's '5 example prompts' evaluation isn't a single scripted entrypoint — PROMPT is one string in central_config.yaml, so covering 5 prompts means manually rerunning fast.py 5 times and manually checking predictions
- Inspector's notes: Unusually transparent repo: it measures its own VRAM via pynvml at startup and will refuse/downsize a run it judges too large for the available GPU, printing a suggested narrower layer slice instead of just OOM-ing.

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
