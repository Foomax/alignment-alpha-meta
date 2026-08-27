# handoff-14 — after R19 (2026-08-27 19:08)

- R19 (`ayoakin/mivlde`) failed at prep: the scanned import list contained `mishax` (a name the scanner could not classify as local), and `uv pip install <batch>` is all-or-nothing, so the venv stayed empty (12 MB) and the script died on `pandas`. **`tree_prep.sh` now falls back to per-package installs** for both `requirements*.txt` and the import list, and prints the installed torch version. R19b queued (same command). Not ledgered.
- R20 (`syvb`) is running with the *old* prep (started before the patch); everything after it uses the patched prep.
- Late queue: 26 entries; done R15, R17, R18, R19 (R17b/R18b/R19b are the live retries). Disk 86 GB free.
- Ledger unchanged (13 attempted / 10 reproduced). Next: handoff-15, lessons-11.
