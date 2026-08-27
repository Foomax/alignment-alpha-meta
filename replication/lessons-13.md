# lessons-13 — from R23 (2026-08-27 20:05)

New:
1. **Well-engineered repos need zero fixes and reproduce in minutes — if you run their documented command.** `uv.lock` + a CLI + documented output paths turned a 45-min "failure" (the runner executed prose) into a 5-min exact reproduction. The spec's `entrypoint_confidence: high` plus a back-ticked command is the strongest signal to bypass the generic runner entirely.
2. **Per-stage metrics files make the before/after claim mechanical.** Tabulate `geometries/*/stages/*/metrics.json` (stage × metric) instead of reading the root summary only; the root file shows the final stage, the claim is about the *contrast* between stages.
3. **Judge the reported variant.** Plain GFAL sat 0.03 outside the target ranges on one geometry; GFAL+ (what the post reports) was inside on both. Say which variant the ranges apply to rather than averaging them.

Confirmed: lessons-4 #3/#4 (verbatim commands; `uv sync`), lessons-synth P2/P6.
