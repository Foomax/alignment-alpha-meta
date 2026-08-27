# handoff-19 — after R4b/R5b (2026-08-27 21:25)

- R4b and R5b both failed at prep with ENOSPC in the uv cache: prep builds a 5.8–6.2 GB venv while unpacking large wheels (sae-lens, e2e_sae's `torch~=2.2.0` pin pulling a second torch), and `/` was too tight for the spike even at 55 GB "free". **Freed 16 GB** by deleting HF models of already-ledgered experiments (`gemma-2-2b`, `Llama-3.2-1B-Instruct`, `Qwen2.5-1.5B-Instruct`, `Qwen3-0.6B`, `gemma-3-270m-it`) → 71 GB free, HF cache 12 GB.
- **Requeued**: R5c (retry with space) and R4c (`typeguard` + put `e2e_sae_src` on `PYTHONPATH` instead of `pip install -e`, which was downgrading torch to 2.2 and pulling torchvision — the disk/time cost). R4b/R5b removed from `tree_late.txt`.
- Bumped the queue's disk floor 12 → 25 GB in `tree_late.sh` (applies on the next relaunch; the running instance already has 71 GB).
- Late queue: R8b running; then R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b, R18b, R19b, R21b, R5c, R4c (18 remaining).
- Ledger unchanged: 16 attempted / 11 reproduced. Next: handoff-20, lessons-16.
