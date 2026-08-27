# lessons-10 — from R19 (2026-08-27 19:08)

New:
1. **`uv pip install a b c` is atomic: one unresolvable name fails the whole batch.** A single bogus entry (here `mishax`, from the import scanner) left the venv empty, and the run then failed on `pandas` — a misleading traceback two steps removed from the cause. Always fall back to per-package installs on batch failure, and log the skipped names.
2. **The import scanner's local-module filter is incomplete for nested layouts.** It treats top-level directories and `.py` files as local; a module imported from a sub-project's own package (or a vendored dir) can slip through as a "package". Cheap guard: after scanning, drop any candidate that also exists as a directory or file anywhere under the repo (`find repo -name '<mod>' -o -name '<mod>.py'`).
3. **A venv size is a health check.** `du -sh .venv` at the end of prep: < 100 MB with torch requested means the install failed silently; the prep log now prints the torch version for the same reason.

Confirmed: lessons-synth P5 (install everything at once — but atomically-failing tools need a fallback), P1 (system before science: an empty venv is a system failure).
