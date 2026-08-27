# lessons-24 — CUDA custom-kernel deps are an engineering-rot black hole (2026-08-28, from H57)

- **`undefined symbol: _ZN3c104cuda...` = torch ABI mismatch.** A prebuilt CUDA-extension wheel (mamba-ssm's
  `selective_scan_cuda`, flash-attn, causal-conv1d, apex) was compiled against a DIFFERENT torch than installed.
  pip happily installs the wheel; it explodes at import. The `c10::cuda` / `c10::` prefix names the torch C++ ABI.
- **Forcing source build is necessary but not sufficient.** `MAMBA_FORCE_BUILD=TRUE` + `--no-build-isolation`
  + `--no-binary` makes it compile against the installed torch — but (a) nvcc must match torch's CUDA minor
  (we had nvcc 12.0 vs torch-cuda 12.1), and (b) **any later `pip install` that bumps torch re-breaks the ABI** of
  the kernel you just compiled. Order matters: install/pin torch FIRST, build the kernel LAST, install nothing after.
- **Know when to stop (P13).** Three distinct diagnoses (isolation -> prebuilt-ABI -> source-build-ABI) is real
  progress, not blind retries, but it is still the 2-3 cap. A 4th "fix the install order" attempt buys zero new
  scientific signal — the engineering-rot finding is already made. Ledger `env` and move on; the build-fail IS the datum.
- **Recompute rescues the hours-class repo next to it.** tarcle (also hours-class) reproduced in 11 min because it
  COMMITS its intermediate artifacts and ships a numpy Stage-2 chain. The lesson for the field: commit your
  intermediates + a CPU re-analysis path, and your work stays reproducible even when your CUDA kernel won't build.
