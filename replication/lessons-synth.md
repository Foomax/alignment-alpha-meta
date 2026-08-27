# lessons-synth — synthesis of lessons-1 … lessons-8 (2026-08-27 18:25)

Source: eight lessons files written during ~36 hours of replicating alignment-forum experiments on one RTX 3090 (2 protocol replications with follow-ups, 31 minute-class experiments, two rerun passes, one usage pause, one disk-full incident). Part 1 abstracts them into principles; Part 2 is the complete practical checklist, deduplicated and ordered by the phase in which it applies.

---

## Part 1 — Abstract lessons (the principles behind the incidents)

**P1. Check the system before the science.** Almost every hour lost was to infrastructure that *looked* like the experiment: a stalled download that looked like model loading (L1-A1), a full disk that looked like sixteen instant failures (L8-2), a launcher shell that matched its own `pgrep` (L1-A2), a runner that fed a notebook's JSON to Python and produced a "NameError" I first blamed on the author (L1-A4). Rule: when a run fails fast, is silent, or fails in a burst, verify disk, network, process and invocation before reading the traceback as science.

**P2. The catalogue describes; it does not command.** The spec's `entrypoint` is a pointer to where the headline number is computed — often prose, often step 7 of a pipeline, sometimes a chain, sometimes with the real command in back-ticks (L1-A4, L2-1, L3-3, L4-3). Treat every entrypoint as something to *read and translate*, never to execute verbatim. Half of all first-pass failures were this one mistake.

**P3. Environments are budgets: time, VRAM, disk, and library epochs.** Time-box every stage from the author's own per-item timings (L1-A5, L6-1); expect 80 GB-era batch sizes to OOM on 24 GB (L1-C5); one torch venv ≈ 4 GB and thirty of them plus a model cache fill a drive (L8-1); and 2024–25 repos silently break under 2026 majors (`transformers` 5, `datasets` 4, `sae-lens` 6, `torch` 2.6) — pin to the author's epoch (L1-C4, L5-4).

**P4. Fix the environment, never the measurement — and make every fix a diffable, named line.** Missing imports, paths (`PYTHONPATH`, Colab `/content`), placeholder secrets, batch sizes, version pins, GitHub-only packages, submodules: all environment, all recorded as `--fix`. Prompts, thresholds, dataset slices, metrics: a different experiment, never touched (L1-B5, L2-4, L3-2, L7-3). Work on copies (notebook copies, wrapper scripts, monkeypatched module names), not on the author's files.

**P5. Install the whole environment at once.** One missing module per run is the wrong unit; scan every import and install the list up front (L2-2, L5-1). The auto-fix loop is a safety net for what the scan misses (author forks, moved APIs), not the primary mechanism.

**P6. Judge from data, not pixels or prose.** Executed notebooks and saved HTML carry the figure arrays; decode them and turn "long-tailed" or "no holes" into percentiles and counts (L3-1, L7-2). Read the author's committed outputs first (L1-B3); run the control first (L1-B2); `git log -S` the config to test whether the paper's setting still exists (L1-B4).

**P7. Pre-register, then honour the rule — and disclose the deviation first.** Write the pass/fail criterion into `run.log` before running; if a strict rule fails on noise, the ledger's binary should reflect the scientific claim *and* the first line of the notes must say the strict rule failed (L1-B1). Judge the measure the claim names (ablation vs DLA), map ordinals to indices, report mean/min/fraction for "~90 %" claims, and mark unmeasured halves UNRESOLVED rather than folding them in (L4-1, L4-2, L6-2, L6-3, L7-4).

**P8. A satisfied training loss is not a result.** Transfer can be ≈0 while the objective is met (L1-D1); a coherence/format gate can be the entire effect (L1-D2); ablations of regularisers that never bind show nothing (L1-D4); small-model success with headline-model failure is a pattern to report as a tally (L1-D3). Seeds: two minimum when the paper's SD is 5–7; cross-seed parameter similarity distinguishes bad luck from a weak solution (L1-B8, L1-D4).

**P9. Sequential, observable, resettable automation.** One GPU job at a time; a busy check that combines `nvidia-smi` *and* runner pids (L1-A3); one log line per node with a monitor on it (L1-B6); a done-list you can reset by editing a text file (L8-3); relabel, never overwrite, earlier `RUN-EXIT` lines (L1-C7). Pause the agent, not the GPU (L5-6).

**P10. Rank follow-ups by "would this flip the verdict?", not by cost.** Extra seeds on settled questions are waste; the paper's own hyperparameters and the ablation table were the follow-ups that changed the story (L1-A8).

**P11. Outward-facing actions are minimal and confirmed.** Forks, pushes, issues: do the least that satisfies the literal request, confirm before scaling (L1-A6). Never push to authors' repos; never paste secrets into notebooks (L7-3).

