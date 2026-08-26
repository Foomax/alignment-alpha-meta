# Hand-off: what to do with 8 hours of RTX 3090 time (written 2026-08-26 20:00, for myself)

State on entry: experiment 02 (AntiPaSTO) is ledgered + 8 follow-ups done (see
`experiments/antipasto-…--wassname/LLM-report.md`). Experiments 01 and 03 have not been run.
GPU is idle. 8 h window ≈ 20:00 → 04:00.

## 1. Candidates (everything I considered)

| # | candidate | GPU cost | what it would settle | blockers |
|---|---|---:|---|---|
| C1 | **Experiment 03** — noise-injection sandbagging (Qwen2.5-1.5B-Instruct, 100 generation passes) | 2–4 h (budget 240 min) | third ledger row; a safety-method replication with an author-flagged fragility (sandbag prompt may stop sandbagging) | none — model cached, ungated |
| C2 | **Experiment 01** — cross-model CKA geometry | 3–6 h | first ledger row (negative claim) | **Llama-3.2-1B/3B are 403** on `devmachine2`; 4/5 evals incl. the control need them. Only eval B runnable → cannot test the claim. `model-access` |
| C3 | AntiPaSTO 270M **ablation suite**: `--no_coh`, `--no_mono`, `--no_rot_v` | 3 × ~35 min | paper Table 2 says −76 %, −18 %, −99 %; the random-dims ablation (−92 % claimed) already failed to reproduce on 270M. Are *any* of the claimed load-bearing components load-bearing on the one model that reproduces? | none |
| C4 | AntiPaSTO 270M **second seed** for default and random dims | 2 × ~35 min | is 41.7 vs 43.6 (random ≥ WANDA) a seed fluke? Paper SD is 5–7 | none |
| C5 | AntiPaSTO 1B **one-factor sweep** from shipped preset toward paper config (lr, r, n_modules, pairs, bs one at a time) | 5 × ~47 min ≈ 4 h | which hyperparameter moves 1B from 2 to ~21 | none, but see cut |
| C6 | AntiPaSTO 1B paper-config **second seed** | 47 min | is the `**` bold-answer artefact seed-specific? | none |
| C7 | Bisect the bold artefact across transformers versions (4.51 … 4.57) | env churn + ~8 min eval each | whether the paper's pmass 0.95 vs our 0.18 is a library-version effect | violates "one venv per experiment" spirit; low confidence it converges in 8 h |
| C8 | Qwen3-0.6B second seed / personas seeds | 35–41 min each | tighten single-seed follow-ups | none |
| C9 | 270M richer personas + `--no_coh` combos, coefficient sweeps ±0.5/±2 | ~35 min each | curiosity | none |

## 2. Critical evaluation

**What the project actually needs.** The ledger (readme R5) wants rows with a failure taxonomy. One row exists. C1 gives a second row for ~3.5 h with zero blockers. C2 would give a third but is blocked on a licence only the user can click — and even then it is 3–6 h, so it cannot also fit tonight. C2 is therefore *not a candidate for this window*; the correct action is to tell the user to accept the Llama-3.2 licence so 01 can run next.

**Where AntiPaSTO follow-ups still have information value.** The 1B story is characterised: shipped preset ≈2, paper config ≈21 before / 14 after a formatting artefact, 26 at best. More 1B runs (C5, C6) refine a number nobody is going to act on differently whether it is 14 or 26 — the headline 31.2 is out of reach either way. C5 in particular costs half the window for a hyperparameter attribution the author could answer in one email. **Cut C5, C6.** C7 is a rabbit hole with venv churn against the protocol's spirit. **Cut C7.** C8/C9 are seeds on results that already point the same way (Qwen 2.5 vs 11.2 is not going to flip with one seed). **Cut.**

