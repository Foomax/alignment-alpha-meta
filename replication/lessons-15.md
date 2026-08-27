# lessons-15 — from R4b/R5b (2026-08-27 21:25)

New:
1. **Prep's peak disk = venv size + wheel-unpack tmp, not just the venv.** uv unpacks each wheel into `~/.cache/uv/.tmp*` before hardlinking; a 6 GB venv can transiently need 10–15 GB more. A "12 GB free" floor checked *before* prep is too low — set it to ≥ 25 GB, or install into a venv on the same filesystem as the cache so hardlinks (not copies) are used (they already are here, but the unpack tmp still spikes).
2. **Never let a repo's editable install re-resolve torch.** `e2e_sae` pins `torch~=2.2.0`; `pip install -e` on top of torch 2.6+cu124 triggers a full downgrade + torchvision pull (multi-GB, minutes, and the ENOSPC trigger). Put such a package on `PYTHONPATH` instead, or install it `--no-deps` and add only its missing pure-Python deps (`typeguard`, `jaxtyping`).
3. **`uv cache prune` frees almost nothing when every wheel is in use** (removed 17 KB of 21 GB here). The lever is the HF model cache and dead venvs, not the uv cache.
4. **HF models of ledgered experiments are the disk reserve.** 16 GB freed in one command by deleting five models whose experiments were done; each is re-downloadable if a follow-up needs it. Keep only models for *pending* queue entries (OLMo for R18b, Llama-3.2-1B for R12b, gemma-3-1b).

Confirmed: lessons-8 (disk is a budget; a full disk looks like instant failures — two here), lessons-synth P3.
