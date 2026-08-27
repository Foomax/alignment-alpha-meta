# handoff-synth — operating instructions for the next Claude instance (2026-08-27 18:25)

You are continuing an unattended replication ledger on the user's RTX 3090. This file is the only thing you need to read first; it supersedes `handoff-0 … handoff-12` (kept as history) and bakes in `lessons-synth.md`. Follow it literally.

## 0. Non-negotiable rules (from the replication prompts and the user)
1. **Environment-only fixes.** Never change a prompt, threshold, dataset slice, metric, seed count or model that decides what is measured. Missing imports, paths, `PYTHONPATH`, batch sizes, version pins, Colab stubs, placeholder logins, submodules, artifact fetches — yes, on *copies* or wrappers, each recorded as a `--fix` line.
2. **No hosted-model APIs**, even keyless ones → ledger `--reason api-key`. Do not substitute an open model and call it a replication.
3. **Pin the commit in `spec.json`.** No `git pull`, no HEAD.
4. **One venv per experiment**, built and deleted by the queue; never install into the base environment.
5. **Never push to the authors' repos, open issues, or contact authors.** Pushes go only to the three allowlisted forks under `Foomax` via `publish.sh`; **create no new forks**.
6. **Commit only `replication/`** in `~/alignment-literature-meta-analysis` (`Foomax/alignment-alpha-meta`, branch `master`). The user's other uncommitted files at the repo root are theirs — leave them.
7. **Do not stop for human guidance.** Write what you need in `human-oversight.md` (ELI5 + step-by-step) and keep the GPU busy.
8. **After every finished run or juncture** write `handoff-N.md` and `lessons-N.md` (next: `handoff-13`, `lessons-9`), add a `human-oversight.md` section, commit, push.
9. Report with tiers: `[MEASURED]` / `[INFERRED]` / `[UNRESOLVED]`. No superlatives. A ledger entry is the goal, not a success.

## 1. Where everything is
- Repo: `~/alignment-literature-meta-analysis/replication/` (= `$R` below). Experiments: `$R/experiments/<slug>/` with `spec.json`, `PROMPT.md`, `report.py`, `run.sh`, `run.log`, `ledger.json` (when judged), `src/` (pinned checkout, gitignored), `executed.ipynb`, `prep.log`, `autofixes.txt`.
- Ledger aggregate: `python3 $R/ledger.py`. As of this file: **attempted 13, installs 13, runs 11, located 12, reproduced 10** (01 cross-model ✓ on evals C/A/B; 02 AntiPaSTO ✗; 03 sandbagging-noise ✓; ioi ✓; probe-necessity ✓; induction-head ✓; coolvision ✓; mild-rgb ✓; ai-forever ✓; codi ✓; matryoshka-saes ✓ toy; ak47na `unclear-entrypoint`; jlens-basin-swaps `api-key`).
- Docs: `hand-off.md` (AntiPaSTO/03 planning), `handoff-0…12.md`, `lessons-1…8.md`, `lessons-synth.md`, `human-0.md`, `human-oversight.md` (§0–14), per-experiment reports in the AntiPaSTO, arena-sandbagging and cross-model folders.
- Forks (do not add): `Foomax/AntiPaSTO`, `Foomax/arena-sandbagging-mi`, `Foomax/cross-model-alignment-geometry` (branch `replication-3090`, README with `# human` / `# LLM`). Publish with `bash $R/publish.sh <slug> "<msg>"` after updating `README.human.md` / `README.llm.md` in the experiment folder.
- Mirror: `/media/user/466CD2B96CD2A34B/home/alignment-replication-3090-2026-08/` (NTFS) via `$R/mirror.sh --loop` every 10 min; `last-mirror.txt`; stop with `touch mirror.stop` there. Venvs excluded on purpose.
- Memory notes for the assistant: `~/.claude/projects/-home-user-prompts/memory/` (`replication-ledger-3090`, `github-forks-foomax`, `handoff-lessons-cadence`, `hf-xet-download-hang`, `background-pgrep-launcher-trap`).

## 2. What is running right now (all detached with `setsid nohup`; survive sessions)
- `$R/tree_late.sh` — the **disk-bounded late queue**. Reads `$R/tree_late.txt` (`name|slug|timeout_min|command`), skips names in `$R/tree_late_done.txt`, waits while the GPU is busy or `/` has < 12 GB free, then per entry: `tree_prep.sh` (clone at SHA if missing → venv → pip/torch/requirements/editable/notebook stack/full import list) → command → **deletes the venv**. One line per node to `$R/tree.log`. Stop with `touch $R/tree_late.stop`; resume by removing it and relaunching (`cd $R && setsid nohup ./tree_late.sh > tree_late_nohup.out 2>&1 < /dev/null & disown`).
  - Entries (24): R15 ✓done, R17 ✓done(failed → R17b queued), **R18 running**, R19, R20, R21, R23, R3b, R4b, R5b, R8b, R10b, R13b, R14b, R25, R27, R28, R30, R32, R29, R31, R6b, R12b, R17b.
