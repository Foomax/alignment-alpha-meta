# Replicate: Banana in, Bostrom out: paperclip maximization is one token-direction swap away (in Qwen 3.6-27B)

Source post: `Eft6ehAcvR8MxFbsR` (2026-07-20, LW karma 8). Repo: `jeffreywilliamportfolio/jlens-basin-swaps` @ `1f68458b9dfc131d10a0e660ad0ad065b2628a75`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> In Qwen3.6-27B under greedy decoding, swapping the J-lens 'peace' token direction to 'banana' (or 'triangle') across layers 18-63 reliably changes a superintelligence-description completion from 'help humanity achieve a state of lasting peace' to 'maximize the number of paperclips produced' (3/3 per batch), while ablating a single 'China'-labeled token direction changes the same baseline completion to 'bring about the end of the world' (3/3); both effects are greedy-argmax phenomena that largely disappear by temperature 0.4.

Supporting quote from the post: "swapping the ‘peace’ token direction to ‘banana’, changes the completion to: “maximize the number of paperclips produced.”"

**Headline metric:** reproducibility of swapped/ablated completion across independent batches; exact-string rate across a temperature sweep
**Claimed value:** paperclip swap 3/3 per batch; doom ablation 3/3; doom string appears 20/20 at temp 0.1, 8/20 at 0.2, 5/20 at 0.3, 0/20 from 0.4 up
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 16 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `reproduce/run_reproduction.py` (confidence: high)
- Produces: printed completion strings from run_reproduction.py matching RESULTS.md's tables: paperclip swap ('maximize the number of paperclips produced.', 3/3) and China-direction ablation ('bring about the end of the world.', 3/3), plus the temperature sweep in data/doom_basin_temperature_curve/
- Models: Qwen 3.6-27B (hosted remotely by Neuronpedia; never downloaded or run locally) (27B)
- Estimated VRAM: 0 GB — No local model execution at all -- reproduce/run_reproduction.py is a ~20-line stdlib script (json/os/sys/urllib.request only) that POSTs to Neuronpedia's public https://www.neuronpedia.org/api/lens/prompt endpoint, which runs Qwen3.6-27B and the Jacobian lens on Neuronpedia's own infrastructure. README: 'No account or API key is required.'
- Data: none listed; availability: in-repo
- Estimated runtime: seconds to low minutes (run_reproduction.py issues one HTTP POST per payload (240s timeout); RESULTS.md reports 3 repetitions per condition across a small number of conditions)
- Stated compute in the repo: none
- Known blockers: depends entirely on a third-party free public API (Neuronpedia) remaining available and behaviorally stable -- the repo's own script docstring warns 'greedy decoding is not guaranteed token-identical across backend builds: reproduce the destination basin, not the byte-exact string'; if Neuronpedia changes or retires the endpoint/lens revision, exact-string reproduction may fail even though the method itself is trivial
- Inspector's notes: Unlike every other repo in this assignment, no local compute is needed at all: a 27B-model steering result is reproduced by a ~20-line stdlib script hitting a free, keyless public API (Neuronpedia's Jacobian Lens), so local VRAM/GPU is irrelevant to fits_3090. The real replication risk is dependence on a third-party hosted service's continued availability, not hardware -- the flip side is that this is NOT a fully offline/self-contained reproduction of the underlying computation.

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
