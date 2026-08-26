# AntiPaSTO replication — machine-oriented report

Audience: an LLM agent continuing this work. Everything here is either [MEASURED] on this machine,
[INFERRED] from measurements, or [UNRESOLVED]. Paths are absolute unless noted. No superlatives.

## 0. Identity

| field | value |
|---|---|
| post | LessWrong `nWiwv4GN8aYqpnZKE` (2026-01-13), paper arXiv 2601.07473 v5, "AntiPaSTO: Self-Supervised Honesty Steering via Anti-Parallel Representations" |
| repo / commit | `wassname/antipasto` @ `5e0f8517f360751220bf0348586952ff0e240907` (2026-08-21, "Correct the results table to the v5 paper numbers") |
| experiment folder | `/home/user/alignment-literature-meta-analysis/replication/experiments/antipasto-self-supervised-honesty-steering-via-a--wassname/` (= `$EXP` below) |
| prompt used | `/home/user/prompts/3090/02-antipasto-honesty-steering.md` |
| machine | RTX 3090 24 GB, driver 580.126.18, CUDA 13.0 host; Pop!_OS; 16 cores; 31 GB RAM |
| env | `$EXP/src/.venv`, Python 3.13.13, from `uv sync --all-groups` on `uv.lock`: torch 2.9.1+cu128, transformers 4.57.1, peft 0.17.2.dev0 @ 41091ec, accelerate 1.11.0, bitsandbytes ≥0.47 |
| HF account | `devmachine2`; Gemma licence accepted by the user during this session (was 403 at start) |
| ledger | `$EXP/ledger.json` (written by `report.py`); VERDICT block at the end of `$EXP/run.log` |

## 1. Claim and tolerance (verbatim from the prompt)

Claim: one adapter on `google/gemma-3-1b-it`, trained on ~800 self-supervised honesty contrast pairs, evaluated on
DailyDilemmas (1,360 dilemmas) gets Steer F1 = 31.2 ± 5.3 (3 seeds); Engineered prompt 13.0; Prompting 4.5; ActAdd 0.0.

- Magnitude reproduces iff 3-seed mean Steer F1 ∈ [25.9, 36.5].
- Ordering reproduces iff AntiPaSTO > Engineered prompt > Prompting > ActAdd.

## 2. Result

### 2.1 Headline [MEASURED]

| run | dir under `$EXP/src/outputs/adapters/` | Steer F1 | Net | Prec | Tgt Flip% | Wrong% | Arb Flip% | Nats lost | wallclock |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| seed 42 | `20260826_061947_g1b-antisym-r64` | 1.8 | 0.010 | 13.4% | 7.2% | 4.0% | 14.5% | 884 | 47 min |
| seed 43 | `20260826_070756_g1b-antisym-r64-seed43` | 0.4 | 0.002 | 5.3% | 4.8% | 2.9% | 10.7% | 524 | 47 min |
| seed 44 | `20260826_080947_g1b-antisym-r64-seed44` | 3.8 | 0.020 | 36.1% | 6.6% | 1.3% | 9.7% | 511 | 47 min |
| **mean ± sd** | | **2.0 ± 1.7** | | | | | | | |
| paper | | 31.2 ± 5.3 | | | 29.9 | 1.9 | 47.0 | | |

Command per seed (from `$EXP/src`, env `WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1`):
`uv run python nbs/train.py gemma1b-24gb [--seed 43|44]`. Logs: `$EXP/seed4{2,3,4}.log`.

Verdict: **magnitude NOT reproduced** (delta −29.2; 5.5 paper-SDs below; 17 of our SDs above our mean).

### 2.2 Baselines, same model, full 1,360 dilemmas [MEASURED]

| method | Steer F1 | notes |
|---|---:|---|
| prompting (`Pretend you're an honest/dishonest person.`) | 13.5 | repo script loads Gemma-1B in **nf4 4-bit** (its own rule for non-0.6B models); pmass 0.951 at coeff 0 vs 0.977 at ±1 → pmass_ratio ≈ 1.05 slightly inflates F1 (≈12.8 without) |
| repeng / ActAdd (mean-diff, layers −5..−12) | 0.0 | Value/Honesty logratio flat: 0.098 / 0.096 / 0.098 |
| engineered prompt (AxBench-style, hardcoded, no API) | **17.9** | follow-up 5 via the wrapper (3 min); paper 13.0; log `followups/fu5_engineered.log`, parquet `outputs/baselines/prompting_engineered/google_gemma-3-1b-it.parquet` |

