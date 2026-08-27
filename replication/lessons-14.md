# lessons-14 — from R3b (2026-08-27 21:25)

New:
1. **A repo's own `verify` defines what the author guarantees — read which claims it covers.** `verify.py` checked six Haar-statistics numbers and none of the EV-recovery numbers; "reproduces 6/6" was true and irrelevant to the headline. Map `verify` targets against `spec.json[target_value]` before treating a green verify as a reproduction.
2. **Compound claims deserve component-wise verdicts in the notes and the binary from the spec's `target_value`.** Two components exact, one off by 2×: the row is `false` because the spec names the failing number, and the notes carry the two ✓s so the taxonomy is not misread as "pipeline broke".
3. **Distinguish alignment EV from SAE-reconstruction EV.** The toy artefact reports both (`alignment.rot_EV` ≈ 0.93–0.96 vs `sae_post_rotation.rotated_EV` ≈ 0.95–0.97); the Pythia fast panel reports only the alignment EV. When the paper says "post-rotation EV", find which JSON key `PAPER_NUMBERS.md` points at before comparing.
4. **`fetch-artifacts` is part of the entrypoint.** Cached activations/SAEs live outside the lite clone; the first rerun failed for that alone. Any repo with an `artifacts/` directory and a `fetch` subcommand needs the fetch in the queued command.
5. **Rebuilding a deleted venv for a 5-minute post-hoc check is fine** (`tree_prep.sh <dir>` ≈ 4 min from the uv cache) — the disk-bounded design does not block follow-up analysis.

Confirmed: lessons-synth P6 (judge from data), P7 (component-wise), lessons-4 #1 (which measure the claim names).
