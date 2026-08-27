# handoff-15 — after R19/R20 (2026-08-27 19:20)

- R20 (`syvb/natural_language_autoencoders`) ledgered `vram`: six Qwen2.5-7B NLA checkpoints (~90 GB) and two 7B models at once on a 24 GB card; author specifies 48 GB. R20b withdrawn from `tree_late.txt`.
- R19 → R19b queued after a prep fix (`tree_prep.sh` now installs requirements and the import list per-package when a batch fails; prints torch version; `tree_imports.py` filters any name that exists as a dir/file in the repo).
- **Process rule added**: never rewrite a running bash script in place — R20's "prep failed" exit was caused by my patching `tree_prep.sh` while it executed. Patch via temp file + `mv` (new inode) from now on.
- Late queue: R21 running; then R23, R3b, R4b, R5b, R8b, R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b, R19b (21 entries after R21). Disk ≈ 86 GB free.
- Ledger: 14 attempted / 10 reproduced (new row: R20 vram). Next: handoff-16, lessons-12.
