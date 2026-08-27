# handoff-4 — current state for another instance picking this up cold (2026-08-27 14:55)

## Where things are
- Repo: `~/alignment-literature-meta-analysis` = `Foomax/alignment-alpha-meta` (`master`, pushed after every judged node). All replication work is under `replication/`. Your other uncommitted files at the repo root are the user's; leave them.
- Ledger: `python3 replication/ledger.py` aggregates `experiments/*/ledger.json`. Rows so far: 01 ✓, 02 ✗, 03 ✓, ioi ✓, probe-necessity ✓, induction-head ✓, top-down-vs-bottom-up `unclear-entrypoint`.
- Forks (only these three, by the user's decision): `Foomax/AntiPaSTO`, `Foomax/arena-sandbagging-mi`, `Foomax/cross-model-alignment-geometry`, branch `replication-3090`, README `# human` / `# LLM`. `publish.sh <slug>` is allowlisted to them. **Do not create more forks.**
- Docs: `hand-off.md` (planning + close-out for the AntiPaSTO/03 window), `handoff-0…4.md` (this series), `human-0.md`, `human-oversight.md` (ELI5 running log + "needs you" items), `lessons-1.md`.

## What is running (one GPU job at a time, all detached with setsid)
1. `tree_queue.sh` — pass 1 over `tree_minute_class.txt` (31 slugs, queue.md order), currently node 18. Skips slugs in `tree_done.txt`. Per node: `prep_env` (venv, torch cu124, requirements, notebook stack) → `run.sh` → auto-fix loop (`tree_autofix.py`). One line per node to `tree.log`.
2. `tree_rerun.sh` — waits for pass 1; hand-written invocations for nodes 3,4,5,6,7,8,10,13,14 (see `handoff-3.md`).
3. `tree_rerun2.sh` — waits for 2; node 12 via nbconvert.
4. `tree_late.sh` — generic late queue: appends to `tree_late.txt` (`name|slug|timeout_min|command`) get run when the GPU is free; currently R15 (matryoshka notebook + missing import) and R17 (sae-lens). Stop it with `touch tree_late.stop`.
5. `tree_publish.sh` — watcher that commits the meta repo after each `NODE … EXIT` line (no forking).
Monitors in this session: `tree.log` lines. If you are a fresh session: `tail -f replication/tree.log`.

## How to judge a finished node (the loop I run)
1. `grep "NODE <n>-" tree.log` for exit code; read `experiments/<slug>/run.log` tail (strip ANSI, `tr '\r' '\n'`), `autofixes.txt`, `prep.log` if exit 2.
2. Compare against `spec.json` (`target_value`, `tolerance`, `headline_artifact`) and `PROMPT.md`'s tolerance paragraph. Notebook outputs are in `experiments/<slug>/executed.ipynb` (`outputs[].text` / `data['text/plain']`).
3. Append a `== VERDICT` block to `run.log` ([MEASURED]/[INFERRED]/[UNRESOLVED] + pipeline line), then `python3 report.py --observed … --reproduced true|false --reason none|env|data|model-access|vram|runtime|code-bug|api-key|unclear-entrypoint --seeds N --fix "…" --notes "…"`.
4. If the failure is a runner/env problem, append a line to `tree_late.txt` instead of ledgering; ledger after the rerun.
5. Add a short section to `human-oversight.md` (ELI5 + "Needs you?"), a `handoff-n.md` when state changes materially, `lessons-n.md` when a new lesson appears; commit `replication/` and push.

## Known open items
- Node 6 (`cywinski/codi`) rerun needs ~95 min (200 prompts × 12.8 s + model load); gated Llama-3.2-1B-Instruct is accessible.
- Node 9 (`ak47na`) is `unclear-entrypoint` (pre-generated completions + W&B artifact); no rerun planned.
- Experiment 01 evals D/E (~100 min each) are UNRESOLVED; models cached; run from the repo root with `PYTHONPATH=$PWD`.
- AntiPaSTO: a third 270M seed for default vs random dims (70 min) would pin the random-dims mean; nothing else worth GPU time without the author's 1B config.
