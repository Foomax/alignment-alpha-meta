# handoff-12 — disk-full incident and recovery (2026-08-27 18:10)

- At ~17:54 `/` reached 100 % (per-experiment venvs ≈ 4 GB × ~30 + HF cache 44 GB + outputs). The harness lost command output (ENOSPC) and every late-queue entry from R17 to R32 "failed" in 0–1 s. **Those tree.log lines are artefacts, not results**; `tree_late_done.txt` was reset to `R15` (backup: `tree_late_done.diskfull-backup.txt`), and a `DISK FULL EVENT` line was appended to `tree.log`.
- Freed: venvs of all experiments (rebuildable), HF models `Llama-3.2-3B`, `pythia-2.8b`, `pythia-1.4b`, `Qwen2.5-1.5B` (re-downloadable; needed only for 01's unresolved evals D/E), and 01's `outputs/*/activations/` (CKA results kept). Free space ≈ 90 GB.
- New mechanics: `tree_prep.sh <exp_dir>` (standalone env prep incl. full import list) and a rewritten `tree_late.sh`: prep → run → **delete venv**, and it waits while < 12 GB is free. Relaunched; R17 is first. Everything else unchanged (`tree_late.txt` 23 entries, `tree_publish.sh` watcher, mirror loop).
- Ledger unaffected: 14 rows (10 reproduced, 1 not, 1 unclear-entrypoint, 1 api-key, 1 pending).
- Next numbering: handoff-13, lessons-9.