Observed ordering: **Eng. prompt (17.9) > prompting (13.5) > AntiPaSTO (2.0 shipped; 0.7 paper-config) > ActAdd (0.0)** → **ordering NOT reproduced** (only the Eng. prompt > prompting > ActAdd sub-ordering holds). The ActAdd = 0 sub-claim reproduces.
Seed 44's own eval table (`$EXP/seed44.log`) contains all three methods because the baseline caches existed by then.

Baseline artefacts: `$EXP/src/outputs/baselines/prompting/google_gemma-3-1b-it.parquet`, `.../repeng/google_gemma-3-1b-it.parquet`
(`*_QUICK.parquet` are the 64-dilemma runs; their Steer F1 is NaN by construction, see §4.4). Logs `$EXP/baseline_{prompting,repeng}_full.log`.

### 2.3 Ledger JSON

See `$EXP/ledger.json`. Key fields: `installs=true, runs=true, claim_located=true, claim_reproduced=false, observed_value="2.0", delta=-29.2, blocking_reason="none", seeds_run=3, wallclock_minutes=229`, five `env_fixes` (§4). `peak_vram_gb=22.9` is the whole-GPU reading during the failed batch-32 baseline attempt; training itself peaked ≈14 GB.

## 3. Why it did not reproduce — evidence ranked

### 3.1 [INFERRED, strong] Config drift: the pinned commit does not ship the paper's configuration

| hyperparameter | paper v5 (Gemma-3-1B headline) | HEAD `gemma1b-24gb` preset (what the prompt pins) |
|---|---|---|
| training pairs | 800 | `max_samples=3000` → 1,033 pairs (all data) |
| lr | 1e-3 | 5e-4 |
| batch (eff.) | 8 (32) | 24 (32) |
| adapter rank `r` | 128 | 64 |
| `n_modules` | 64 | 256 (52 actually fit) |
| epochs / wd | 30 / 1e-5 | 30 / 1e-5 |
| loss layer / adapter depth | 90% / 10–90% | 0.9 / 0.1 (same) |

- `git log -S` over `antipasto/config.py`: **no commit ever had `r=128`, `n_modules=64` or `lr=1e-3` as defaults**; `max_samples=800` was the default only at the first commit `d9b131c` (2026-01-09) and was changed in `ddcd830` (2026-01-16). Later commits `c157500 "smaller init"`, `77c9634 "fixes"`, `3747447 "asym_coh_ratio"` (Feb 2026) changed defaults after the paper runs. The paper values appear nowhere in justfile/nbs/scripts history either.
- The paper's own ablation table lists "Full AntiPaSTO" as 21.4 ± 5.5 (not 31.2), i.e. the headline is the best of ≥2 "full" configurations.
- Consequence for the ledger: the reproduction target at the pinned commit is untestable as shipped; the entry records the shipped preset's number.

### 3.2 [MEASURED] Not seed noise

`$EXP/followups/cross_seed_similarity.py` (CPU): SVD bases identical across seeds (`data_seed=42`); rotation generators
`theta_v` agree at mean cos-sim 0.78 (42v43), 0.87 (42v44), 0.68 (43v44); unrelated 64×64 matrices give ≈0.02.
All three seeds learn essentially the same adapter, and all three score ≈2. Output: `$EXP/followups/cross_seed_42_43_44.txt`.

### 3.3 [MEASURED] Direction right, effect small, non-specific

- `Value/Honesty` logratio is monotone in coeff for every seed: 2.21→2.98→3.37 (42), 1.26→2.98→4.38 (43), 0.56→2.98→3.31 (44). `3_eval_summary.parquet` per run.
- pmass = 0.959 at every coeff (gate 0.95) → the pmass penalty is not what suppresses F1. Precision is: Arb Flip% (10–15%) ≥ Tgt Flip% (5–7%).
- Per-axis Steer F1 via the repo's `_compute_steering_f1_for_method` with the target column swapped
  (`$EXP/followups/per_axis_f1.py`, output `per_axis_f1_42_43_44.txt`):
  Honesty (n=378) 1.8/0.4/3.8; Responsible (`Value/Responsibility`, n=216) 0/0/0; Traditional (`WVS/Traditional`, n=72) 0/0/0;
  Ambitious n=8 and Friendly n=4 → values (26/29/8 and 52/0/0) are noise. Paper Table 4 claims 8.3–14.4 on Responsible/Traditional.
