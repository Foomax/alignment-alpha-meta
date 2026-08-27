# lessons-synth (v2) — synthesis of lessons-1 … lessons-22 (2026-08-28 04:40)

Supersedes the v1 synthesis. Source: ~50 hours replicating alignment-forum experiments on one RTX 3090 — 3 protocol replications with follow-ups, 32 minute-class experiments, six rerun/late passes, one usage pause, one disk-full incident, and a long tail of dependency-drift cases. Part 1: principles. Part 2: the phase checklist. **Part 3 is new and the most reusable: a symptom→cause→fix failure-mode catalog.**

---

## Part 1 — Principles (unchanged from v1, two added)

**P1. Check the system before the science.** Nearly every hour lost was infrastructure wearing an experiment's mask: a stalled download that looked like model loading; a full disk that looked like a burst of instant failures; a launcher shell matching its own `pgrep`; a runner feeding a notebook's JSON to Python; a SIGKILL that was RAM-OOM not GPU-OOM. When a run fails fast, is silent, fails in a burst, or exits 0 in 0 min, verify disk/RAM/network/process/invocation before reading the traceback as science.

**P2. The catalogue describes; it does not command.** `spec.json.entrypoint` is a *pointer* to where the headline is computed — prose ~1/3 of the time, often step-N of a pipeline, sometimes a chain, sometimes the real command in back-ticks, sometimes a subset (the "fact variant"), sometimes a function library with no `__main__`. Read and translate every entrypoint; never execute it verbatim. This was the single largest failure source.

**P3. Environments are budgets: time, VRAM, system RAM, disk, and library epochs.** Time-box from the author's per-item timing; expect 80 GB-era batch sizes to OOM on 24 GB and fp32×N model copies to OOM 31 GB RAM; one torch venv ≈ 5 GB and thirty fill a drive; 2024–25 repos silently break under 2026 majors (`transformers 5`, `datasets 4`, `sae-lens 6`, `setuptools 81`, `torch 2.6`).

**P4. Fix the environment, never the measurement — on copies, one named `--fix` line each.** Imports, paths, `PYTHONPATH`, batch size, device, dtype, version pins, Colab stubs, placeholder logins, submodules, artifact fetches, symlinked dir names: all environment. Prompts, thresholds, dataset slices, metrics, seed counts: a different experiment. Work on notebook copies and wrapper scripts, never the author's files.

**P5. Install the whole environment at once, atomically-safe.** Scan every import and install the list; but `uv pip install a b c` fails wholesale on one bad name, so fall back to per-package on batch failure.

**P6. Judge from data, not pixels or prose.** Executed notebooks and saved HTML carry the figure arrays (`bdata` base64; `Plotly.newPlot`); reading plot *images* is right for a curve-shape claim; read the author's committed outputs first; `git log -S` the config to test whether the paper's setting still exists.

**P7. Pre-register, honour the rule, disclose the deviation first — and judge the measure the claim names.** Binary reflects the scientific claim; the notes' first sentence carries any strict-rule deviation. Judge the named measure (ablation vs DLA), map ordinals to indices, report mean/min/fraction for "~90%" claims, split compound claims, mark unmeasured halves UNRESOLVED. **Match the target to the right variant/subset before declaring non-reproduction** (peppinob's headline was the fact subset, not the default).

**P8. A satisfied training loss / a green `verify` / a committed graph is not a reproduction.** Transfer can be ≈0 while the objective is met; a coherence gate can be the whole effect; a repo's `verify` may check numbers unrelated to the headline; a byte-identical recompute of committed artefacts is weaker than training from scratch. State which tier a row is (below).

**P9. Sequential, observable, resettable, disk-bounded automation.** One GPU job at a time (busy = python-on-GPU OR runner-pid-alive); one log line per node with a monitor; a plain-text done-list you can reset; relabel not overwrite prior `RUN-EXIT`; **delete the venv after each run and refuse to start below a disk floor**; pause the agent, not the GPU.

**P10. Rank follow-ups by "would this flip the verdict?", not by cost.** Paper hyperparameters and ablation tables changed stories; extra seeds on settled questions did not.

**P11. Outward-facing actions are minimal and confirmed.** Forks/pushes/issues: least that satisfies the literal ask, confirm before scaling; never push to authors' repos; never paste secrets into notebooks.

