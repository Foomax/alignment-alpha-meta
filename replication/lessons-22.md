# lessons-22 — batch R13c/R27/R28/R30/R25 (2026-08-28 01:55)

New:
1. **A `sys.modules` fake for `google.colab` must also set `__spec__` and `__path__`.** Bare `ModuleType` objects have `__spec__=None`; `from google.colab import X` then raises `ValueError: __spec__ is None` under importlib. Set `__spec__ = importlib.util.spec_from_loader(name, None)` and `__path__=[]` on both `google` and `google.colab`. (Third iteration of this stub — get it right once in a reusable helper.)
2. **EleutherAI's `sparsify` is distributed as `eai-sparsify`** (PyPI metadata name) but imports as `sparsify`. `pip install "sparsify @ git+..."` fails the name check; use `pip install "git+https://github.com/EleutherAI/sparsify.git"` (no name constraint) — it provides `import sparsify`.
3. **Repos that `assert Path(__file__).parent.name == "<reponame>"`** need to be run from a directory of that name. Symlink `<reponame> -> src` and run from the symlink; don't rename the checkout.
4. **`torch==2.3.1` fixes `params_t` but re-breaks transformer-lens** (unpack arity), a reminder that pinning torch back drags a whole compatibility web with it — sometimes there is no co-installable set, and `env` is the honest terminal state.
5. **Full-vocab-through-hooks sweeps are hours, not minutes** — 2 of 12 layers in 60 min → ~6 h. Grep the entrypoint for a per-layer/per-vocab loop; if the headline is one head/layer, scoping it would edit what's run, so ledger `runtime`.

Confirmed: lessons-5 #4/#5 (version pins, GitHub pkgs), lessons-6 #1 (author-timed boxes), lessons-14 #1 (headline is a variant/subset).
