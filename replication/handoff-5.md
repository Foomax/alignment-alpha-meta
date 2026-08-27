# handoff-5 — juncture after pass-1 nodes 15–19 (2026-08-27 15:10)

State delta since handoff-4:
- Node 16 (`ameya-bit/QuotesByNiche`) **reproduced exactly** → ledgered (copying 0.615/0.347; OV +0.556/−0.105).
- Nodes 15, 17, 18, 19 failed on plumbing → queued in `tree_late.txt` as R15 (missing `import torch.nn.functional as F`, notebook copy), R17 (`sae-lens` beyond the 3 auto-fix rounds), R18 (run the pipeline chain 01→03→07, 90-min box), R19 (`PYTHONPATH` for a sub-project).
- Late queue now: R15, R17, R18, R19; rerun passes still armed behind pass 1 (nodes 20–32 to go).
- Ledger count: 8 rows (5 reproduced, 1 not, 1 unclear-entrypoint) + 1 in progress.

If you take over: read `handoff-4.md` for the full mechanics; the only new mechanism is `tree_late.txt` (append `name|slug|timeout_min|command` — the `tree_late.sh` loop picks it up within 2 min when the GPU is free). Ledger rows for R-nodes are written after their rerun; do not ledger a plumbing failure.