**P12. Keep two readers in mind.** Ledger row is the deliverable; human doc and machine doc are patched as results land; each finished run gets a handoff (state) + lessons (delta).

**P13 (new). Don't grind the tail past its information value.** The first ~15 nodes established the reproduction rate and the taxonomy; nodes 16+ mostly re-confirm "engineering rot" at 2–3 requeues each. Cap requeues (≤2–3), then ledger the honest reason (`env`/`runtime`/`model-access`) and move on. A clean `env` row is a finding, not a failure.

**P14 (new). The harness is a deliverable.** The prep/autofix/import-scan/notebook-stub/queue tooling + this synthesis is a reusable replication harness — often worth more than the marginal next row.

---

## Part 2 — Phase checklist (condensed; full detail in v1 history / Part 3)

- **Before GPU:** export `HF_HUB_DISABLE_XET=1 HF_HUB_DISABLE_TELEMETRY=1 WANDB_MODE=disabled PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false`; `df -h /` (floor ≥25 GB), free ledgered experiments' venvs/models/intermediates; pre-download models over HTTP in the background; read the author's committed outputs and per-item timing; `git log -S` the config; pre-register the criterion in `run.log`.
- **Env (`tree_prep.sh`):** sanitise python version; `pip "setuptools<81" wheel`; torch from the CUDA index (**old torch pins need their own index**, `torch==2.3.1`→cu121); requirements then editable (or `uv sync` if `uv.lock`); notebook stack for `.ipynb`; full `tree_imports.py` list; per-package fallback on batch failure; delete venv after run.
- **Entrypoint translation:** back-ticked command → verbatim; `a.sh→b.py` → chain with venv on PATH (`bash -e`); `.ipynb` → nbconvert `--execute --allow-errors`; `pkg/module.py` relative imports → `python -m pkg.module` from root; `from src.x` → `PYTHONPATH` = parent/grandparent/root; grep for `load_file/open/read_csv` inputs and prepend the generator (`prepare_*.py`); Colab → rewrite `/content`, stub `google.colab` in `sys.modules` (with `__spec__`+`__path__`), stub `login()`; `assert dir.name=="X"` → symlink `X→src`.
- **Run:** one GPU job at a time; time-box from author timing; batch ≤8 on 24 GB; `--quick` may swap model+drop controls; distinguish a *stall* (kill) from *transient retries* (wait); "EXIT 0 in 0 min" or a burst of "EXIT in 0s" is a red flag.
- **Judge:** the named measure; ordinals→indices; mean/min/fraction; decode plotly arrays; per-condition n; raw generations at the extreme setting; does the regulariser *bind*; two seeds when SD 5–7; cross-model tally; deviation in notes' first sentence; hosted API → `api-key`; partial → UNRESOLVED; never ledger a failure pointing at your own invocation.
- **Ops:** VERDICT+`report.py` → human/machine docs → commit `replication/` → push; forks allowlisted; mirror `--no-links`; `HF_HOME` off NTFS.

---

## Part 3 — Failure-mode catalog (symptom → cause → fix)

The reusable core. When a node fails, match the symptom.

