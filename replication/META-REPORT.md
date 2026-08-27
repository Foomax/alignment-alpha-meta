# Replicating alignment-forum empirical work on one RTX 3090 — meta-report

**Status: FINAL** (N=34; queue drained 2026-08-28 05:55). Numbers regenerate via `python3 make_report_table.py`; rows via the generator in the same file. Every claim below is auditable in the named `experiments/<slug>/{ledger.json,run.log}`.

## Executive summary

We attempted to reproduce the headline numerical claim of **34** alignment-forum / interpretability posts on a single RTX 3090 (24 GB, 31 GB RAM), under a fixed protocol: pin the author's commit, one virtualenv per experiment, **environment-only fixes** (never touch prompts/thresholds/data-slices/metrics/seed-counts), no closed-model APIs, a time-box, and a `[MEASURED]/[INFERRED]/[UNRESOLVED]` verdict per row.

**Headline finding.** *When the code runs at all, the work reproduces at a high rate to the stated precision. The binding constraint on reproducibility is engineering rot — not scientific fragility.*

Two numbers carry it:
- **Of the 19 experiments that ran far enough to test the claim, 17 (89%) reproduced at least partially** (14 full + 3 partial). Exactly **one** was a genuine scientific non-reproduction (AntiPaSTO — and it reproduces at smaller scale; see below), and one more was a hosted-API artefact, not a local test.
- **15 of 34 attempts (44%) never reached a measurement at all — and every one of those 15 failed on engineering or hardware**, never on the science: a "entrypoint" that was prose, a library asset renamed across versions, a checkpoint the repo didn't commit, a Colab assumption, a `TrainingArguments` kwarg removed mid-version, a multi-hour run mis-tagged "minutes," a 48 GB-card design, a W&B-gated SAE, an OOM.

So the reproducibility of this literature, on this evidence, is **gated by packaging, not by science**.

## Method
- **Corpus:** the three protocol experiments in `~/prompts/3090/` (a negative, a positive, a replication) + the minute-class rows of `queue.md` (from 87 inspected candidates).
- **Protocol / audit trail:** as above; each environment fix is a `--fix` line in `ledger.json`; each `run.log` ends with a `== VERDICT` block. Automation: a sequential, disk-bounded GPU queue (`tree_late.sh`+`tree_prep.sh`+`tree_imports.py`+`tree_autofix.py`+`nb_colab_stub.py`); judgement by hand per row.
- **Quality tiers:** **exact** = regenerated the core computation from source and matched; **recompute** = re-ran a script over the author's *committed* artefacts without regenerating them; **partial** = some components match; **not** = located and genuinely off; **n/a** = never located.

## Results (N=34)

| metric | value |
|---|---|
| attempted | 34 |
| installed | 33 |
| ran | 20 |
| **located (reached a measurement)** | **19** |
| **reproduced** | **14 (74% of located, 41% of attempted)** |
| reproduced — tier mix | 11 exact, 3 recompute |
| located but not reproduced | 5 — 3 partial, 1 not (config-drift), 1 hosted-API |
| never located | 15 — env 6, runtime 3, unclear-entrypoint 2, vram 2, data 1, model-access 1 |
| **located that reproduced ≥ partially** | **17 / 19 (89%)** |

### All 34 rows (✅ reproduced · ❌ located-not-reproduced · — never-located; tier; failure reason in parens)

