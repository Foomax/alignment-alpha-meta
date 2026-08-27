# lessons-19 — batch R27–R32 (2026-08-27 23:30)

New:
1. **The headline number may be a *variant* the default run doesn't produce.** `peppinob-ol`'s post reports 0.5394/0.8257; the default 5-dataset summary gives 0.689/0.890, but the **fact-checking** dataset (`usa_states_fact_batch`) gives 0.5425/0.8412 — the actual headline. Before judging "not reproduced", check every summary file in `output/` and match the target to the right subset; the spec's `headline_artifact` names the file, read it fully.
2. **`setuptools>=81` removes `pkg_resources`**, breaking `wandb` and other legacy imports on Python 3.11/3.12. Add `setuptools<81` to the base env for any repo importing wandb/pkg_resources — done globally in `tree_prep.sh`.
3. **`transformer-lens` needs `typeguard`+`jaxtyping` that the import scanner misses** (they're its deps, not repo imports). Pre-install them whenever transformer-lens is pinned to an old torch that skips its extras.
4. **`sparsify` is a name collision**: EleutherAI's SAE library (`from sparsify import Sae`) vs Neural Magic's unrelated PyPI `sparsify`. `Sae`/`SparseCoder` imports → install `git+https://github.com/EleutherAI/sparsify`.
5. **The uv cache is the slow disk leak** (grew 21→39 GB over the reruns) and is not prunable while wheels are referenced. The recoverable reserve is (a) ledgered experiments' `src/` outputs and (b) their HF models. Sweep `du -sh experiments/*/src` between nodes and delete finished ones.
6. **Catalogue "minutes" tags undercount training loops.** A script that trains N models in a `for` loop is N × per-model time; grep for `for .* in range(` before trusting the budget.

Confirmed: lessons-14 #1 (verify/headline coverage), lessons-5 #4/#5 (major-version pins, GitHub packages), lessons-8 (disk budget), lessons-6 #1 (time-box from per-item timing).