- Largest raw endpoint deltas on seed 42 are on unrelated values (goodwill +18, Financial Stability +17) vs Honesty +1.2 → steering is not honesty-specific at this config.

### 3.4 [MEASURED] Training dynamics

`1_train_history.parquet`: projection loss reaches −11 to −13 within 1–2 epochs and then drifts to −10…−12; `loss_coh` ≈ 0 and `loss_monotonic` = 0 throughout (barriers never bind); `cos_delta` ≈ −0.95 (antiparallel objective satisfied). Early stopping never triggered (its best-val bookkeeping starts after warm-up and kept improving by ≥1e-5); all 30 epochs ran. So the optimisation *succeeds at its own objective* while the downstream metric stays ≈0.

### 3.5 [MEASURED] Follow-up 1: the paper hyperparameters steer strongly, then a formatting shift zeroes the metric

`--lr 1e-3 --r 128 --n_modules 64 --max_samples 810 --bs 8` (eff. 32), seed 42, 30 epochs, 40 min, adapter `20260826_093640_paperconfig`:

| | paper (Table 1) | paper-config run here | shipped preset here (3-seed mean) |
|---|---:|---:|---:|
| Steer F1 | 31.2 | **0.7** | 2.0 |
| Steer F1 with pmass_ratio neutralised (metric function called with pmass₊=pmass₋=pmass_ref) | — | **20.9** | 2.0 |
| Tgt Flip% | 29.9 | 24.6 | 6.2 |
| Wrong% | 1.9 | 2.9 | 2.7 |
| Arb Flip% | 47.0 | 53.5 | 11.6 |
| Pmass | 0.95 | 0.922 / 0.961 / **0.180** (coeff −1 / 0 / +1) | 0.959 at all coeffs |
| Value/Honesty logratio −1/0/+1 | — | 2.92 / 3.21 / 5.14 | e.g. 0.56 / 2.98 / 3.31 |
| val loss_proj (end) | — | −11 (train −19) | −12 (train −16) |

- The flip statistics (Tgt, Wrong, Arb) land near the paper's, and 20.9 matches the paper's ablation-table "Full AntiPaSTO 21.4 ± 5.5". So the paper configuration *does* produce a materially stronger steer than the shipped preset; config drift is real.
- The penalty: `pmass_ratio = (min(pmass₊, pmass₋)/pmass_ref)² = (0.180/0.961)² = 0.035`. Cause: at coeff +1, **78.9 % of generations start with `**`** (markdown-bold `**Yes**` / `**No**`) vs 0 % at coeff 0 and −1 (`2_eval_labelled.parquet`, `output_text`). `antipasto/eval.py::get_choice_ids` matches only plain yes/no vocab tokens at the first generated position, so bold answers count as "no choice mass". The answers themselves are coherent (see `examples_after_training_…tsv`, +1 row).
- The paper reports Pmass 0.95 for AntiPaSTO, i.e. this bold-formatting side-effect did not occur (or was not counted) in the author's runs. `pmass_threshold` was lowered 0.5 → 0.05 in commit `f5a1ed8` (2026-01-18, "lower pmass thresh"), with the docstring left saying 0.5; under the old 0.5 threshold this run would have returned NaN rather than 0.7.
- Open: whether the bold prefix is a Gemma-3 chat-template/tokenizer-version artefact (transformers 4.57.1 here) or a genuine effect of the stronger adapter; and what F1 the paper-config adapter gets if pmass is measured after an optional `**` prefix (needs a re-eval with modified choice handling — a metric change, so a labelled follow-up, ≈5 min GPU via `load_adapter` + `evaluate_daily_dilemma`).
- Follow-up 7 (bold-tolerant re-score, see §5): **14.1**. Counting `**Yes`/`**No` as answers restores pmass at +1 from 0.18 to 0.70 and puts the flip profile on top of the paper's (Tgt 29.7 vs 29.9; Wrong 2.8 vs 1.9; Arb 54 vs 47). The residual pmass deficit is other non-Yes/No openings at +1; if pmass were the paper's 0.95 the same flips would give ≈26.
- Net: under the shipped metric code neither Gemma-1B configuration reproduces 31.2. The paper config reproduces the paper's *flip* statistics and its 21.4 ablation number; the headline 31.2 is not reached even with the formatting artefact excused (14.1 measured, ≈26 at the paper's pmass).

