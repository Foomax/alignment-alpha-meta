# Replication harness — reusable tooling + manual

A small, sequential, disk-bounded harness for reproducing many pinned research repos on one GPU, one at a time, with environment-only fixes and a per-row ledger. Built during the 3090 replication run (34 experiments); the failure knowledge that drives it is in **`lessons-synth.md`** (Part 3 is the symptom→cause→fix catalog — read it first).

## Layout
```
replication/
  experiments/<slug>/         spec.json, PROMPT.md, report.py, run.log, ledger.json, src/ (pinned checkout)
  tree_prep.sh                env prep for one experiment dir  (clone@SHA → venv → deps → import scan)
  tree_imports.py             AST import scan (.py+.ipynb) → pip names, stdlib/local filtered
  tree_autofix.py             module→pip-name map (shared with tree_imports)
  nb_colab_stub.py            make a *_repl.ipynb with a sys.modules google.colab stub (with __spec__)
  tree_late.sh                the queue: reads tree_late.txt, one GPU job at a time, deletes venv per run
  tree_late.txt / _done.txt   queue entries (name|slug|timeout_min|cmd) / completion log (resettable)
  tree.log                    one line per finished node (monitor this)
  tree_publish.sh             commit replication/ after each node (no forking)
  publish.sh                  push one experiment to its Foomax fork (allowlisted; README # human / # LLM)
  ledger.py / report.py       (project) aggregate / write a row's ledger.json
  annotate_tiers.py           add quality_tier to every ledger.json
  make_report_table.py        regenerate META-REPORT numbers
  mirror.sh                   rsync repo (minus venvs) to external drive every 10 min
```

## The core workflow
1. **Queue a row:** append `name|slug|timeout_min|command` to `tree_late.txt`. `command` runs inside `experiments/<slug>/`, with the venv at `../.venv/bin/python`.
2. **`tree_late.sh`** (detached: `setsid nohup ./tree_late.sh > tree_late_nohup.out 2>&1 < /dev/null & disown`) waits for a free GPU and ≥25 GB disk, runs `tree_prep.sh <dir>` (clone at the spec SHA, build `.venv`, install), then the command, then **deletes the venv**. One line to `tree.log`. Stop: `touch tree_late.stop`.
3. **Judge** each `NODE … EXIT` line (loop in `handoff-synth.md` §A3): read the log, translate/fix per `lessons-synth.md`, requeue (≤2–3 tries) or ledger (`report.py` + `== VERDICT`), commit.

## Design rules learned the hard way (all in lessons-synth)
- One GPU job at a time; busy = python-on-GPU **or** a runner-script pid alive.
- Delete the venv after each run; refuse to start below 25 GB free (a torch venv ≈ 5 GB; the uv cache grows unboundedly).
- The `spec.json.entrypoint` is a *pointer*, not a command — translate it (prose / chain / notebook / subset / function-library); never execute it verbatim.
- Environment-only fixes on copies; each a `--fix` line. Notebooks: nbconvert `--allow-errors`; stub `google.colab` in `sys.modules` **with `__spec__`+`__path__`** (leave the import lines intact).
- Pin to the author's library epoch: `transformers<5` (mid-4.x for `evaluation_strategy`), `datasets<4`, `sae-lens<6`/`<4`, `setuptools<81`, `torch==2.3.1`→cu121.
- Never push to upstream; never paste tokens; pause the agent, not the GPU.

## Reuse elsewhere
Point `experiments/<slug>/spec.json` (`repo`, `head_sha`, `entrypoint`, `budget_minutes`, `target_value`, `tolerance`) at any pinned repo and queue it. The harness is provider- and topic-agnostic; only `tree_autofix.py`'s name-map and the `lessons-synth` catalog are domain-flavoured (mech-interp / SAE / transformer-lens), and both are easy to extend.
