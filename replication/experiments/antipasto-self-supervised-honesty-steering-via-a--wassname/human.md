# AntiPaSTO on your 3090 — what happened, in plain terms

**One line:** the shipped code runs perfectly and, on the headline model, produces almost nothing. The paper claims an honesty‑steering score of 31.2 on Gemma‑3‑1B; the pinned repo's own preset gets **2.0** across three seeds, and plain prompting (13.5) beats it. The most likely reason is that the repository no longer contains the configuration the paper's 1B numbers came from — the same code reproduces the paper's *270M* result (41.7 vs 38.7) out of the box.

## What was tested

[AntiPaSTO](https://arxiv.org/abs/2601.07473) trains a small adapter inside Gemma‑3‑1B so that turning a dial to +1 makes the model more honest and −1 less honest, using only the words "honest" / "dishonest" as supervision. It's then scored on 1,360 moral dilemmas the model never saw ("Steer F1": how often the dial fixes a wrong answer, minus how often it breaks a right one or moves unrelated answers). The claim: **31.2 ± 5.3**, vs 13.0 for a carefully engineered prompt, 4.5 for a naive prompt, and 0.0 for the classic "add a vector" method (ActAdd).

## What we got

| | Steer F1 |
|---|---:|
| AntiPaSTO, seed 42 | 1.8 |
| AntiPaSTO, seed 43 | 0.4 |
| AntiPaSTO, seed 44 | 3.8 |
| **AntiPaSTO, mean of 3** | **2.0 ± 1.7** (claimed 31.2 ± 5.3) |
| Engineered prompt, same model | 17.9 (claimed 13.0) |
| Naive prompting, same model | 13.5 (claimed 4.5) |
| ActAdd, same model | 0.0 (claimed 0.0) |

So: the magnitude fails by a wide margin, the ordering flips (both prompting baselines win), and only the "ActAdd gets zero" part holds. The ledger entry is `claim_reproduced = false`, with no blocking reason — everything ran to completion.

## Why — the short version

1. **The repo drifted away from the paper.** The paper says: 800 training pairs, learning rate 1e‑3, batch 8, adapter rank 128, 64 modules. The pinned commit's `gemma1b-24gb` preset says: ~1,000 pairs, lr 5e‑4, batch 24, rank 64, 256 modules. I searched the entire git history — the paper's values were never the defaults anywhere, and the commits after the paper (“smaller init”, “fixes”, “asym_coh_ratio”) are exactly the ones that changed them. The README's results table was updated to the paper's numbers on 21 Aug, but the code that produced them wasn't.
2. **It's not bad luck with seeds.** I compared the three trained adapters directly: they agree with each other at cosine similarity 0.7–0.9 (random would be ~0.02). All three seeds learn the same thing, and that thing barely moves the needle.
3. **The dial works, just weakly.** In every seed the honesty score rises monotonically from −1 to 0 to +1 — the direction is right. But the shift is about the same size as the collateral movement on unrelated values, so the precision term of the score kills it. On axes with decent sample sizes (Honesty, Responsible, Traditional) the score is ≈0–4 in all seeds.
4. **The training loss looks fine.** The optimiser hits its own objective within two epochs. This is a case of "the loss went down and nothing happened downstream", not a crashed or diverged run.

**Follow‑up with the paper's own hyperparameters (done, 40 min):** this changes the story. The adapter now steers *hard* — it flips 24.6 % of target answers (paper: 29.9 %) and 53.5 % of unrelated ones (paper: 47.0 %), and the honesty score moves 2.9 → 3.2 → 5.1 across the dial. Scored without the "coherence" penalty it gets **20.9**, which is exactly the paper's own ablation‑table number for the full method (21.4 ± 5.5). With the penalty it gets **0.7**. Why: at +1 the model starts answering in **bold** (`**Yes**`) 79 % of the time, and the metric only recognises a plain ` Yes`/` No` as an answer, so it treats four‑fifths of the honest‑steered answers as "no answer" and multiplies the score by 0.035. The answers are perfectly coherent — it's a formatting tic, and the paper reports it didn't happen in their runs (Pmass 0.95). So: config drift is real and explains most of the gap between 2 and ~21; the remaining gap to 31.2 and the bold‑answer quirk are unexplained. Re‑scoring with the bold prefix counted as an answer (done, 8 min): **14.1**. The flip statistics now sit right on the paper's (29.7 % of target answers fixed vs the paper's 29.9 %), but about a third of the honest‑steered answers still open with something the scorer doesn't recognise, so the coherence factor still halves the score. Even excusing all of that, this adapter would land around 26, not 31.

## What went wrong along the way (and cost time)