The one AntiPaSTO question with a *new* answer is C3: the paper's ablation table is its mechanistic argument ("all components are load-bearing"); the first ablation I tried on the model that reproduces went the *opposite* way. Testing the other three claimed components on 270M is cheap (1.75 h), single-flag, and if two or three more fail to degrade the score, that is a stronger statement about the paper than anything else on the list. C4 (second seed, 1.2 h) is needed to make C3 interpretable: the paper's own SD is 5–7, so a −18 % effect (mono) is undetectable with one seed, but −76 % and −99 % are not. Keep C4 at one extra seed for default and random; do not add seeds to the other ablations unless an effect is ambiguous.

**Risks.** C1: the author's notes say the sandbag prompt once stopped working; the protocol handles that (stop, `unclear-entrypoint`) and it would *free* GPU time, not cost it. Runtime: the author saw ~2 min/pass; 100 passes ≈ 3.5 h — right at the 240-min budget; the prompt pre-authorises stopping after seeds 0–4. C3/C4: one job at a time on the card, so they must queue behind C1, which delays their results to ~03:00; acceptable, fully automatic. Two things must not happen: the queue starting before 03 has the card (it will use an nvidia-smi compute-process check *and* a sentinel file), and any `pgrep` pattern appearing in a launcher command line (see memory `background-pgrep-launcher-trap`).

**Sequencing.** 03 first (it needs attention during setup and its result may end early); ablation queue armed to start when 03's process is gone. Order inside the queue by information value: `--no_rot_v` (−99 % claimed), `--no_coh` (−76 %), `--no_mono` (−18 %), then seed-43 default, seed-43 random.

## 3. Decision and time budget

| slot | job | est. | cumulative |
|---|---|---:|---:|
| 20:00 | 03 setup (clone, venv, the two prescribed script edits, smoke of first two passes) | 15 min | 0:15 |
| 20:15 | 03 run: 10 seeds × 6 noise levels × 2 prompts (noise 0 added) ≈ 102 passes | ≤ 240 min | 4:15 |
| ~23:00 | 03 analysis, ledger, VERDICT (CPU) — overlaps with queue below | 20 min | — |
| ~00:15 | 270M `--no_rot_v` | 35 min | 4:50 |
| | 270M `--no_coh` | 35 min | 5:25 |
| | 270M `--no_mono` | 35 min | 6:00 |
| | 270M default, seed 43 | 35 min | 6:35 |
| | 270M random dims, seed 43 | 35 min | 7:10 |
| ~03:10 | patch AntiPaSTO reports; update this file | — | 7:20 |

Slack ≈ 40 min. If 03 overruns its budget, it stops per protocol at seeds 0–4 and the queue starts earlier. If 03 ends early on the fragility path, everything shifts earlier and there is room for one more 270M seed of `--no_rot_v` or `--no_coh` (whichever is ambiguous).

Deferred with reasons: 01 (licence), C5/C6/C7/C8/C9 (low marginal information per GPU-hour, see §2).

## 4. Results (filled in as they land)

- 03: **DONE 21:49 (103 min, exit 0). Ledger `claim_reproduced=true`** — (b) 9/10 seeds gain > 5 pp (author 6/10), sandbag mean 46 → 60 % at noise 0.001; strict (a) fails by a +1.0 pp within-SE wobble at noise 0.0005 (disclosed in ledger notes), passes within 1 SE. 3 env fixes. Mechanism: bare-guess share 47 % → 11 % with noise. Note: `report-03.md`.
- Seed-43 ablations: `--no_rot_v` **9.69** (seed 42: 9.69 — deterministic) · `--no_coh`: **35.7** (seed-43 default 29.3; 2-seed means 41.4 vs 35.5) · `--no_mono`: **35.8** (seed-43 default 29.3; 2-seed means 38.6 vs 35.5)
- Slack used: second seeds of the three ablations queued (`queue_ablations2.sh`, A6–A8, ~1.75 h) after A1–A5; finished **02:07** — 6 h 08 min of the 8-h window used; GPU idle from 02:07.
- C3 `--no_rot_v`: **9.7** (default 41.7 → −77 %; paper −99 %) · `--no_coh`: **47.1** (default 41.7 → no drop; paper −76 %) · `--no_mono`: **41.5** (default 41.7 → no change; paper −18 %)
- C4 seed 43 default: **29.3** (seed 42: 41.7; 2-seed mean 35.5 vs paper 38.7 ± 5–7) · seed 43 random: **2.7** (seed 42: 43.6) → random dims is seed-fragile; 2-seed mean 23.2 vs default 35.5

