# handoff-25 — after R18b/R19b + R20 kill (2026-08-28 00:45)

- **R19 ledgered `unclear-entrypoint`**: `run_experiment.py` is a function library (no `__main__`), needs uncommitted activation data; matches spec blocker.
- **R18b SIGKILL(137) = system-RAM OOM**: `07_compare_patch.py` loads 3 fp32 OLMo-1B copies (>31 GB RAM) on the author's CPU config. Fixed by editing `src/config.py` `DEVICE="cpu"`->"cuda" (hardware knob; fp32×3 ≈12 GB fits the 24 GB GPU); **R18c** queued (04->07).
- **Killed stale R20**: the original `R20|` queue line (already ledgered `vram`) re-triggered and started its 90 GB / 2×7B download; killed by PID, removed the line, added `R20` to the done-list. (Reminder: my own `pgrep -f <slug>` command shells match the slug — the launcher trap; verify kills with `ps`, not the pgrep count.)
- Ledger: 20 attempted / 12 reproduced (taxonomy: none 14, unclear-entrypoint 2, env 1, api-key 1, runtime 1, vram 1). Disk 38 GB.
- Queue (26): R21b running-next, R5c, R4c, R13c, R14c, R25c, R27c, R28c, R30c, R31b, R32c, R29c, R6c, R12c, R18c. Next: handoff-26, lessons-22.