- `$R/tree_publish.sh` — watcher: after each `NODE … EXIT` line commits `replication/` and pushes (no forking; `publish.sh` is allowlisted).
- `$R/mirror.sh --loop` — the external-drive mirror.
- `tree_queue.sh`, `tree_rerun.sh`, `tree_rerun2.sh` are **finished**; do not relaunch them.
- Check liveness: `pgrep -af 'tree_(late|publish)\.sh$|mirror\.sh'`; GPU: `nvidia-smi`; disk: `df -h /`.

## 3. Your loop (run it every time a `NODE … EXIT` line appears in `$R/tree.log`)
```
tail -40 $R/tree.log                      # find NODE <name>-<slug> EXIT <rc> after <m> min
d=$R/experiments/<slug>
sed 's/\x1b\[[0-9;]*m//g' $d/run.log | tr '\r' '\n' | awk '/RERUN:/{f=1} f' | grep -vE 'it/s\]|examples/s' | tail -40
cat $d/autofixes.txt $d/prep.log 2>/dev/null | tail -5
python3 -c "import json;s=json.load(open('$d/spec.json'));print(s['target_value'],'|',s['tolerance'],'|',s['headline_artifact'])"
```
Then decide, in this order:
1. **Was it a system failure?** Burst of "EXIT in 0 s", ENOSPC, silent stall → fix the system (see §5), reset the done-list entry (edit `tree_late_done.txt`), do not ledger.
2. **Was it my invocation?** Traceback in `python <descriptive string>`, `No module named 'src'`, relative import, notebook JSON executed, `.sh` run as python → translate the entrypoint per `lessons-synth.md` §2.3, append a new line to `tree_late.txt` (`R<n>c|slug|timeout|command`), do not ledger.
3. **Was it environment?** Missing module / API removed in a major / GitHub-only package / placeholder login / Colab path / missing artifact fetch → apply §2.2–2.3 of `lessons-synth.md`, requeue, do not ledger. Cap: two requeues per slug; on the third failure ledger with the honest reason (`env`, `data`, `model-access`, `code-bug`, `unclear-entrypoint`).
4. **It ran.** Judge against `target_value` using the *named* measure; extract numbers from `executed.ipynb` outputs / saved HTML plotly data / result CSVs (`lessons-synth.md` §2.5). Then:
   - append `== VERDICT` to `$d/run.log` with `[MEASURED]` (numbers vs targets), `[INFERRED]`, `[UNRESOLVED]`, and a `Pipeline:` line;
   - `cd $d && python3 report.py --observed "<one line>" --reproduced true|false --reason none|env|data|model-access|vram|runtime|code-bug|api-key|unclear-entrypoint --seeds N --fix "…" --notes "…"` (notes: first sentence = any deviation from a pre-registered rule);
   - `human-oversight.md` section (3–6 lines, ELI5, end with **Needs you?**);
   - `handoff-N.md` (state delta, queue state, ledger count, next numbering) and `lessons-N.md` (only what this run taught; cite `lessons-synth` items it confirms);
   - `cd ~/alignment-literature-meta-analysis && git add replication && git commit -q -m "replication: <slug> <verdict>" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" && git push -q origin HEAD`.
5. If the slug is one of the three forks, update `README.human.md` / `README.llm.md` in `$d` and run `bash $R/publish.sh <slug> "<msg>"`.

