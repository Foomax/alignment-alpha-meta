# lessons-8 — the disk-full incident (2026-08-27 18:10)

New:
1. **One venv per experiment × torch is a disk budget, not a hygiene rule.** ~4 GB each (torch+CUDA wheels dominate); 30 of them plus a 44 GB model cache filled a 449 GB drive that had 129 GB free at the start of the day. Budget disk like GPU time: `df` in the queue loop, refuse to start below a floor, and delete the venv after each run (uv rebuilds one in 3–5 min from its cache).
2. **A full disk masquerades as a burst of instant failures.** 16 "EXIT in 0 s" lines in one minute is the signature; the harness also loses command output (ENOSPC). Rule: any node that fails in < 5 s *and* lands within a minute of other such failures is suspect — check `df` before reading tracebacks, and never ledger from those lines.
3. **Keep a done-list you can reset.** Because the late queue tracked completion by name in a plain file, recovery was `echo R15 > tree_late_done.txt` plus a relaunch; the per-experiment `run.log` history stays intact because reruns relabel earlier `RUN-EXIT` lines instead of overwriting.
4. **Model caches are the other silent consumer.** Every minute-class node that touches a 1–3B model adds 2–10 GB to `~/.cache/huggingface`. Decide up front what is disposable (anything re-downloadable whose experiment is ledgered) and put `HF_HOME` on the largest ext4 volume available — not NTFS (symlinks).
5. **Raw activation dumps are not results.** 01 kept 4.4 GB of fp32 activations whose only downstream products (CKA CSVs, 100 KB) were already saved. Delete intermediates once the derived artefact exists and is committed.

Confirmed: lessons-1 A1/A2 pattern (silent stalls and instant failures both need a "check the system before the science" reflex).