- **Hugging Face download hang** — the new xet transport froze at 99.99 % of the 2 GB weights for 38 minutes with zero network traffic. Killed it, switched to plain HTTP (`HF_HUB_DISABLE_XET=1`), done in 6 minutes. This ate 50 of the 240 budget minutes; you may want that env var set globally.
- **The baseline scripts don't test the model the claim is about.** `--quick` evaluates Qwen3‑0.6B, and the ActAdd script loops over all ten models (including 12B) even in quick mode. I ran the scripts unmodified through a tiny wrapper that points them at Gemma‑1B.
- **24 GB isn't 80 GB.** The evaluation hard‑codes a batch of 32, which needs ~10 GB just for logits; I forced batch 8 in the wrapper. Batch size doesn't change the numbers.
- **A caching bug** in the ActAdd script made a full run silently return the 64‑dilemma quick result in "0 minutes". Deleted the mis‑named cache and re‑ran.
- `--quick` mode can't compute Steer F1 at all (the 64‑dilemma subset has none of the "arbitrary" control questions the metric needs), so the baselines had to be full runs — luckily only 2–3 minutes each.

None of these touch prompts, thresholds, data slices or metrics; all five are logged as environment fixes in the ledger.

## Where everything is

Folder: `~/alignment-literature-meta-analysis/replication/experiments/antipasto-self-supervised-honesty-steering-via-a--wassname/`

- `ledger.json` — the formal entry; `run.log` — timeline + `== VERDICT` at the bottom
- `seed42.log`, `seed43.log`, `seed44.log`, `baseline_*_full.log`, `followup1_paperconfig.log`
- `src/outputs/adapters/<timestamp>_g1b-…/` — trained adapters, per‑dilemma parquet results, example generations
- `followups/` — analysis scripts and outputs (cross‑seed similarity, per‑axis F1, metrics table)
- `LLM-report.md` — the dense version of this document with exact commands and paths
- `baselines_gemma1b.py` — the baseline wrapper

## What I'd do next (each under an hour of GPU)

1. **Paper‑config run** — done (see above): 0.7 as scored, 14.1 with bold answers counted, ≈26 if the model answered in plain text as the paper's did. Closer, but not 31.
2. **Gemma‑3‑270M** — done: **41.7** (paper 38.7). Same code, same defaults, and it *reproduces*. So the method and the scoring code are fine; the failure is specific to Gemma‑1B with the shipped preset — which makes "the 1B config is missing from the repo" the most likely story.
3. **Break it on purpose** — done, all four of the paper's headline ablations on the 270M model where the method reproduces, two seeds each (default: 41.7 / 29.3, mean 35.5):
   - fixing the rotation (paper −99 %): **9.7 on both seeds** — genuinely load‑bearing;
   - random dimension selection (paper −92 %): **43.6 then 2.7** — a coin flip: sometimes as good as the clever selection, sometimes a collapse where the training loss looks *great* but the learned direction steers unrelated answers instead of honesty;
   - no coherence barrier (paper −76 %): **47.1 / 35.7** — no harm at all;
   - no monotonicity constraint (paper −18 %): **41.5 / 35.8** — no harm at all.
   The two barrier terms never switch on at this scale (visible in the training logs), so removing them can't matter. Scorecard for the paper's "every ingredient is load‑bearing" table: one clear yes, one "sometimes", two noes.
4. **Qwen3‑0.6B** — done: **2.5** (paper 11.2). Clean run, no formatting quirk, just a weak steer. So with the shipped presets only the smallest Gemma reproduces; both other models fall far short.
5. **Engineered‑prompt baseline** — done: 17.9, above naive prompting (13.5) as the paper says, and above every AntiPaSTO number here.
6. **Richer personas** — done: **34.5** vs 41.7 with the plain "honest/dishonest" pair on 270M. The stronger wording steers harder but breaks more unrelated answers and makes the dishonest end less coherent, so the score goes down, not up (one seed).

**Bottom line after all follow‑ups (finished 13:02):** the code and scoring work — they reproduce the paper on the smallest model out of the box (270M: 41.7 vs 38.7) — but the headline Gemma‑1B claim doesn't hold with anything in the repo: 2.0 with the shipped preset, 0.7 with the paper's own hyperparameters as scored, 14.1 with a formatting artefact excused, ≈26 at best if the model answered in plain text. Of the paper's supporting claims, ActAdd = 0 held; Qwen3‑0.6B did not (2.5 vs 11.2); and the ablation table is mixed — the rotation is essential, random dimension selection is seed‑fragile rather than fatal, and the two "barrier" losses are inert. A control confirmed the bold‑tolerant re‑scoring doesn't inflate a normal adapter (3.50 → 3.45).

Things I deliberately didn't do: evaluate the author's published adapter (the HF repo is a 404), try the "full LoRA" v2 idea (needs loss changes the author says are unreleased), or contact the author (the protocol forbids it during a replication — but "which config produced the README table?" is the one question worth asking them afterwards).