| | tier | repo | headline result / reason |
|---|---|---|---|
| ✅ | exact | ai-forever/data_leakage_detect | target-free MIA AUC 0.9887 (=~0.986) on VL-MIA-Flickr-2k |
| ✅ | exact | ameya-bit/quotesbyniche | B5H0 copying 0.615 vs next 0.347; OV bracket +0.556 / −0.105 |
| ✅ | exact | coolvision/interp | neuron–vocab alignment long-tailed, late-layer (3–13.5% vs ~0%) |
| ✅ | exact | cywinski/codi | latent 3/5 hold intermediate values (−0.30/−0.22 vs ≈0) |
| ✅ | exact | fractalmachinist/ioi | IO/S logit-diff drop 0.231 (=0.23), all 8 stats match |
| ✅ | exact | jaehoonlee0829/cross-model-alignment-geometry | CKA within 0.914 vs cross 0.208/0.222 (evals C/A/B = README) |
| ✅ | exact | lovkush-a/arena-sandbagging-mi | noise recovers sandbagging 9/10 seeds (author 6/10) |
| ✅ | exact | mild-rgb/qwen-echo | head 2 top-3 by ablation 44/44; ~0.9 BOS attention (modal) |
| ✅ | exact | mshinkle/activation_plateau_mechanisms | freezing MLP eliminates plateaus; attention preserves them |
| ✅ | exact | noanabeshima/matryoshka-saes | toy: vanilla 9/20 absorbed, Matryoshka 0/20 |
| ✅ | exact | phusroyal/phu-bluedot | probe AUC 0.9997→0.57 (GFAL), causal delta 0.02→3.5 |
| ✅ | recompute | patrickod32/seq2feature | committed 5 MB probe AUC 0.90 (=0.90), 88% vs SAE 89% |
| ✅ | recompute | peppinob-ol/attribution-graph-probing | fact-variant Repl 0.5425 / Comp 0.8412 (=0.5394/0.8257) |
| ✅ | recompute | vaiyr/probe-necessity | 17 recovered + 5 alarmed (auto 22/27) |
| ❌ | partial | idostik/llm-typos | L0H3 merging-head mechanism ✓; exclusivity sweep blocked (t-lens arity) |
| ❌ | partial | jordanmccann/polymorphism-is-rotation | toy + Haar exact (verify 6/6); Pythia post-rot EV 0.2–0.5 vs 0.85–0.99 |
| ❌ | partial | shivasrightfoot/soo-jailbreak | fusion adapter trains & bypasses refusals ✓; ASR% needs a separate eval |
| ❌ | not | wassname/antipasto | Steer F1 2.0 vs 31.2 — config drift (270M reproduces at 41.7 vs 38.7) |
| ❌ | n/a | jeffreywilliamportfolio/jlens-basin-swaps | reproduction script POSTs to a hosted Neuronpedia API (api-key) |
| — | n/a | ak47na/top_down_vs_bottom_up | needs pre-generated completions + W&B artifact (unclear-entrypoint) |
| — | n/a | artmtt/sae-interp-small-reasoning | inference-gen cell commented out; inputs not committed (data) |
| — | n/a | ayoakin/mivlde | function library, no `__main__`, uncommitted activations (unclear-entrypoint) |
| — | n/a | ckkissane/sae-dataset-dependence | SAE behind a W&B artifact login (model-access) |
| — | n/a | dajale423/error_pathology | e2e_sae fork: torch 2.2 pin + missing scripts subpackage (env) |
| — | n/a | g-w1/gradient-routed-vae | 30-VAE training > 2 h (runtime) |
| — | n/a | ibm/sae-steering | torch 2.3.1 ↔ transformer-lens arity drift (env) |
| — | n/a | james-sullivan/arithmetictransformer | grokking checkpoints need ~6000-epoch × 8-ratio training (runtime) |
| — | n/a | jim-maar/interpretability | asserts checkout dir be named "interpretability" (env) |
| — | n/a | mamiglia/deep-dive-l1h5 | full-vocab hook sweep ~6 h (runtime) |
| — | n/a | sunmoonron/super-weight-circuit-patching | 3× fp32 OLMo-1B > 31 GB RAM in compare step (vram) |
| — | n/a | syvb/natural_language_autoencoders | 2×7B models, ~90 GB checkpoints, 48 GB-card design (vram) |
| — | n/a | tenseisoham/finetuning-mechinterp | `TrainingArguments(evaluation_strategy=)` removed mid-4.x (env) |
| — | n/a | thebuleganteng/interpretability-prototyping | SAE id `11-res-jb` removed across sae-lens versions (env) |
| — | n/a | uchicago-xlab/superposition-replication | dependency set does not build reliably in-queue (env) |

