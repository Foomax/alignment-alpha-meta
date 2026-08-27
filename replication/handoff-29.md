# handoff-29 — hours-class scale-test complete; queue STOPPED (2026-08-28 06:56)

Read `handoff-synth.md` first. This closes the scale-test the user asked for as step 3.

## Both hours-class rows judged
- **H36c star2vec/tarcle = REPRODUCED (recompute).** Two target anchors exact (+0.352 / -1.000); imposter-FV
  thesis holds (out-of-pool collapse + behavioral GO). See handoff-28 / human-oversight §27.
- **H57 filyp/sneaky-mamba = NOT LOCATED, reason env.** mamba-ssm `selective_scan_cuda` will not import in-queue
  across 3 tries (build-isolation -> prebuilt-wheel ABI mismatch `undefined symbol c10::cuda` -> forced source build
  still ABI-unstable: nvcc 12.0 vs torch-cuda 12.1, dep-induced torch bump). Stopped at the 2-3 cap (P13). The claim
  (standard Mamba fails hidden-serial-reasoning vs cross-channel `switcher` solves) was never reached. human-oversight §28.

## Ledger (FINAL, N=36) — `python3 ledger.py`
**36 attempted · 35 installs · 21 runs · 20 located · 15 reproduced** (11 exact + 4 recompute).
located that reproduced >=partially: **18/20 = 90%**. never located: **16/36 (44%)**, all engineering/hardware.
Taxonomy: none 19, env 7, runtime 3, unclear-entrypoint 2, vram 2, api-key 1, data 1, model-access 1.

## Scale-test read (honest)
Sample of 2 hours-class repos: 1 reproduced (via the committed-artifact RECOMPUTE path — the from-scratch GPU
extraction, the actually-hours-class part, was not run), 1 failed on a CUDA custom-kernel build. The
89%->90% / "engineering-rot dominates" pattern HELD, but n=2 is tiny and one was recompute-not-from-scratch.
Do NOT overclaim "the finding holds at scale" from this; state it as consistent, not confirmed.

## State
- Queue STOPPED (`tree_late.stop` set); `tree_late.txt` drained. Do not relaunch.
- Remaining work: (1) fold both rows into META-REPORT.md (in progress this turn); (2) then STOP per the user's
  "stop after the tail + follow suggested steps" — harness packaged (HARNESS.md), scale-test done.
- Direction work continues separately in `prompts2/` (another instance). Leave it alone.