### 3.6 [MEASURED] Follow-ups 2–3: the same code and defaults reproduce the paper on Gemma-3-270M — and its key ablation does not

`gemma270m-80gb --bs 24 --seed 42` (everything else shipped defaults) → **Steer F1 41.7** vs paper Table 5 **38.7**. So the pipeline, metric and environment are capable of producing paper-level numbers; the failure is specific to Gemma-1B + shipped preset. This sharpens §3.1: what is missing for 1B is the 1B-specific configuration, not the method. It also matches the paper's own observation that 270M > 1B.

Cross-model tally with shipped presets, seed 42: Gemma-270M 41.7 (paper 38.7) ✓; Gemma-1B 2.0 (31.2) ✗; Qwen3-0.6B 2.5 (11.2) ✗. Only the smallest model reproduces.

With `--dim_select_method random` (everything else identical) the 270M run scores **43.6** — no degradation, versus the paper's −92 %. Either the WANDA selection matters only at the setting the paper ablated (base 21.4), or the ablation is seed-fragile. One seed each; a second seed of both would settle it (~35 min each).

### 3.7 [MEASURED] Follow-ups A1–A3 (2026-08-26 evening): the paper's ablation table on Gemma-3-270M, seed 42

Everything shipped-default (`gemma270m-80gb --bs 24 --seed 42`) except the one flag named. Logs `followups/fuA{1,2,3}_*.log`; adapters `outputs/adapters/20260826_2*_fuA*`.

| ablation | paper Table 2 (base 21.4) | here (base 41.7) | Tgt Flip% | Arb Flip% | honesty −1/0/+1 | verdict |
|---|---:|---:|---:|---:|---|---|
| ¬ V rotation (`--no_rot_v`, only `delta_s` learns) | 0.2 (−99 %) | **9.7 (−77 %)** | 19.3 | 31.6 | −2.99 / −2.33 / −0.95 | load-bearing ✓ (smaller than claimed) |
| ¬ coherence barrier (`--no_coh`) | 5.2 (−76 %) | **47.1 (+13 %)** | 64.6 | 51.8 | −0.87 / −2.33 / +1.38 | not load-bearing ✗ |
| ¬ monotonicity (`--no_mono`) | 17.5 (−18 %) | **41.5 (−0.5 %)** | 63.5 | 50.8 | −0.36 / −2.33 / +1.09 | no effect ✗ |
| WANDA dims → random (`--dim_select_method random`, run 3) | 1.8 (−92 %) | **43.6 (+5 %)** | — | — | −2.93 / −2.33 / +0.66 | not load-bearing ✗ |

Why the barriers don't matter here [MEASURED]: in every 270M and 1B training history `loss_coh ≈ 0` and `mono_frac_violated = 0` — the coherence and monotonicity hinges never activate with the shipped thresholds (`coh_thresh 0.9`, `mono_margin 0.5`), so removing them changes nothing (`train_adapter.py:137` sets `effective_coh_weight = 0` when `coh=False`; with `coh=True` the logged term is ≈0 anyway). pmass with `--no_coh` is 0.885 / 0.928 / 0.876 vs 0.88 / 0.93 / 0.84 with it. The paper's −76 % / −18 % must come from a regime where the barriers bind (larger model, other thresholds) or from seed variance. Side effect: early stopping is only enabled when `coh and mono` are both true (`train_adapter.py:1969`), so ablation runs always do 30 epochs — the defaults did too in practice.

Single-seed reading superseded by the two-seed table in §3.8.

### 3.8 [MEASURED] Follow-ups A4–A8: second seed (43) for the 270M default and all four ablations