**P12. Keep two readers in mind at once.** The ledger row is the deliverable; the human doc and the machine doc are patched as results land, never re-derived (L1-B7). Every finished run gets a handoff (state) and a lessons entry (delta) so the next instance starts warm.

---

## Part 2 — Compiled practical lessons (checklist by phase)

### 2.1 Before touching the GPU
- [ ] `export HF_HUB_DISABLE_XET=1 HF_HUB_DISABLE_TELEMETRY=1 WANDB_MODE=disabled PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false` in every shell. (L1-A1)
- [ ] `df -h /` — refuse to start a node below 12 GB free; delete venvs of ledgered experiments; delete re-downloadable models whose experiments are done; delete raw activation/intermediate dumps once derived CSVs are saved. (L8-1, L8-4, L8-5)
- [ ] Pre-download models with `snapshot_download` over plain HTTP in the background, *outside* any budgeted run (~6 MB/s here; 22 GB ≈ 106 min). (L1-C3)
- [ ] Read the author's committed outputs/logs/timestamps: they give the targets to 3 decimals, the per-seed baseline, and the per-pass runtime. (L1-B3, L6-1)
- [ ] `git log -S "<paper's default value>" -- <config file>` to confirm the repo still contains the paper's configuration. (L1-B4)
- [ ] Pre-register the pass/fail criterion verbatim in `run.log`. (L1-B1)

### 2.2 Building the environment (per experiment, `tree_prep.sh`)
- [ ] Sanitise `python_version` to `3.X` (values like `3.13.13`, `>=3.10`, `3.11+` occur). (L1-C1)
- [ ] `uv venv`, then `pip setuptools wheel` (uv venvs ship without pip; `%pip` cells fail otherwise). (L1-C1)
- [ ] torch from the CUDA index; **a pinned old torch needs its own index** (`torch==2.3.1` → cu121). (L5-3)
- [ ] `requirements*.txt`, then editable install if `pyproject.toml`/`setup.py`; if the repo has `uv.lock`, use `uv sync` + `uv run` instead. (L4-4)
- [ ] Notebook entrypoint → `jupyter nbconvert ipykernel matplotlib ipympl`; if the source mentions `HookedTransformer` → also `transformer-lens transformers plotly`. (L1-C1, L3-4)
- [ ] Run `tree_imports.py <repo>` and install the whole list once. (L5-1)
- [ ] Default pins for a 2024–25 repo with no lock: `transformers<5`, `datasets<4`, `sae-lens<6` (`<4` for the `'11-res-jb'` id scheme), torch per repo. (L5-4)
- [ ] GitHub-only packages → `git+https://…`; wheel omits a subpackage → editable clone; `.gitmodules` present → `git submodule update --init --recursive`. (L5-5)
- [ ] Delete the venv after the run (one on disk at a time). (L8-1)

### 2.3 Translating the entrypoint (never execute the spec string)
- [ ] Back-ticked command in the entrypoint → use verbatim. (L4-3)
- [ ] `a.sh → b.py → c.py` → run as a chain with the venv first on `PATH`; author `.sh` files with `bash -e`. (L3-3, L5-2)
- [ ] `.ipynb` → `python -m jupyter nbconvert --to notebook --execute <nb> --output <path> --ExecutePreprocessor.timeout=-1`. (L1-A4)
- [ ] `pkg/module.py` with relative imports → `python -m pkg.module` from the repo root. (L1-A4)
- [ ] `from src.x import …` → `PYTHONPATH` = script's parent, grandparent and repo root. (L2-3)
- [ ] `grep -n "load_file\|open(\|read_csv\|torch.load"` the entrypoint for inputs; if an earlier numbered script produces them, queue the chain. (L2-1)
- [ ] Artifacts commands (`fetch-artifacts`, `setup_box.sh`) come first; if they use the author's private token → `model-access`/`data`. (L2-1)
- [ ] Colab notebooks: rewrite `/content` paths in a *copy*; stub `from google.colab import …`; stub `login("Your hf token")` (cached token is used). Notebook `source` may be a string — `splitlines(keepends=True)` and assert replacements > 0. (L3-2, L7-1, L7-3)
- [ ] Compound targets across sibling scripts → run the entrypoint, judge it, queue the sibling, mark the rest UNRESOLVED. (L6-3)