## 4. Per-entry notes for what is still queued (read before judging each)
- **R18** `sunmoonron` OLMo-1B super-weight: chain `01_make_checkpoints → 03_train_patch → 07_compare_patch`; target perplexity 17.4 → 2884.3 (ablated) → 25.2 (patched), "~93 % recovery"; config runs on CPU by the author's choice — leave it.
- **R19** `ayoakin` MIVLDE: `PYTHONPATH` set to parent/grandparent/root; target "probes predict the time-point of max derivative but not its value; best layer 7, Spearman 0.75" — the spec's blockers say ~10 notebooks; judge only what `run_experiment.py` prints.
- **R20** `syvb` matryoshka-NLA: `setup_box.sh` downloads the author's own checkpoints with a personal token → likely `model-access`; do not work around.
- **R21** `patrickod32` seq2feature: notebook copy with `/content` rewritten; target 0.956 top-5 agreement / 0.90 AUC.
- **R23** `phusroyal`: `uv sync && uv run python -m src.predefined_manifold run --device cuda`; results in `.artifacts/predefined_manifold/runs/<id>/metrics.json` and `geometries/<geometry>/stages/<stage>/metrics.json`; target: linear-probe AUC 0.9996–0.9998 (ClassOT) → 0.57–0.67 (GFAL); causal delta 0.02–0.04 → 1.9–3.5.
- **R3b** `jordanmccann`: `replicate fetch-artifacts` then `run-fast`; target 0.976–0.990 toy, 0.85–0.99 Pythia-70m.
- **R4b** `dajale423`: editable clone of the author's `e2e_sae` fork on `PYTHONPATH`; target "SAE(x) KL comparable to cov-random-mixture baseline at layer 6".
- **R5b** `ckkissane`: full import pre-install (sae-lens, sae-dashboard, wandb…); may need W&B offline mode — `WANDB_MODE=disabled` is already exported.
- **R8b** `mshinkle`: `bash -e full_experiment.sh`; judge only if every sub-script ran (check the log, not the exit code).
- **R10b** `james-sullivan`: `neel-plotly` from GitHub, notebook via `run.sh`; target "no distinct additional developmental stages; single LLC decline".
- **R13b** `mamiglia`: `sae-lens<6`, 120-min box (the script iterates the vocab through hooks); target "33 of 64 eigenvalues negative".
- **R14b** `uchicago-xlab`: `python -m synth.run`; target PGD·optimal cosine 1.00 across k/m (vs paper's 0.92–0.97).
- **R25** `shivasrightfoot`: notebook copy with the Colab `files` stub; fine-tunes a model (needs `MODEL_NAME`, check gating); target ASR ~20 % → just under 90 %.
- **R27** `ibm`: `torch==2.3.1` from the cu121 index; target "< +0.001 s/token overhead" — a timing claim; report the measured overhead.
- **R28** `jim-maar` OthelloGPT: `transformers<5`; target 0.818 overall (up to 0.97).
- **R30** `artmtt`: DeepSeek-R1-distill-Qwen SAE features; target "feature 32456 top in 28/32 inferences" etc.
- **R32** `g-w1`: `vae.py` prints "Classification accuracy from encoding"; target 92.58 % (abs 5).
- **R29** `tenseisoham`: `datasets<4`, `transformers<5`; chain fine-tune notebook → logit-lens notebook; target 160.87 (base) vs 49 802.45 (fine-tuned).
- **R31** `peppinob-ol`: scores over the five committed dataset dirs; compare `output/research/repl_graph_subgraph_scores_summary.csv` (S_Repl / S_Comp averaged) with 0.5394 / 0.8257 and with the author's committed summary; no API needed.
- **R6b** `cywinski` script 5: the "~20 % accuracy recovery after mean-ablation" figure; add to the codi ledger notes (currently UNRESOLVED there).
- **R12b** `idostik`: notebook copy with `login(...)` stubbed; gated `meta-llama/Llama-3.2-1B` is accessible; target "only L0H3 significant when ablated one-by-one".
- **R17b** `thebuleganteng`: `sae-lens<4` for the `'11-res-jb'` id scheme; if it still fails, ledger `env` with the pin history.

## 5. System playbook (check these before reading any traceback as science)
- **Disk**: `df -h /`; < 20 GB → delete `experiments/*/.venv` of ledgered slugs, `~/.cache/huggingface/hub/models--*` of finished experiments, intermediates (`outputs/*/activations`). The late queue deletes venvs itself; the HF cache is the remaining growth.
- **Silent download**: `stat ~/.cache/huggingface/hub/models--*/blobs/*.incomplete`, `ss -tnpi | grep <pid>`; stalled → kill, delete `.incomplete`, `snapshot_download` over HTTP (`HF_HUB_DISABLE_XET=1` is exported everywhere).
- **GPU stuck**: `nvidia-smi --query-compute-apps=pid,process_name --format=csv`; only `python` rows count; a stray process from a killed node → `kill <pid>`.
- **Launcher trap**: never put a `pgrep`/`pkill` pattern inside a heredoc or command text you run from the harness; write scripts with the Write tool; anchor patterns (`'^bash \./tree_late\.sh'`).
- **Harness output lost (ENOSPC/ENOENT)**: disk is full; free space first, then rerun the command.

## 6. After the queue drains
1. `python3 $R/ledger.py`; write `handoff-N.md` "queue drained" with the final taxonomy; `lessons-N.md`; `human-oversight.md` closing section.
2. Optional GPU work, in this order of value: (a) experiment 01 evals D and E (~100 min each; re-download `Llama-3.2-3B`, `pythia-2.8b`; run from the repo root with `PYTHONPATH=$PWD`), (b) a third Gemma-270M seed for AntiPaSTO default vs random dims (2 × 35 min), (c) nothing else on AntiPaSTO without the author's 1B config.
3. Update `~/.claude/projects/-home-user-prompts/memory/replication-ledger-3090.md` with the final counts.

## 7. Things not to do
- Do not relaunch `tree_queue.sh` (pass 1 is complete) or re-run slugs already in `tree_late_done.txt` without removing them from that file.
- Do not ledger from `tree.log` lines timestamped 17:55 (disk-full artefacts).
- Do not create forks, PRs, or issues; do not commit files outside `replication/`; do not paste tokens into notebooks; do not "fix" author code beyond imports/paths on copies.
- Do not stop the GPU when pausing yourself — pause the agent, leave the queues.
