# lessons-20 — from R17b/R6b/R12b (2026-08-28 00:35)

New:
1. **Renamed library *assets* (registry ids, model hub keys) are a distinct failure class from renamed *APIs*.** `sae-lens`'s `11-res-jb` SAE id, HF dataset config names, `transformer_lens` model aliases — these live in the library's version-specific registry, and the old id often needs an old library that no longer co-installs with current torch. Two pins deep with no resolution → `env`, and name the exact id in the ledger so a future run can pin the whole old stack deliberately.
2. **`--allow-errors` must be on *every* notebook rerun command, not just the ones added after a given date.** R12b lacked it (my blanket `sed` missed its line), so a mid-notebook error at minute 38 discarded all output. Grep `tree_late.txt` for nbconvert lines without `--allow-errors` before trusting the queue.
3. **A multi-script experiment usually has a `prepare_*`/`generate_*` step that writes the inputs.** codi's script 5 reads `prompts/prompts.json` produced by `prepare_prompts_json.py` (README step 1). When a script fails on a missing *input* file (not output), look for its generator in the repo root and prepend it — don't confuse it with an output dir you may have deleted for disk.
4. **`ValueError: too many values to unpack (expected 2)` in a mech-interp notebook = a tuple-arity API change** (e.g. `run_with_cache`, `model(tokens)` return shapes shifted between transformer-lens versions). Fixable only by matching the author's transformer-lens version or editing the unpacking — the latter risks changing what's measured, so prefer the version pin or ledger `code-bug`.

Confirmed: lessons-12 (--allow-errors), lessons-2 #1 / lessons-14 #4 (chain inputs), lessons-5 #4 (major-version drift).