## 5. Close-out (2026-08-27 02:10)

Everything in §3 ran; nothing was cut mid-way. Outcomes: 03 reproduced (ledgered); the 270M ablation suite gives the paper's Table 2 a mixed grade (rotation essential; random dims seed-fragile; coherence and monotonicity barriers inert). Both AntiPaSTO reports (`experiments/antipasto-…/{LLM-report.md,human.md}`) carry the full tables in §3.7–3.8 / item 3.

What I would do with the *next* GPU window, in order: (1) experiment 01 — the moment the Llama-3.2 licence is accepted (3–6 h); (2) a third 270M seed for default vs random dims (70 min) to pin the random-dims mean; (3) nothing else on AntiPaSTO without a reply from the author about the 1B configuration.

## 6. Should experiment 01 run at all? (2026-08-27 02:30, licences now accepted)

**Facts gathered (CPU only).** Repo `jaehoonlee0829/cross-model-alignment-geometry` @ `bfacecf` clones fine; one YAML per eval; every README number maps to a script; reference outputs committed (3.2 MB) for A/B/D/E and the control C. Extraction is *last-token* activations of 10k Pile prompts at 128 tokens, 9 layers, stored fp32 → ~80 MB per model, minutes of GPU per model on a 3090. CKA is on a 5,000-row subsample of 2048-dim vectors; the 500-permutation tests are CPU. The dominant cost is not GPU: six models ≈ 22 GB of downloads (Llama 1B/3B, pythia 1.4b/2.8b, gemma-2-2b; Qwen cached) at the ~6 MB/s this machine got over plain HTTP ≈ 1 h. Realistic total ≈ 2–2.5 h wall-clock, of which ≈ 30–45 min is GPU — not the 3–6 h in the prompt. Risk: `requirements.txt` pulls `sae-lens` and `nnsight`, unused by these scripts; install without them if they fail to resolve (prompt pre-authorises).

**Case for moving on.** The ledger measures a *rate and a failure taxonomy*; rows per GPU-hour is the currency. `queue.md` lists 34 minute-class experiments and ranks 01 at #33 by run order — in the wall-clock 01 takes, 5–10 minute-class rows could be added. And 01's prior of reproducing is high (deterministic pipeline, committed outputs, well-specified negative number), so the expected information from the *scientific* outcome is low.

**Case for running it.** (1) The three 3090 prompts were selected together "for stake and diversity" — positive (02), replication (03), negative (01); it is the only negative-claim row, and a taxonomy without negative claims is lopsided. (2) It is the #1 pareto pick (0.81) and the corpus's most contested phenomenon (22-vs-5). (3) It is now unblocked and cheap: ≈ 40 min of GPU. (4) The informative axis for the ledger is *pipeline/environment* survival (dependency rot, gated models, headline spread over five scripts), and that is exactly what a replication rate is supposed to capture — a "reproduces" row from a well-engineered repo is a real data point, not a wasted one. (5) The control eval C gives an internal validity check the other two experiments lacked.

**Verdict: run it — but as a background batch, not a session.** Start the 22 GB of downloads now (no GPU), run C → A → B → D → E with the 240-min box, skip the probe-transfer scripts, ledger it, and treat the whole thing as ~45 min of GPU. Then move to the minute-class queue in batches of 5–10, which is the right next phase regardless of 01. The only scenario in which skipping 01 is correct is if the GPU is needed for something else within the next 3 hours; there is no scientific reason to skip it.
