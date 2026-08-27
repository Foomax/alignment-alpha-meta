# lessons-18 — from R25 (2026-08-27 22:20)

New:
1. **Stub a Colab import by making it resolve, not by deleting it.** Commenting `from google.colab import files` leaves later `files.download(...)` calls referencing an undefined name (NameError, not the `except ImportError` the author wrote), and replacing the import line with a multi-line class breaks single-statement blocks (`try:`/`if:`) → IndentationError. Correct: prepend one cell that registers a fake module in `sys.modules['google.colab']` with no-op `files`/`drive`/`userdata`, and leave every import line untouched. The author's own `try/except ImportError` then passes.
2. **A notebook that fails at a *save/upload* cell has usually already produced the result.** R25's adapter was trained and saved before the failing download cell; with `--allow-errors` the metric cells would have been captured. Always pair notebook reruns with `--allow-errors` (lesson 12) *and* fix trailing Colab plumbing so the run is clean.
3. **Verify a generated notebook copy by `ast.parse` on each edited cell before queuing** — it catches indentation/name breakage in seconds, versus a 10-minute run that dies at the end.

Confirmed: lessons-12 (--allow-errors), lessons-7 #1 (string/list sources), lessons-3 #2 (Colab).
