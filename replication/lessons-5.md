# lessons-5 — from the first rerun pass and the resume (2026-08-27 17:05)

New:
1. **One module per round is the wrong unit.** Seven of nine reruns failed on *one more* missing module after the previous fix. Scan all imports up front (`tree_imports.py`: AST over `.py` + notebook code cells, stdlib/local filtered) and install the list once. Cost: 30 s. Saved: a full run per module.
2. **Shell entrypoints swallow errors.** `full_experiment.sh` ran `python a.py; python b.py; …` — each died on `tqdm`, the script exited 0, the node was marked a success in 0 min. Run author `.sh` files with `bash -e`, and treat "EXIT 0 after 0 min" as a red flag to read the log.
3. **Pinned old torch needs the matching CUDA index.** `torch==2.3.1` has cu121 wheels, not cu124; `requirements.txt` pins silently fail under the cu124 index and the newer torch stays. Install pins from the index that has them.
4. **Major-version API removals are now the most common env failure class for 2024–25 repos**: `transformers.TRANSFORMERS_CACHE` (gone in 5), `datasets` non-namespaced names like `"imdb"` (gone in ≥4), `sae_lens.toolkit` (gone in 6), `torch.optim.optimizer.params_t` (gone in 2.6). Default pins for a 2025 repo: `transformers<5`, `datasets<4`, `sae-lens<6`; torch per the repo.
5. **Some "packages" are GitHub-only** (`neel-plotly`, the author's `e2e_sae` fork whose wheel omits `scripts/`). Fall back to `git+https://…` and, when a repo imports a submodule the wheel omits, an editable clone.
6. **Pausing the agent, not the GPU, is the right shape for a usage budget.** Detached queues completed 9 nodes and a rerun pass during a 90-minute pause; the resume cost was one `tail` of `tree.log`.
7. **Mirror to removable media with `--no-links` and exclude venvs**; NTFS drops symlinks (venv `python` is one) and would otherwise report thousands of errors.

Confirmed: lessons-2 #1, lessons-3 #3, lessons-4 #3 (descriptive entrypoints keep being the #1 failure source); lessons-1 D5.
