# Replicate: Exploring Shard-like Behavior: Empirical Insights into Contextual Decision-Making in RL Agents

Source post: `fbw3PcLTGn53fxCM7` (2024-09-29, LW karma 6). Repo: `aristizabal95/procgen-tools` @ `49d4759a90b7d8d38ea03beb621f1ef501a7854a`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Cheese-seeking behavior in a maze-solving RL policy is spatially localized around the cheese's position, even though the presence of cheese is linearly decodable at near-perfect accuracy from activations at nearly every layer of the network; sensitivity of activations to cheese proximity is concentrated in later layers, especially the fully-connected layer preceding the value head.

Supporting quote from the post: "Our findings suggest that while all network layers consistently encode the presence of cheese, the effect of this information on the agent's behavior is spatially localized within the maze environment."

**Headline metric:** linear probe accuracy for cheese-presence detection across network layers
**Claimed value:** near-perfect accuracy in most layers, dropping to 90% at the policy head
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `experiments/probing_main.py` (confidence: medium)
- Produces: experiments/probing_main.py/.ipynb per-layer linear probe accuracy table/plot for cheese-presence detection
- Models: ? (0.0006B)
- Estimated VRAM: 2 GB — Small IMPALA-CNN procgen maze policy (order 10^6 params) plus forward-pass activation caching (via circrl hooks) over a batch of collected maze observations for probe fitting — negligible relative to 24GB; the probes themselves are sklearn/CPU.
- Data: pretrained IMPALA maze policies (maze_I/*.pth) from Langosco et al., public Google Drive link in README, rollout/observation datasets for probing, generated on the fly via env simulation (gatherdata_*.py / probing_gather.py), not shipped as static files; availability: download-script
- Estimated runtime: hours (No stated runtime in the repo. Probe-dataset collection (probing_gather.py, gatherdata_vfields.py) requires simulating potentially thousands of maze episodes through the CPU-bound procgen environment before any GPU work happens, which is the likely bottleneck rather than the small CNN's forward passes.)
- Stated compute in the repo: none
- Known blockers: Pinned dependencies are old (torch==1.13.1, gym==0.21.0, procgen==0.10.7); procgen wheels are not reliably available for modern Python/OS combos, so environment setup (not compute) is the main practical friction and likely needs an older Python (3.8/3.9) environment.; Multiple overlapping probing scripts/notebooks exist (experiments/probing_main.py, experiments/probing_gather.py+probing_postproc.py, playground/action_probing*.py, playground/goal_probing*.py) without one clearly-marked canonical entrypoint for the exact headline number.
- Inspector's notes: Compute is trivial (small CNN, arguably CPU-feasible even); the realistic friction is installing a multi-year-old procgen/gym/torch stack and picking the correct one of several overlapping probing scripts. Pretrained models are public (Google Drive, not gated).

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
