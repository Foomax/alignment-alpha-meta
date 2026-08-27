# handoff-10 — after R6 (2026-08-27 17:50)

- R6 (`cywinski/codi`) **reproduced** on the entrypoint script (same-vs-different latent patching; baseline 0.520 within ±5 of 55 %). `R6b` (script 5, the "~20 % recovery" figure) appended to the late queue (now 22 entries).
- Rerun pass 1 complete. `tree_rerun2.sh` (R12) is next, then `tree_late.sh` drains R15 … R6b in file order. Each finished node prints a `NODE … EXIT` line; the session monitor is armed.
- Ledger: 13 rows — 9 reproduced, 1 not, 1 unclear-entrypoint, 1 api-key, 1 pending (jordanmccann after R3b). Aggregate: `python3 replication/ledger.py`.
- Mirror to `/media/user/466CD2B96CD2A34B/home/alignment-replication-3090-2026-08/` every 10 min (check `last-mirror.txt`).
- Next numbering: handoff-11, lessons-7.