## Discussion

1. **Engineering rot dominates, decisively.** All 15 never-located failures and 4 of the 5 non-reproductions are packaging/hardware. The recurring rot classes (full symptom→cause→fix catalog in `lessons-synth.md` Part 3): (a) `spec.json.entrypoint` is a *pointer*, not a runnable command — prose, a pipeline step, a chain, a subset (the "fact variant"), or a function library — the single largest source; (b) 2026-major-version drift silently breaks 2024–25 code (`transformers 5` and its mid-4.x `evaluation_strategy` rename, `datasets 4`, `sae-lens 6`/`4`, `setuptools 81`, `torch 2.6`); (c) uncommitted artefacts (checkpoints, prompt files, activations, W&B-gated SAEs, commented-out generation cells); (d) Colab assumptions (`/content`, `google.colab`, placeholder tokens); (e) hardware/time budgets the catalogue mis-estimated (RAM-OOM, 48 GB designs, "minutes" that are hours).

2. **The one genuine scientific miss is informative.** AntiPaSTO reproduces on Gemma-270M (41.7 vs 38.7) but not Gemma-1B (2.0 vs 31.2) — because the repo's shipped 1B preset is *not* the paper's configuration (`git log -S` shows the paper's values never existed as defaults), compounded by a `**Yes**`-formatting artefact that suppresses the metric. It is characterised, not merely "failed."

3. **The 3 partials are honest halves, not fudges.** jordanmccann: toy + Haar-rotation exact (the repo's own `verify` passes 6/6), Pythia post-rotation EV off. idostik: the L0H3 subword-merging *mechanism* reproduces; the "only L0H3" exclusivity sweep died on transformer-lens arity drift. shivasrightfoot: the conceptual-fusion jailbreak *method* reproduces (the adapter demonstrably bypasses refusals), but the ASR percentage is computed by a separate eval notebook at a different retention setting.

4. **Tier honesty.** 3 of 14 "reproduced" are **recompute** — re-running a script over the author's committed artefacts (a shipped probe, committed graphs, committed per-cell results). They show the *repo is self-consistent*, weaker than the 11 **exact** (trained/extracted from source). A reproduction rate is only as strong as its tier mix; ours is 11 exact / 3 recompute.

## Threats to validity
- **Selection:** minute-class rows only; the 38 untouched **hours-class** rows (bigger models, more training) may reproduce *less* often and are the obvious next sample.
- **One machine (24 GB / 31 GB RAM), one operator:** 4 of the 15 non-located failures are *this box's* limits (2 vram, and RAM-bound), not universal; a bigger box would recover them. Environment fixes are logged judgement calls.
- **Recompute tier:** three rows evaluate committed artefacts, not upstream training.
- **Reason attribution:** `env` vs `runtime` vs `data` are the operator's classification; each is defended in the row's VERDICT.

## Next steps (from `handoff-synth.md` §B)
1. ✅ Tail drained; ✅ this report finalised.
2. **Package the harness** (`tree_*`, `*_imports.py`, `nb_colab_stub.py`, `publish.sh`) with `lessons-synth.md` as its manual — a reusable replication harness is arguably the larger contribution.
3. **Selectively run 2–3 high-value hours-class experiments** — contested *negative* claims / safety-relevant rows the ledger is light on — to test whether the 89%-of-located rate holds at larger scale (the main threat to the finding).
4. Deferred, human-gated: author-facing notes on AntiPaSTO (config-drift) and jordanmccann (Pythia-EV gap); AntiPaSTO evals D/E (~100 min each).