| symptom (in log) | cause | fix |
|---|---|---|
| silent, no writes/socket for >5 min, GPU idle | xet download stall | `HF_HUB_DISABLE_XET=1`; kill, delete `.incomplete`, HTTP re-download |
| burst of "EXIT in 0s", ENOSPC, lost command output | disk full (venvs + uv cache + HF cache) | free ledgered experiments' venvs/models/intermediates; floor ≥25 GB; delete venv per run |
| `SIGKILL`/137 on a CPU node | system-RAM OOM (fp32×N model copies >31 GB) | edit `DEVICE="cpu"→"cuda"` (fp32×N fits 24 GB GPU); it's a hardware knob |
| CUDA OOM in `calc_nll`/vmap | 80 GB-era batch / full-residual Jacobian on 24 GB | force eval batch ≤8; full-residual Jacobian on a large model = `vram`/UNRESOLVED |
| `ModuleNotFoundError` for a normal package | import scanner missed a transitive dep | pre-install; `typeguard`+`jaxtyping` for transformer-lens; per-package fallback |
| `No module named 'src'` / relative import | wrong CWD / not run as module | `PYTHONPATH`=repo root(s); or `python -m pkg.module` from root |
| `NameError: true` / notebook JSON in traceback | runner ran a `.ipynb`/`.sh` string as Python | dispatch on extension; nbconvert for notebooks |
| `import transformers … TRANSFORMERS_CACHE` | removed in transformers 5 | `transformers<5` |
| `datasets` `HfUriError`/`'imdb'` non-namespaced | removed in datasets 4 | `datasets<4` |
| `sae_lens.toolkit` / `sae_lens.sae` missing | moved/removed across sae-lens majors | `sae-lens<6` (toolkit) / `<4` (sae); may then conflict with torch → `env` |
| KeyError on an SAE release id (`'11-res-jb'`) | sae-lens registry id renamed; lives only in ~1.x–2.x | old sae-lens conflicts with torch 2.6 → usually `env` |
| `pkg_resources` missing (wandb) | setuptools ≥81 dropped it | `setuptools<81` (now global in prep) |
| `params_t` from torch.optim | removed in torch 2.6 | `torch==2.3.1` from cu121 index (may re-break transformer-lens arity → `env`) |
| `not enough/too many values to unpack` in mech-interp | transformer-lens cache/hook API arity drift | match author's transformer-lens version, or `code-bug`/`env` |
| `cannot import name Sae from sparsify` | wrong PyPI `sparsify` (Neural Magic) shadows EleutherAI's | `pip install "git+https://github.com/EleutherAI/sparsify.git"` (pkg is `eai-sparsify`, no name constraint) |
| `No module named e2e_sae.scripts` | author's fork wheel omits `scripts/` | editable clone on `PYTHONPATH`, don't `pip install -e` (it downgrades torch) |
| `mishax`/GitHub-only pkg unresolvable | not on PyPI | `git+https://…`; per-package fallback skips it if unused |
| `google.colab.__spec__ is None` / IndentationError near `try` | Colab stub incomplete or edited the import line | leave imports intact; prepend `sys.modules['google.colab']` module with `files/drive/userdata` **and** `__spec__`+`__path__` |
| `login("Your hf token")` raises | placeholder Colab secret | stub the call in a copy; cached token is used |
| `FileNotFoundError: prompts/prompts.json` (input) | a `prepare_*.py` generates it (README step 1) | prepend the generator; don't confuse with an output dir you deleted |
| `FileNotFoundError: patched_merged.safetensors` | earlier pipeline step produces it | build the chain from `config.py` PATH constants → grep for the `save_file` producer |
| `assert dir.name == "<repo>"` | script requires its dir be named `<repo>` | `ln -sfn src <repo>`; run from the symlink |
| `AssertionError: upload X to /content` | Colab file-upload cell | rewrite `/content` paths to the repo checkout in a notebook copy |
| exits 0 in 0 min, no output, no `__main__` | entrypoint is a function library needing uncommitted data | `unclear-entrypoint` |
| runs, times out, only k/N of a loop done | multi-hour training/sweep mis-tagged "minutes" | `runtime` (scoping it would edit what's measured) |
| downloads a private/token'd or 2×7B checkpoint set | author's private HF token / 48 GB-card design | `model-access` / `vram`; don't work around |
| entrypoint POSTs to a hosted API (even keyless) | not local inference | `api-key` |

---

## Part 4 — Reproduction quality tiers (use these when judging)

- **T-exact:** trained/computed from scratch, matches to stated precision (AntiPaSTO-270M, sandbagging-03, cross-model-CKA, ioi, induction-head, mild-rgb, coolvision, phusroyal, mshinkle, seq2feature, matryoshka-toy, ai-forever, cywinski-headline).
- **T-recompute:** recompute over the author's *committed* artefacts, matches (often byte-identical) but did not regenerate the underlying models (vaiyr, peppinob). Weaker evidence — say so.
- **T-partial/direction:** some components match, others don't, or direction-only (jordanmccann toy+Haar ✓ / Pythia-EV ✗; codi-recovery ~7% vs 20%).
- **T-not:** located and genuinely off (AntiPaSTO config-drift).

## Part 5 — Numbers for this card (RTX 3090, 24 GB, 31 GB RAM)
AntiPaSTO seed 47 min (270M 33) · Qwen2.5-1.5B GSM8K 350-q pass ~1 min/15 GB · CKA+500-perm per 1–3B pair ~100 min · debiased-CKA extraction ~5 min/model · quick notebooks 1–3 min once the venv is right · venv prep 3–12 min · torch venv ≈5 GB · uv cache grows unboundedly (the disk sink) · HF over HTTP ~6 MB/s.
