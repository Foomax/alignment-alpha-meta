# lessons-9 — from R18 (2026-08-27 19:00)

New:
1. **Chain discovery must be transitive, from the config's PATH constants.** I traced `07`'s inputs one level (`base`, `broken`, `patch`) and missed that it also loads `PATCHED_MERGED_PATH`, produced by `04`. Do it mechanically: `grep -n "_PATH\s*=" config.py` → for each constant, `grep -ln "save_file(.*<CONST>\|<CONST>)" *.py` gives the producer; build the chain from the leaves. One 33-minute rerun would have been avoided.
2. **Keep intermediates between reruns when the venv is deleted.** The disk-bounded queue removes `.venv` but not `src/`; the checkpoints from 01/03 survived, so R18b is `04 → 07` only. Design cleanup to delete *environments*, never *outputs*.
3. **`pybind11>=2.12` / "compiled against numpy 1.x" warnings are noise unless the run fails at that import.** Note them, don't chase them.

Confirmed: lessons-synth P2 (entrypoint = pointer; pipelines), §2.3 chain rule.
