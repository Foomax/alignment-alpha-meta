# lessons-2 — from pass-1 nodes 15–19 (2026-08-27 15:10)

New (not in lessons-1):
1. **The catalogue `entrypoint` is a pointer, not a command.** In ~half the quick projects it names the script/notebook where the headline number is *computed*, which may be step 7 of a pipeline (node 18: `07_compare_patch.py` needs `base.safetensors` from `01_…` and `patch.safetensors` from `03_…`). Before running an entrypoint, `grep -n "load_file\|open(\|read_csv"` it for inputs and check which earlier script produces them; queue the chain, not the last step.
2. **Auto-fix rounds should be counted in packages, not attempts.** Node 17 needed 5 packages and got 3 rounds. Either raise the cap when every round installed something new and progressed past the previous failure line, or install the whole import list up front (`grep -h "^import\|^from" *.py *.ipynb` → package map) — cheaper than a run per package.
3. **Sub-project layouts need a path search, not a single `PYTHONPATH`.** Node 19's script lives in `subteams/LLMProbing/experiments/` and imports `src` relative to `subteams/LLMProbing/`. Set `PYTHONPATH` to the script's parent, grandparent and repo root; it is harmless when unneeded.
4. **A missing import in a notebook is the same class as a missing import in a module** (03 precedent): copy the notebook, prepend one import cell, record as an env fix. Do not edit the author's file in place.
5. **Authors' "CPU because I'm poor" configs are a gift**: they bound the runtime (node 18 trains one weight row for 2 epochs) and mean a 3090 will not be the bottleneck — the download is. Pre-download the model when the spec lists it.

Confirmed from lessons-1: A4 (descriptive entrypoints), C1 (notebook stack), C2 (auto-fix map), D5 (deterministic small-model notebooks reproduce to 3 decimals: node 16).
