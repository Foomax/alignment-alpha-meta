# Replicate: Testing which LLM architectures can do hidden serial reasoning

Source post: `ZB6guMhHH3NEyxA2k` (2024-12-16, LW karma 86). Repo: `filyp/sneaky-mamba` @ `b44a1d34d055c2c97a9def073f520806582b24f7`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Contrary to the hypothesis that recurrence itself would let Mamba outperform Transformers at a toy hidden-serial-reasoning task, standard Mamba (whose SSM recurrence transforms each channel independently) cannot solve the hidden task at all, while a modified Mamba SSM enabling cross-channel communication can; non-linearity is not required for hidden reasoning; and Transformers need roughly 3 extra layers to gain 1 extra unit of serial computation depth.

Supporting quote from the post: "Not every recurrence though - connections between channels are needed. Notably Mamba architecture isn't capable of hidden reasoning."

**Headline metric:** max hidden-task sequence length solved
**Claimed value:** standard Mamba fails to solve the hidden task; a modified Mamba with cross-channel SSM communication solves it; Transformers require about +3 layers per +1 unit of solvable task length
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `rel:0.15` — other scalar metric: 15% relative; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `sneaky_mamba/doublethink_train.py` (confidence: high)
- Produces: Per-architecture curriculum accuracy bars / max solved task length printed during training (architecture switch in doublethink_train.py covers mamba/switcher(modified mamba)/transformer in one script) plus switcher_direct_train.py for the direct (non-curriculum) comparison.
- Models: state-spaces/mamba-130m (stripped to 6 layers, ~30M effective) (0.03B), state-spaces/mamba-370m (Switcher variant) (0.37B), gpt2 (stripped to 1-5 layers) (0.124B)
- Estimated VRAM: 2 GB — All architectures are tiny (30-370M params, further truncated to a handful of layers) trained with batch size 64 on short synthetic token sequences -- negligible VRAM.
- Data: synthetic 'doublethink'/hidden-serial-reasoning task generated in utils/generation.py; availability: in-repo
- Estimated runtime: hours (Curriculum training loop runs until task_steps_limit>=30 or total_examples>2e6 at batch size 64 on tiny models; no stated wall-clock time in repo, but scale strongly suggests well under a few hours on a 3090.)
- Stated compute in the repo: none
- Known blockers: mamba-ssm and causal-conv1d require CUDA compilation at install time -- environment setup friction, not a compute blocker.; wandb.login() is called unconditionally; requires either a wandb account or setting WANDB_MODE=offline (trivial workaround, not a hard blocker).
- Inspector's notes: Cleanest 'no' surprise in the batch in reverse: this is by far the cheapest repo to reproduce -- toy models, toy task, single GPU, no external data or API dependency, matching the post's own framing as a small mechanistic toy experiment.

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
