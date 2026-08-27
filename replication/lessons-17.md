# lessons-17 — from R10b/R13b/R14b (2026-08-27 22:15)

New:
1. **`tree_prep.sh`'s import-list install fights a rerun's version pin.** The scanner installs the latest `sae-lens`; a rerun needing `sae-lens<6` must pin it in its own command (prep runs first, the rerun command second), or the pin is a no-op. General rule: version-sensitive pins belong in the rerun command, not in prep.
2. **Grokking / training-dynamics claims are inherently multi-hour** — the phenomenon is defined by thousands of epochs of delayed generalization. If the entrypoint loads a checkpoint the repo does not commit, and the only producer is a full training notebook, the honest reason is `runtime`, not a fixable env problem. Look at the committed result graphs to state whether they *support* the claim, but do not mark it reproduced without regenerating.
3. **A stale, incomplete venv survives a crash and poisons the next rerun** (`prep done` in 2 s = venv reused). The disk-bounded queue deletes venvs on the *happy* path only; after a prep or run crash, delete `experiments/<slug>/.venv` before requeuing.
4. **Committed `graphs/` PNGs are the author's results, not a reproduction.** Reading them (as with the grokking loss curves) tells you the claim is plausible and the repo self-consistent; it is not evidence *you* reproduced it. Keep that distinction in the ledger (`located` vs `reproduced`).

Confirmed: lessons-5 #4 (major-version pins), lessons-14 #4 (fetch/inputs part of entrypoint), lessons-synth P3 (budgets), P7 (located vs reproduced).