### 2.4 Running
- [ ] One GPU job at a time; busy = `nvidia-smi --query-compute-apps` shows `python` **or** a runner script pid is alive (`pgrep -f '^bash \./tree_…\.sh'`). (L1-A3)
- [ ] Time-box every stage, from the author's per-item timing × items + model load (read the first minute of the progress bar). Catalogue "45 min" is a guess. (L1-A5, L6-1)
- [ ] On a 24 GB card force eval batch ≤ 8 from a wrapper when the script floors it at 32 (fp32 logits over a 262k vocab at batch 32 ≈ 10 GB). (L1-C5)
- [ ] Check what a `--quick` flag actually changes before using it for a claim (may switch model *and* remove the control items). (L1-A7)
- [ ] Transient `HTTPSConnectionPool` errors self-heal inside a generous box; a *silent* stall (no writes, no socket traffic for minutes) never does — kill, delete `.incomplete`, re-download over HTTP. (L1-A1, L6-4)
- [ ] Scripts written with the Write tool, launched `setsid nohup … & disown`; `pgrep`/`pkill` patterns anchored to the executable; no heredoc containing the pattern text. (L1-A2)
- [ ] One log line per finished node → `tree.log`; monitor that, not per-epoch output. (L1-B6)
- [ ] "EXIT 0 after 0 min", or a burst of "EXIT in 0 s" lines, is a red flag: read the log / check `df` before believing it. (L5-2, L8-2)
- [ ] Relabel earlier `RUN-EXIT` lines to `ATTEMPT-EXIT` before a rerun; `report.py` greps the first `RUN-EXIT`. (L1-C7)
- [ ] Done-lists are plain text files you can reset. (L8-3)

### 2.5 Judging
- [ ] Judge on the measure the claim names (e.g. ablation, not DLA); record the other measure's ranking in the notes. (L4-1)
- [ ] Map ordinals to 0-indexed positions before reading tables. (L6-2)
- [ ] For "~X %" sub-claims report mean, min and the fraction of items where it holds. (L4-2)
- [ ] Decode plotly arrays (`bdata` base64 in executed notebooks; `Plotly.newPlot(...)` in saved HTML) and compute the statistic instead of eyeballing PNGs. (L3-1, L7-2)
- [ ] Always print the per-condition n next to per-condition numbers. (L1-B9)
- [ ] A satisfied training loss ≠ transfer; inspect the eval's own diagnostics and the raw generations at the extreme setting (format/coherence gates). (L1-D1, L1-D2)
- [ ] Check whether a regulariser *binds* (its logged loss) before interpreting its ablation; two seeds minimum when the paper's SD is 5–7. (L1-D4)
- [ ] Cross-seed cosine similarity of learned parameters separates "unlucky seed" from "converges to the same weak solution". (L1-B8)
- [ ] Report cross-model tallies (small ✓ / headline ✗) rather than one number. (L1-D3)
- [ ] Deterministic small-model notebooks reproducing to 3 decimals are valid "pipeline survived" rows. (L1-D5)
- [ ] If a strict pre-registered rule fails within sampling error, ledger the scientific verdict and put the deviation in the first sentence of the notes. (L1-B1)
- [ ] Hosted-model APIs (even "no key required") are not local replications → `api-key`. Partial-claim repos → judge what exists, UNRESOLVED for the rest. (protocol rule 5; L7-4)
- [ ] Never ledger a failure whose traceback points at *your* invocation. (L1-A4)

### 2.6 Ops, docs, and outward actions
- [ ] Ledger row first (VERDICT block in `run.log` + `report.py`), then the human and machine docs, then follow-ups. (L1-B7)
- [ ] After every finished run or juncture: `handoff-N.md` (state) + `lessons-N.md` (delta only, cite prior lessons when merely confirming) + a `human-oversight.md` section (ELI5 + "Needs you?"); commit `replication/`; push. (L1-B7)
- [ ] Follow-ups ranked by "could this flip the verdict?" (paper hyperparameters, ablation tables) — not by cost. (L1-A8)
- [ ] Forks/pushes/issues: minimum that satisfies the literal request; confirm before scaling; never push to authors' repos; `publish.sh` is allowlisted to three forks. (L1-A6)
- [ ] Mirror to removable media with `rsync -a --no-links --exclude .venv`; NTFS drops symlinks. (L5-7)
- [ ] Pause the agent, not the GPU: detached queues keep producing; resume = `tail tree.log`. (L5-6)
- [ ] Keep `HF_HOME` off the system drive (ext4/xfs, not NTFS) when a session will touch many models. (L8-4)

### 2.7 Numbers for this card (RTX 3090, 24 GB)
Gemma-3-1B AntiPaSTO seed 47 min; 270M 33 min · Qwen2.5-1.5B GSM8K 350-q greedy pass ~1 min, 15 GB · debiased CKA + 500-perm test per 1–3B pair ~100 min (extraction ~5 min/model) · quick notebooks 1–3 min once the venv is right; venv prep 3–5 min (12 min with a large import list) · HF over HTTP ~6 MB/s · torch venv ≈ 4–5.5 GB.
