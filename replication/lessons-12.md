# lessons-12 — from R21 (2026-08-27 19:55)

New:
1. **Always execute notebooks with `--allow-errors`.** Without it, nbconvert discards the whole output notebook when any cell raises — 37 minutes of computed metrics vanished because the *last* cell imported `google.colab`. With it, every cell's output is written and the error cell is marked; judge from the outputs and report the failed cell.
2. **Colab imports can appear anywhere, not just in the setup cell.** Grep the entire notebook for `google.colab`, `drive.mount`, `files.download`, `userdata.get`, and `%pip`/`!pip` cells before running; stub the module in `sys.modules` from a prepended cell rather than editing individual import lines (covers `import google.colab as x`, nested imports, later cells).
3. **Cost-weight your pre-checks by the run's length.** A 30-second scan of the notebook would have saved a 37-minute run; the earlier 2-minute notebooks did not justify the scan, this one did. Rule of thumb: if the box is > 15 min, read every cell's first lines before queuing.

Confirmed: lessons-3 #2 (Colab paths), lessons-7 #1 (string-vs-list sources), lessons-synth P2/P4.
