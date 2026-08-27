# lessons-1 — what the first ~30 hours of replication on one 3090 taught (2026-08-27)

For other instances running this ledger. Organised as dead-ends (don't repeat), best approaches (do repeat), optimisations (do earlier), and judgement lessons (how to read results). Concrete, with the incident that taught each.

## A. Dead-ends — things that cost hours and produced nothing

1. **Trusting a silent download.** The xet transport froze at 99.99 % of a 2 GB file for 38 min with an empty log and an idle GPU; it looked exactly like "model loading". Cost 50 of a 240-min budget. → `HF_HUB_DISABLE_XET=1` in every shell on this machine; if a load step is silent > 5 min, `stat` the `.incomplete` blob and `ss -tnpi` on the process before waiting longer. Pre-download models with `snapshot_download` *outside* the budgeted run.
2. **Heredocs in background launchers.** The harness wraps every Bash call as `bash -c "<whole command text>"`, so any `pgrep -f <pattern>` whose pattern appears in the command text matches the launcher itself: two queue scripts deadlocked for 35 min; a `pkill -f` killed its own shell. → Write scripts with the Write tool; anchor patterns to the executable (`'^(uv run python|[^ ]*/python3?) nbs/train\.py'`); launch with `setsid nohup … & disown`.
3. **`nvidia-smi` as the only "GPU busy" signal.** Compute-apps lists desktop processes (cosmic, Chrome) — filter on `python` — and has gaps between an experiment's phases (extraction → CKA), during which a second job started. → busy = python on GPU **or** the runner script's pid.
4. **Executing the catalogue's `entrypoint` string literally.** ~1/3 of spec entrypoints are prose ("`python -m replicate run-fast (replicate/run_fast.py; e.g. …)`", "`full_experiment.sh (runs …)`", "`x.ipynb (per-head ablation loop)`"). The thin runner ran them as `python <string>`; Python even executed a notebook's JSON (`NameError: name 'true'`) which I first misfiled as an author bug. → Parse the entrypoint (strip parenthetical descriptions; dispatch on `.ipynb`/`.sh`/`-m`), or hand-write invocations for the failures in a second pass. Never ledger a failure whose traceback points at *my* invocation.
5. **Budget guesses from "minutes" tags and extraction-only time-boxing.** Experiment 01's CKA + permutation stages took ~100 min per eval (extraction ~5 min/model); I time-boxed only extraction, so eval B overran the 240-min budget by 92 min. A catalogue "45 min" box killed a run at 77/200 prompts that the author's own timestamps put at ~50 min. → Time-box every stage; prefer author-stated runtimes; read the author's committed logs/timestamps for per-pass timing before choosing the box.
6. **Bulk outward-facing actions without asking.** I forked 34 repos in one loop because the request said "each project"; the user meant one. Deleting 31 forks was easy, but the right move was to fork the three with work and ask about the rest. → For anything visible outside the machine (forks, pushes, issues), do the minimum that satisfies the literal request and confirm before scaling.
7. **`--quick` modes as a substitute for the real metric.** AntiPaSTO's `--quick` evaluates a different model *and* a 64-dilemma subset with no "arbitrary" control questions, so the headline F1 is NaN by construction. Ten minutes lost, plus a misleading "—" table. → Check what a quick flag actually changes before using it for a claim; full runs were 2–3 min anyway.
8. **Chasing seeds on a settled question.** Extra 1B seeds/personas/Qwen seeds would have refined numbers nobody would act on differently. The information-dense follow-ups were the ones that could *flip* a conclusion (paper hyperparameters; the 270M ablations). → Rank follow-ups by "which outcome would change the verdict", not by cheapness.

## B. Best approaches — what reliably worked

1. **Pre-register the pass/fail rule in `run.log` before the run**, verbatim, then honour it — and when a strict rule fails on noise (03: +1.0 pp within 1 SE), record the strict result *and* the judgement, deviation first line of the notes. The ledger's binary should reflect the scientific claim; the deviation must be impossible to miss.
2. **Run the control first** (01: within-family eval C before cross-family). A broken pipeline then shows as a missing 0.9, not a plausible 0.2.
3. **Read the author's own committed outputs before judging.** Their CSVs gave the noise-0 gap, per-seed variance, and the "6 of 10 seeds" baseline for 03; their `outputs/` CSVs gave 3-decimal targets for 01; the AntiPaSTO README table vs. `git log -S` on `config.py` exposed the config drift.
4. **`git log -S "<default value>"` on the config file** is the fastest way to test "does the repo still contain the paper's setting?". Twenty seconds; it decided the AntiPaSTO story.
5. **Environment-only fixes, each one a `--fix` line, with the failing code path named.** Missing import that breaks *import* of a helper module (03, 15) = environment; changing a prompt/threshold/dataset slice = a different experiment. The wrapper pattern (import the author's script unmodified, override one module-level name, monkeypatch a batch size) keeps the boundary clean and diffable.
6. **One sequential GPU queue per phase, each node reporting one line to a log, a monitor on that log.** Per-node notifications are the right granularity; per-epoch monitors got auto-throttled (tqdm floods).
7. **Ledger row first, reports second, follow-ups third.** The row is the deliverable; reports (LLM + human) are patched as follow-ups land; nothing is re-derived twice.
8. **Cross-seed adapter similarity (cos-sim of learned parameters)** is a cheap CPU check that distinguishes "unlucky seed" from "the method converges to the same weak solution" — it settled AntiPaSTO's 1B result in one minute.
9. **Per-axis / per-condition sample sizes next to every per-axis number.** The "Friendly 52.4" that would have been a headline was n=4.

## C. Optimisations — do these earlier next time

1. **Prep the environment in the tree, not in `run.sh`**: sanitise `python_version` (`3.13.13`, `>=3.10`, `3.11+` all appeared), install `pip setuptools wheel` (uv venvs have no pip, so notebooks' `%pip` cells fail), torch from the CUDA index, requirements + editable install, and the notebook stack (`jupyter nbconvert ipykernel matplotlib ipympl`) for `.ipynb` entrypoints. This turned 0-second failures into real runs.
2. **Auto-fix loop on `ModuleNotFoundError`** with a module→package map and ANSI stripping (nbconvert colours its tracebacks). Right ~60 % of the time; wrong when the package is the author's GitHub fork (`e2e_sae`) or when an API moved between majors (`sae_lens.toolkit` → pin `<6`). Log every auto-install for the ledger.
3. **Download once, over HTTP, in the background, before the GPU job**; 22 GB took 106 min here (~6 MB/s).
4. **Pin the major version the author ran under** when a repo has no lock (03: `transformers<5`); uv's resolver will otherwise hand you next year's API.
5. **On a 24 GB card, expect 80 GB-era eval batch sizes to OOM** (fp32 logits over a 262k vocab at batch 32 ≈ 10 GB). Batch size is an environment knob; force it from the wrapper.
6. **Write the analysis script while the run is in flight** and dry-run it on partial outputs (03: caught nothing wrong, but it made the ledger step a 2-minute job).
7. **Keep `run.log` parseable**: `report.py` greps the *first* `RUN-EXIT`; relabel failed attempts (`ATTEMPT1-EXIT`) so the ledger reflects the successful run, and say so in the notes.
8. **Watcher pattern for "commit as we go"**: a tail-based watcher on the tree log that commits the meta repo after each node; publishing to forks gated by an allowlist.

## D. Judgement lessons — reading results

1. A training loss that reaches its objective proves nothing about transfer (AntiPaSTO 1B: loss −13, F1 2; random-dims seed 43: loss −14, F1 2.7). Look at the eval's own diagnostics (Tgt vs Arb flips, pmass, per-condition n).
2. A metric's coherence/format gate can be the whole result: 79 % of `**Yes**` answers turned a ≈21 into 0.7. Always inspect raw generations at the extreme coefficient before believing a collapse.
3. "Reproduces on the small model, not on the headline model" is a common and informative pattern (AntiPaSTO 270M ✓, 1B ✗, Qwen-0.6B ✗) — report the cross-model tally, not one number.
4. Ablation tables need two seeds minimum when the paper's own SD is 5–7; one of four "load-bearing" components was load-bearing, one was seed-fragile, two were inert because the loss terms never activate at that scale. Check whether a regulariser *binds* (its logged loss) before interpreting its ablation.
5. Deterministic small-model notebooks (GPT-2 IOI, character-level induction head, shipped per-cell results) reproduce to three decimals — those rows are "did the pipeline survive", and that is still a valid ledger signal.
6. A qualitative claim ("noise partially undoes sandbagging") can reproduce *more strongly* than in the author's data (9/10 seeds vs 6/10); say so, and look for the mechanism the extra clarity exposes (bare-guess share 47 % → 11 %).

## E. Numbers worth remembering (this card)

- Gemma-3-1B AntiPaSTO seed: 47 min (85 s/epoch × 30 + 4 min eval); 270M: 33 min.
- Qwen2.5-1.5B GSM8K 350-question greedy pass, 400 new tokens, batch 350: ~1 min, 15 GB.
- Debiased CKA + 500-perm tests for a 1–3B pair: ~100 min; extraction ~5 min/model.
- Quick notebooks (GPT-2 small scale): 1–3 min once the venv is right; venv prep 3–5 min.
- HTTP download from HF: ~6 MB/s.
