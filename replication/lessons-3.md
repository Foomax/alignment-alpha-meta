# lessons-3 — from nodes 20–22 (2026-08-27 15:25)

New:
1. **Qualitative claims can be judged quantitatively from the notebook's own figures.** Executed notebooks keep plotly figures as JSON with typed binary arrays (`{"dtype":"f8","bdata":"<base64>"}`); decode with `np.frombuffer(base64.b64decode(bdata), dtype)`. That turns "long-tailed, more in later layers" into per-layer percentiles and tail fractions in one script — far better evidence for a ledger than eyeballing a PNG (which nbconvert does not even produce for plotly).
2. **Colab notebooks hard-code `/content`.** Without root you cannot create it, but you do not need to: copy the notebook and rewrite the path string in the cell sources (7 lines here), record it as an environment fix, run the copy. Same class as the protocol-prescribed output-dir edit in experiment 03.
3. **Chain entrypoints ("a.sh → b.py → c.py") must be run as a chain with the venv on `PATH`**; the thin runner fed the whole string to Python (SyntaxError in 0 s). Detect `->` or `→` in an entrypoint and split.
4. **Three auto-fix rounds is one too few for TransformerLens notebooks** (plotly + jupyter stack + transformers + transformer-lens is already four packages). Pre-install `transformer-lens transformers plotly` for any `.ipynb` whose source mentions `HookedTransformer`.

Confirmed from lessons-1/2: A4, C1, C2; lessons-2 #1 (entrypoint = pointer).
