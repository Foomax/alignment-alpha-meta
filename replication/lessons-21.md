# lessons-21 — from R18b/R19b/R20 (2026-08-28 00:45)

New:
1. **SIGKILL(137) on a CPU node = system-RAM OOM, not GPU.** The author's `DEVICE="cpu"; DTYPE="float32"` config loaded 3 fp32 copies of a 1B model (>31 GB RAM). `DEVICE` and `DTYPE` are hardware knobs (like batch size): switching `cpu`->`cuda` runs the identical computation on the 24 GB GPU where fp32×3 (~12 GB) fits. Check `free -g` / `dmesg | grep -i "killed process"` to distinguish RAM-OOM from a GPU OOM before choosing the fix.
2. **A stale entry in a *live* queue file can re-execute even after you ledgered it.** I ledgered R20 `vram` but left its `R20|` line in `tree_late.txt`; the outer loop re-read the file and ran it. When you decide not to run a queued node, remove its line AND add its name to the done-list in the same step; killing the process alone is not enough.
3. **`pgrep -f <slug>` / `pkill -f <slug>` match your own harness command shell** (the launcher trap, lessons-1 A2) — the "N processes still alive" count includes the very `bash -c` running your check. Confirm real survivors with `ps -o pid,stat,cmd -p <pid>`; kill by explicit PID.
4. **An entrypoint that exits 0 in 0 minutes with no output is a function library, not a runnable.** `run_experiment.py` had no `__main__`; running it did nothing. Grep for `__main__`/`argparse` before trusting a clean-but-silent exit; no self-execution + uncommitted inputs = `unclear-entrypoint`.

Confirmed: lessons-1 A2 (launcher trap), lessons-8 (memory budgets), lessons-2 #1 (entrypoint semantics).