| config | seed 42 | seed 43 | mean | paper Table 2 direction | reading |
|---|---:|---:|---:|---|---|
| default | 41.7 | 29.3 | **35.5** | base (21.4 in the paper's ablation setting; 38.7 in Table 5) | reproduces Table 5 within the paper's SD 5–7 |
| WANDA → random dims | 43.6 | **2.7** | 23.2 | −92 % | **seed-fragile**: matches WANDA on one seed, collapses on the other (−35 % mean). Collapsed run: objective satisfied *better* (val loss_proj −14, cos_delta −0.99, pmass 0.88–0.93) but Tgt Flip 6 % vs Arb Flip 48 % — the antiparallel direction landed in a subspace unrelated to honesty. Same signature as the 1B shipped preset. |
| fixed V (`--no_rot_v`) | 9.69 | 9.69 | 9.7 | −99 % | **load-bearing, robust** (−73 %); result is seed-invariant because only `delta_s` learns on a deterministic basis |
| no coherence barrier | 47.1 | 35.7 | 41.4 | −76 % | **not load-bearing** (+17 %, both seeds ≥ default) |
| no monotonicity | 41.5 | 35.8 | 38.6 | −18 % | **no effect** (+9 %, both seeds ≥ default) |

All ten runs trained the full 30 epochs (early stopping never triggered where enabled; it is disabled when `coh` or `mono` is off — `train_adapter.py:1969`), so the barrier-off runs are not favoured by extra training. Logs `followups/fuA*.log`, `followups/queue.log`.

Net for the paper's mechanistic claims, on the one model where the headline reproduces: the SVD/rotation structure is load-bearing (fixed V breaks it, robustly); the dimension selection matters on average but is seed-fragile rather than the clean −92 %; the two barrier terms never activate with the shipped thresholds and can be removed without loss. The paper's ablation table is 1½ for 4 here.

## 4. Environment fixes (all recorded in `ledger.json.env_fixes`) and gotchas

1. **xet download hang**: `hf_hub` via xet stalled at 1,999,811,208 / ~2.0 GB for 38 min with zero socket traffic (log `~/.cache/huggingface/xet/logs/xet_*_156015.log`). Fix: kill, delete `.incomplete`, `HF_HUB_DISABLE_XET=1`, `snapshot_download` over HTTP (340 s). Cost 50 min of budget.
2. **Baseline scripts evaluate the wrong model**: `--quick` uses `EVAL_BASELINE_MODELS[:1]` = `Qwen/Qwen3-0.6B`; `eval_baseline_repeng.py` loops `EVAL_BASELINE_MODELS` (all 10, incl. 12B/7B) even in quick mode. Fix: `$EXP/baselines_gemma1b.py` imports the scripts unmodified and sets the module-level list to `["google/gemma-3-1b-it"]`. Usage from `$EXP/src`: `../src/.venv/bin/python ../baselines_gemma1b.py prompting|repeng|prompting_engineered [quick|full]`.
3. **OOM in `calc_nll`**: scripts floor eval batch at `max(32, bs)`; fp32 logits 32×~320×262,144 ≈ 10 GB. Fix: wrapper monkeypatches `evaluate_daily_dilemma` to `batch_size=8`. (`PYTORCH_ALLOC_CONF=expandable_segments:True` alone fixed only the quick repeng run.)
4. **Repeng cache-name bug**: `cache_path` is built before `_QUICK` is appended, so a quick run writes the full-run filename and the full run silently reuses it ("EXIT 0 after 0 min"). Fix: delete `outputs/baselines/repeng/google_gemma-3-1b-it.parquet` before a full run if a quick run preceded it. Prompting script does not have this bug.
5. **`--quick` cannot produce Steer F1**: the 64-dilemma subset selected by `select_dilemma_by_values` contains no `Math/*` or `Preference/*` (the "arbitrary" cluster) → `arb_w` empty → NaN. Use full runs for any F1 (≈3 min prompting, ≈2 min repeng on this card).
6. Once baseline parquet caches exist, `nbs/train.py`'s eval merges them into its table (see seed 44's log) — convenient, but means seeds 42/43 tables show AntiPaSTO only.
7. `wassname/antipasto-gemma-3-1b-honesty` (README "pretrained adapter") is a 404 on HF → cannot evaluate the author's own adapter.
8. `PYTORCH_CUDA_ALLOC_CONF` is deprecated in torch 2.9 → use `PYTORCH_ALLOC_CONF`.
9. Python stdout from `uv run python … > log` is block-buffered; use `PYTHONUNBUFFERED=1` if tailing. Loguru output goes to stderr with `\r` progress bars: `tr '\r' '\n' | sed 's/\x1b\[[0-9;]*m//g'` to grep.
10. **Scheduler off-by-one** (`train_adapter.py:1963`): choose `bs`/`effective_bs`/`max_samples` so that `len(train_loader) % (effective_bs//bs) == 0`, or the last epoch crashes before the adapter is saved. Dry-run the dataset builder (`create_train_dataset`) on CPU to find a `max_samples` that works; for bs 8 / eff 32 on Gemma-1B, 780, 810, 830 work and 800 does not.
11. **Harness gotcha**: any background launcher whose command text contains a string like `nbs/train.py` will match `pgrep -f nbs/train.py`; anchor wait patterns to the real executable (see `followups/queue.sh`).
12. Timing on the 3090: 85 s/epoch (bs 24), 30 epochs + 1,360×3 eval ≈ 47 min per seed; rnd smoke test 3.5 min.

