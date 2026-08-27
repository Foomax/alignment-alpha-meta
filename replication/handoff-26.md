# handoff-26 — batch R13c/R21/R27/R31 + tail requeues (2026-08-28 01:55)

Ledgered this batch:
- **R21 (`patrickod32`) reproduced**: probe AUC 0.90 (=target), keyword floor 0.75, probe 88% ≈ SAE 89%.
- **R31 (`peppinob-ol`) reproduced**: fact-variant S_Repl 0.5425 / S_Comp 0.8412 (target 0.5394 / 0.8257), byte-identical to committed.
- **R13 (`mamiglia`) `runtime`**: sae-lens<6 fixed the import; skew_analysis is a ~6 h full-vocab sweep (2/12 layers in 60 min), mis-tagged minutes.
- **R27 (`ibm`) `env`**: torch 2.3.1 fixes params_t but transformer-lens then unpack-errors (arity drift).

Tail requeued (final targeted attempts): R25d (stub `__spec__`/`__path__` — the training works, only Colab plumbing broke), R30d (`git+EleutherAI/sparsify`, pkg is named `eai-sparsify`), R14d (`python -m synth.run`; prep is transiently flaky but works), R28d (symlink `interpretability -> src`; utils.py asserts the dir name), R4d (e2e_sae on PYTHONPATH), R5d (`sae-lens<4`). Plus R32c (VAE, running), R29c, R6c, R12c, R18c.
- Ledger: **24 attempted / 14 reproduced** (taxonomy: none 16, env 2, unclear-entrypoint 2, runtime 2, api-key 1, vram 1). Disk 38 GB, uv cache the sink.
- Policy from here: these are the hard version-drift/gated tail; one more attempt each, then ledger env/runtime/model-access. Next: handoff-27, lessons-23.
