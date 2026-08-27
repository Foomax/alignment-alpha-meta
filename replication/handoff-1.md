# handoff-1 — node 01: `jaehoonlee0829/cross-model-alignment-geometry` — REPRODUCED on C, A, B; D, E unresolved (2026-08-27 14:30)

- Pinned `bfacecff`; env `.venv` py3.11, torch 2.6.0+cu124, full requirements. Pipeline `run01.sh` (extraction → CKA → corrected permutation tests per config). Env fixes: `PYTHONPATH=<repo root>` (attempt 1 died at import on every eval); xet disabled + 22 GB pre-download (106 min); CUDA torch.
- [MEASURED] max/mean debiased CKA — C 0.9138/0.6045, A 0.2082/0.0531, B 0.2224/0.1116; perm p=0.002 each; ratio 4.1×. README: 0.914/0.605, 0.208/0.053, 0.222/0.112. `claim_reproduced=true`, reason `none`, wallclock 332 min.
- Timing reality: ~100 min per eval, dominated by the CKA + permutation stages (extraction ~5 min/model). My estimate of "45 min of GPU" was wrong by ~6×. The 240-min budget ran out during B; only extraction was time-boxed, so B overran by 92 min — recorded in the ledger notes. Prompt contingency ("stop after A–C") applied; D, E are UNRESOLVED (≈100 min each if ever wanted; models cached).
- Fork `Foomax/cross-model-alignment-geometry` @ `97feccc` has README (# human / # LLM), ledger, run.log, results CSVs.
- Tree state at this point: nodes 2–14 processed; 2, 7, 11 exit 0; the rest are runner/env failures being batched into a rerun pass (see handoff-3).