## 5. Follow-ups

All follow-ups finished 2026-08-26 13:02. All GPU items ran one-at-a-time, each < 1 h. Full timeline in `followups/queue.log`. Everything here is outside the protocol's 240-min budget and is **not** part of the ledger entry.

| # | idea | why (source) | status | result |
|---|---|---|---|---|
| 1 | Train with the paper-v5 hyperparameters: `nbs/train.py gemma1b-24gb --lr 1e-3 --r 128 --n_modules 64 --max_samples 810 --bs 8 --seed 42 --experiment_name paperconfig` | §3.1; the single most informative test of "config drift vs. method" | DONE (40 min; adapter `$EXP/src/outputs/adapters/20260826_093640_paperconfig`; log `followups/fu1_paperconfig_retry.log`). First attempt with `--max_samples 800` crashed at epoch 29/30 on the scheduler off-by-one (§4 item 10). | **Steer F1 = 0.7 with the pmass penalty, 20.9 without it** — see §3.5 |
| 2 | Cross-model: `gemma270m-80gb --bs 24 --seed 42` (shipped defaults otherwise: lr 5e-4, r 64, n_modules 256→36 fit, 1,033 pairs) | paper Table 5 says the *smaller* model scores higher (38.7 vs 31.2) | DONE (35 min; adapter `20260826_102103_fu2-270m`; log `followups/fu2_gemma270m.log`) | **Steer F1 = 41.7** (paper 38.7) → **reproduces**. Tgt Flip 61.4%, Wrong 8.2%, Arb 49.5%, pmass 0.88/0.93/0.84, 0% bold answers. Honesty logratio −1.13 / −2.33 / +1.03 at −1/0/+1 — the +1 side works, the −1 side moves slightly *toward* honesty (directional F1 ignores this). |
| 3 | Ablation on 270M: `gemma270m-80gb --bs 24 --seed 42 --dim_select_method random` | paper Table 2: WANDA→random = −92% (21.4→1.8); README v2 "reduce init variance" | DONE (33 min; adapter `20260826_105614_fu3-270m-random`; log `followups/fu3_270m_random.log`; verified the selected SVD dims differ from run 2 via `0_precomputed_indices.pt`) | **Steer F1 = 43.6** vs 41.7 with WANDA → the ablation claim does **not** reproduce on 270M (1 seed). Honesty logratio −2.93 / −2.33 / +0.66 (monotone, unlike run 2); pmass 0.93/0.93/0.94. Caveat: the paper's ablation base is 21.4, i.e. a different (probably 1B) setting. |
| 4 | Cross-model: `q06b-24gb --seed 42` (Qwen3-0.6B, shipped preset) | paper Table 5: 11.2 | DONE (41 min; adapter `20260826_112926_fu4-q06b`; log `followups/fu4_qwen06b.log`) | **Steer F1 = 2.5** (paper 11.2) → does not reproduce. pmass 0.998 at all coeffs, no bold artefact; honesty 0.11 / 1.33 / 1.54 (monotone, small); Tgt 6.6%, Wrong 3.3%, Arb 8.5%. |
| 5 | Engineered-prompt baseline, full: `../baselines_gemma1b.py prompting_engineered full` | completes the ordering claim (paper 13.0) | DONE (3 min) | **17.9** |
| 7 | Bold-tolerant re-score of the paper-config adapter (`followups/rescore_bold.py`: P(Yes)=P(Yes)+P(`**`)·P(Yes\|`**`), one extra forward pass; everything else the repo's) | §3.5 | DONE (8 min; log `followups/fu7_rescore_paperconfig.log`; parquet `…paperconfig/2_eval_labelled_{standard,bold_tolerant}.parquet`) | standard re-eval **0.74** (= training-time 0.736 ✓); bold-tolerant **14.1**. pmass at +1: 0.179 → 0.697; Tgt 29.7% (paper 29.9), Wrong 2.8% (1.9), Arb 54.4% (47.0), Net 0.25, Prec 27.6% → F1 ≈ 26 before the pmass term, × (0.697/0.951)² = 0.54 → 14.1. A further ~30% of +1 answers begin with something other than `**`/Yes/No (see §3.5). |
| 7c | Control: same re-score on shipped seed-44 adapter (no bold artefact) | validates the mixture doesn't inflate scores | DONE (8 min; log `followups/fu7c_rescore_seed44.log`) | standard **3.50**, bold-tolerant **3.45** → unchanged, as expected. (3.50 vs the training-time 3.81 = eval sensitivity to batch size 8 vs 32 / padding — ±0.3 on this metric.) |
| 6 | Richer personas on 270M: `gemma270m-80gb --bs 24 --seed 42 --PERSONAS.0 "a scrupulously honest, transparent and truthful" --PERSONAS.1 "a manipulative, deceptive and dishonest"` | README v2 "more expressive personas" | DONE (34 min; adapter `20260826_121118_fu6-270m-personas`; log `followups/fu6_270m_personas.log`) | **Steer F1 = 34.5** vs 41.7 with the plain pair. Steers harder (Tgt 78.0%, Net 0.65) but less cleanly (Wrong 10.3%, Arb 59.7%); pmass 0.68 / 0.93 / 0.95 → pmass_ratio ≈ 0.54 is what costs it. Honesty −2.42 / −2.33 / +1.50. 1 seed. |
| A1–A3 | 270M ablations `--no_rot_v`, `--no_coh`, `--no_mono` (seed 42) | paper Table 2 | DONE (30–32 min each) | 9.7 / 47.1 / 41.5 vs 41.7 — see §3.7 |
| A4–A8 | 270M seed 43: default, random dims, and the three ablations | make §3.6–3.7 interpretable against the paper's SD 5–7 | DONE (30–33 min each; finished 2026-08-27 02:07) | default 29.3, random 2.7, fixed-V 9.69, no-coh 35.7, no-mono 35.8 — see §3.8 |
| D | Cross-seed adapter similarity | README v2 "reduce init variance"; paper Limitations SD 5–7 | DONE | cos-sim 0.68–0.88; see §3.2 |
| E | Per-value-axis Steer F1 from own parquet | README "wins 5 of 6 value axes"; v2 "better metric" | DONE | see §3.3 |

Rejected: evaluating the author's published adapter (404); full-LoRA v2 (needs loss changes the author says are unreleased); ≥4B models (over the hour on a 3090); anything that edits prompts/thresholds/metrics inside the ledger run.

## 6. How to continue

- Re-run the whole protocol: follow `$EXP/PROMPT.md` (copy of the 3090/02 prompt) with the fixes in §4 applied up front (`HF_HUB_DISABLE_XET=1`, use the wrapper for baselines, batch 8).
- Cheap re-analysis without GPU: every adapter dir has `2_eval_labelled.parquet` (per-dilemma, per-coeff, all `logscore_*` columns), `3_eval_summary.parquet`, `3_eval_effect_main.parquet`, `1_train_history.parquet`, `adapter_model.safetensors`, `0_svd_bases.safetensors`, `training_config.json`.
- Scripts: `$EXP/followups/cross_seed_similarity.py <dirA> <dirB> …`; `$EXP/followups/per_axis_f1.py <dir> …` (run from `$EXP/src`, absolute dirs); `$EXP/baselines_gemma1b.py`.
- Open questions in priority order: (0) a third 270M seed for default vs random dims would settle whether random-dims averages −35 % or worse (35 min each); (a) why does the paper-config 1B adapter emit `**`/blank openings at +1 on this stack (transformers 4.57.1, torch 2.9.1) when the paper reports pmass 0.95 — tokenizer/chat-template version, or the adapter? (b) second seeds for 270M default vs random dims (35 min each) to confirm the non-reproducing ablation; (c) is the paper's Table 2 "Full AntiPaSTO 21.4" the shipped config on 1B? (d) which config produced the README's 31.2 — the one question worth asking the author afterwards (rule 8 forbade contact during the replication).
- Aggregate ledger: `cd ~/alignment-literature-meta-analysis/replication && python3 ledger.py` after all three 3090 experiments.
