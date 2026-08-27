# lessons-7 — from R12 and R15 (2026-08-27 18:00)

New:
1. **Notebook `source` can be a string or a list.** `nbformat` allows both; iterating a string yields characters, so a line-wise rewrite silently does nothing (two of my stub attempts "succeeded" with 0 changes). Normalise with `src.splitlines(keepends=True)` and assert the replacement count > 0 before queuing a rerun.
2. **Plotly figures saved as HTML carry the full data**: `Plotly.newPlot("<id>", [traces], layout)` with `z` either a nested list or `{"dtype","bdata","shape"}`; a 15-line extractor turns a "look at the heatmap" claim into diag/off-diag statistics. Prefer that over eyeballing PNGs, and keep the PNGs as the human-facing artefact.
3. **Placeholder secrets in notebooks** (`login("Your hf token")`) are a distinct failure class from missing modules: the call raises on an invalid token even though the machine already has a cached one. Stub the call in a copy; never paste a token into a notebook.
4. **Partial-claim repos are common**: the spec's blockers said the LM half had no code, and it didn't. Judge the half that exists, write UNRESOLVED for the rest, and do not let a clean toy result stand in for the language-model claim in the ledger's notes.

Confirmed: lessons-2 #4 (missing import → copy + one cell), lessons-3 #1 (figure data > pixels), lessons-5 #1 (pre-install all imports).
