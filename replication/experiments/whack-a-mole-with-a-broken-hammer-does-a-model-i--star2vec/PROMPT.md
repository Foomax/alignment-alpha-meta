# Replicate: Whack-a-mole with a broken hammer: does a model internally track its automaton state?

Source post: `LzeZW9PvR6Njc9ngr` (2026-08-18, LW karma 7). Repo: `star2vec/whackamole` @ `290dd72e94179cd793d85d3e7ba33dd4780afce3`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> A linear probe on Qwen2.5-1.5B activations reads a small model's internal, never-transcribed automaton state (a 6-state login DFA) correctly 88.6% of the time and outperforms order-blind baselines on order-ambiguous positions (80.8% vs 60.4% max), but the model cannot represent the count needed to distinguish 'two failures' from 'locked' (chance-level, ~50%, at every layer, even when the three-strikes rule is stated), and split-half probe testing confirms these are genuine model limitations rather than probe artifacts (only 33.8% agreement between two independently trained probes on the original probe's errors)

Supporting quote from the post: "The state is correctly read from the model's activation 88.6% of the time... Any method that sees the events and their number, but not their order, gets a maximum of 60.4%, but the probe scores 80.8% here."

**Headline metric:** linear probe classification accuracy on internal automaton state
**Claimed value:** 88.6% overall (vs 76.9% transcript-only, 20% majority baseline); 80.8% on order-ambiguous positions (vs 60.4% max for order-blind methods); 50.8% on the 'two failures' vs 'locked' distinction (chance)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 6 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `whackamole/gen.py -> whackamole/cache.py -> whackamole/probe.py (also bagcheck.py, control_task.py, layersweep.py, reliabilitymap.py for the secondary claims)` (confidence: high)
- Produces: figures/probe_v0.json (88.6% vs 76.9% vs 20%), figures/bag_analysis.json (80.8% vs 60.4%), figures/witness_reliability.json / figures/reliability_map.json (0.338 / max 0.623 split-half agreement)
- Models: Qwen/Qwen2.5-1.5B-Instruct (1.5B)
- Estimated VRAM: 6 GB — 1.5B model, prefill-only (no generation) forward passes with output_hidden_states=True over ~4,000 trajectories / 66k labeled positions, batched
- Data: synthetic login-protocol DFA trajectories, generated entirely in-repo by gen.py; availability: in-repo
- Estimated runtime: hours (cache.py contains a self-imposed compute budget gate (MAX_HOURS = 4.0) that projects wall time from the first few batches and aborts if exceeded; probe.py is fast sklearn logistic regression on cached activations)
- Stated compute in the repo: none
- Known blockers: data/ (trajectories, activations, frozen probes) is explicitly gitignored - the full pipeline must be regenerated from scratch, nothing is shipped as an artifact
- Inspector's notes: The cleanest repo in this batch for feasibility: self-contained synthetic data generation (no external corpus to source), a small ungated model, and an author-imposed 4-hour compute ceiling baked directly into the code. High confidence this reproduces on a single 3090.

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
