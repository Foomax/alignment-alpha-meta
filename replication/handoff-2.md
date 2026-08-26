# handoff-2 — node 2: `fractalmachinist/ioi` (GPT-2 small IOI, negative claim) — REPRODUCED (2026-08-27 07:35)

- Pinned `1571259a`; entrypoint `experiments.ipynb` via nbconvert, 3 min wall-clock, GPU ~2 GB.
- [MEASURED] drop +0.231 ± 0.844 (n=128), t=3.0922 p=0.002443, d=0.2733, acc 0.9531→0.9453 — all eight target numbers match to stated precision. `claim_reproduced=true`, reason `none`.
- Env only: repo has no requirements file; notebooks need pip+jupyter in uv venvs. Auto-fix loop installed `transformer-lens scipy jupyter nbconvert ipykernel` (rounds 1–2), prep now pre-installs the notebook stack, so later notebook nodes should pass first time.
- Runner lessons applied to the tree this round: (1) sanitise `python_version` before `uv venv`; (2) pre-build venvs in the tree (run.sh skips its install block when `.venv` exists); (3) strip ANSI before parsing tracebacks; (4) treat a running `run01.sh` as GPU-busy (nvidia-smi alone has gaps between an experiment's phases — node 2 overlapped with node 01 for ~3 min; both fit in VRAM, no effect on either result).
- Node 01 status at this point: eval C extracted + CKA done, permutation test running; A/B/D/E to follow.
- Next: judge nodes as they land; node 3 (`jordanmccann/polymorphism-is-rotation`) is first in the relaunched queue.
