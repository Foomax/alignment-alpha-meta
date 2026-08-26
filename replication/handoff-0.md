# handoff-0 — pros/cons of the plan, and the execution tree (2026-08-27 02:45)

Plan under evaluation (from `hand-off.md` §6): run experiment 01 now that the Llama licences are
accepted, then work through the minute-class queue in `queue.md`. Below: a quick pros/cons, then the
exact tree being queued and how each node is judged.

## Pros / cons

| | Pros | Cons |
|---|---|---|
| **Running 01 first** | Completes the designed triad (negative / positive / replication); #1 pareto pick; unblocked; ≈45 min GPU; built-in control eval C; committed reference outputs make judgement mechanical | ≈1 h of downloads first (22 GB at ~6 MB/s); `sae-lens`/`nnsight` in requirements may not resolve; scientific outcome fairly predictable (high prior of reproducing) |
| **Then the minute-class queue via each folder's `run.sh`** | Rows per GPU-hour is the ledger's currency; 31 candidates already inspected (spec.json with pinned SHA, entrypoint, budget); `run.sh` is a uniform thin runner (clone → venv → torch cu124 → requirements → entrypoint with timeout) so the mechanical part is fully automatic | `run.sh` never *fixes* anything: an experiment that dies on a missing pin or a path will be recorded as a failure unless I intervene; judgement (observed value, tolerance) still needs me per row; installs are ~3–5 min each → 31 × (install + run) could be 6–12 h; some rows will be `api-key`/`model-access` by construction |
| **Fully unattended queue** | GPU never idles; one job at a time; timeouts per spec budget | If a job hangs *inside* its budget (like the xet stall) it burns the whole budget; a bad `run.sh` install can pollute nothing else (per-experiment venv), but uv cache lock contention is possible if two installs overlap — avoided by strict sequencing |
| **Per-run handoff/human docs** | Forces a judgement per row instead of a pile of logs; ELI5 keeps the human in the loop | 31 short docs is noise if every row is "installs ✓ runs ✓ reproduces ✓"; keep them to a few lines unless something interesting happened |

Net: the plan is sound. Biggest real risk is not science but *attention*: the queue runs faster than I can judge if many rows are trivial, and slower than the budget if several need env fixes. Mitigation: judge in arrival order, fix-and-rerun only when the fix is a one-liner inside the row's budget, otherwise record the failure reason and move on.

## Execution tree (one GPU job at a time)

```
tree
├── 01 cross-model geometry  (experiments/cross-model-…--jaehoonlee0829/run01.sh)
│   ├── wait for downloads.log DOWNLOADS-EXIT 0   (running now, no GPU)
│   ├── venv py3.11 + torch cu124 + requirements (sae-lens/nnsight dropped if they fail)
│   ├── for cfg in eval_c phase_a phase_b phase_d phase_e:  extraction → cka → permutation tests
│   └── RUN-EXIT → I run analysis, report.py, VERDICT → handoff-1.md, human-1.md
└── minute-class queue (replication/tree_minute_class.txt, queue.md order, 31 rows)
    └── for slug: experiments/<slug>/run.sh  (own venv, timeout = budget)  → tree.log line
        → I judge each on arrival: observed vs target, report.py, handoff-n.md, human-n.md
```

Judgement rules per row (from the shared ground rules): pin the SHA; environment fixes only; no closed APIs; `[MEASURED]/[INFERRED]/[UNRESOLVED]`; a ledger entry is the goal, not a success.

Numbering: `handoff-1`/`human-1` = experiment 01; `handoff-n`/`human-n` for n ≥ 2 follow `tree.log` order.
