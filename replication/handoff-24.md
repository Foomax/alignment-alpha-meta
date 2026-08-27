# handoff-24 — after R17b/R6b/R12b (2026-08-28 00:35)

- **R17 ledgered `env`** (2 attempts spent): notebook loads SAE by legacy sae-lens id `11-res-jb`, removed in sae-lens ≥3; pinning back conflicts with transformer-lens/torch 2.6. Claim (Jaccard 0.13; within/cross cosine 0.50/0.14) needs that SAE.
- R6b → **R6c** (run `prepare_prompts_json.py` first — script 5 needs `prompts/prompts.json`). Note: codi's headline already reproduced at R6; this is only the "~20% recovery" sub-figure.
- R12b (38 min) → **R12c** with `--allow-errors` (a mid-notebook `ValueError: too many values to unpack` — transformer-lens version drift; capture partial output to salvage the L0H3 result, else code-bug). Last attempt.
- Running: R18b (`sunmoonron` OLMo super-weight, chain 04→07). Queue tail: R19b, R21b, R5c, R4c, R13c, R14c, R25c, R27c, R28c, R30c, R31b, R32c, R29c, R6c, R12c.
- Ledger: 19 attempted / 12 reproduced (taxonomy: none 14, api-key 1, unclear-entrypoint 1, runtime 1, vram 1, env 1). Disk 50 GB, uv cache ~39 GB (the growing sink). Next: handoff-25, lessons-21.
