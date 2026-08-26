# 80/20 over the replication candidates

Scored by `replication/pareto.py` on 2026-08-26 over the **142 inspected candidates** (open-weight models, code linked, a number to hit, largest model fits 24 GB on paper). Output: `replication/pareto.json`.

## The metric

Two families of factors, each 0–1, combined as a geometric mean so that a project that is worthless *or* unrunnable scores low rather than average:

**Value** — why anyone would care whether the result holds:

| factor | weight | source |
|---|---:|---|
| contested phenomenon (both positive and negative findings exist) | 2.0 | `p3/findings.md` §1 |
| in-degree: other posts whose `depends_on` names this post or repo | 1.5 | `p3/claims/` |
| phenomenon size (log n posts on the same phenomenon) | 1.0 | `p3/claims/` |
| attention (log LW karma, ×0.8 if not promoted to AF) | 1.0 | `union.json` |
| negative / null / replication claim (re-verifying one is disproportionately informative) | 1.0 | `p3/claims/` |
| target well-specified (post reported uncertainty on the headline) | 1.0 | `p3/claims/` |
| rigor (baseline, ablation, held-out, seeds, ≥2 model families — from reading, not regex) | 1.0 | `p3/claims/` |

**Feasibility** — can it run here, and will the run test the published claim:

| factor | weight | source |
|---|---:|---|
| needs a closed-model API (hard: → 0) | 3.0 | inspection |
| fits the 3090 (yes 1 / probably .8 / tight .5 / unknown .3 / no 0) | 2.0 | inspection |
| entrypoint identified, by confidence | 1.5 | inspection |
| data obtainable | 1.5 | inspection |
| headline artifact located in the repo | 1.0 | inspection |
| runtime class (minutes 1 / hours .7 / unknown .4 / days .2) | 1.0 | inspection |
| hygiene: requirements, pins, stated compute | 0.5 | inspection |

Weights are stated so they can be argued with; `pareto.py --top-frac` moves the cut.

## The finding: it is not Pareto-shaped

`[MEASURED]` The top 20% (28 projects) hold **28% of the total score**, not 80%. The distribution is flat: the 28th-ranked project scores 0.73 against the 1st at 0.81. `[INFERRED]` That is what the corpus looks like once the closed-API and does-not-fit cases are removed — a large middle of small, runnable, moderately interesting experiments, and no tail of stand-out ones. Choosing three from the top of this list is a judgment about *stake and diversity*, not a threshold the numbers hand you.

`[MEASURED]` All 28 of the top 28 are runnable here (fit yes/probably, no closed API) — feasibility is doing its job as a gate, and within the gate the ranking is driven by value factors, mostly *contested* and *negative*.

## Top 20%

| # | title | repo | phenomenon | claim | value | feas | score | fit | runtime |
|---|---|---|---|---|---:|---:|---:|---|---|
| 1 | Cross-Model Activation Generalizability Isn't Strong | `jaehoonlee0829/cross-model-alignment-geometry` | representation geometry | negative | 0.69 | 0.96 | **0.81** | yes | hours |
| 2 | Confirming Claims of Superposition and Adversarial E | `uchicago-xlab/superposition-replication` | superposition | replication | 0.69 | 0.95 | **0.81** | yes | minutes |
| 3 | AntiPaSTO: Self-Supervised Honesty Steering via Anti | `wassname/antipasto` | activation steering | positive | 0.66 | 0.98 | **0.81** | yes | minutes |
| 4 | Features of SAEs are universal - but only up to an u | `jordanmccann/polymorphism-is-rotation` | representation geometry | positive | 0.65 | 1.00 | **0.80** | yes | minutes |
| 5 | Can we interpret latent reasoning using current mech | `cywinski/codi` | interpretability tooling | positive | 0.65 | 0.99 | **0.80** | yes | minutes |
| 6 | Adding noise to a sandbagging model can reveal its t | `lovkush-a/arena-sandbagging-mi` | sandbagging | replication | 0.68 | 0.94 | **0.80** | yes | hours |
| 7 | Deep Causal Transcoding: A Framework for Mechanistic | `amack315/melbo-dct-post` | activation steering | method | 0.72 | 0.88 | **0.80** | yes | hours |
| 8 | Unpacking Multimodal Data Leakage, Broken Benchmarks | `ai-forever/data_leakage_detect` | eval methodology critique | negative | 0.63 | 0.99 | **0.79** | yes | minutes |
| 9 | [Replication] Crosscoder-based Stage-Wise Model Diff | `annasoligo/tiny-sleepers` | crosscoder / model diffing | replication | 0.65 | 0.96 | **0.79** | yes | hours |
| 10 | GPT-2's IOI behavior is defined where the paper's al | `fractalmachinist/ioi` | circuit discovery | negative | 0.63 | 0.97 | **0.78** | yes | minutes |
| 11 | Most of the residual stream forgets within a token.  | `fodenthal/residual-geometry-experiment` | representation geometry | positive | 0.64 | 0.96 | **0.78** | yes | hours |
| 12 | Can 7B-8B LLMs judge their own homework? | `dmitry-dereshev/positive-jailbreaks-llm-failure-modes` | eval methodology critique | negative | 0.66 | 0.92 | **0.78** | yes | hours |
| 13 | Matryoshka Sparse Autoencoders | `noanabeshima/matryoshka-saes` | dictionary learning method | positive | 0.67 | 0.91 | **0.78** | yes | minutes |
| 14 | Weight-Sparse Circuits May Be Interpretable Yet Unfa | `jacobcd52/sparse_pretrain_public` | circuit discovery | negative | 0.66 | 0.89 | **0.77** | yes | hours |
| 15 | A necessity check for linear safety probes | `vaiyr/probe-necessity` | linear probe detection | negative | 0.59 | 0.99 | **0.76** | yes | minutes |
| 16 | The imposters among us: function vectors that ace ev | `star2vec/tarcle` | activation steering | negative | 0.61 | 0.94 | **0.75** | yes | hours |
| 17 | Harmfulness Directions in OLMo | `harmfulness-exploration/harmfulness_direction_entanglement` | training dynamics | positive | 0.63 | 0.90 | **0.75** | yes | days |
| 18 | (Not) Explaining GPT-2-Small Forward Passes with Edg | `davidudell/sparse_circuit_discovery` | circuit discovery | negative | 0.59 | 0.94 | **0.75** | yes | unknown |
| 19 | Matryoshka NLAs: training activation verbalizers to  | `syvb/natural_language_autoencoders` | interpretability tooling | method | 0.55 | 1.00 | **0.74** | yes | minutes |
| 20 | Investigating Sensitive Directions in GPT-2: An Impr | `dajale423/error_pathology` | sparse autoencoder quality | negative | 0.59 | 0.91 | **0.74** | yes | minutes |
| 21 | Does routine compression undo LLM unlearning? A shor | `hannahtao/compression-unlearning` | machine unlearning robustn | negative | 0.58 | 0.94 | **0.74** | yes | hours |
| 22 | Positive jailbreaks in LLMs | `dmitry-dereshev/positive-jailbreaks-llm-failure-modes` | jailbreaking / adversarial | positive | 0.62 | 0.87 | **0.74** | yes | hours |
| 23 | Developmental Stages in Multi-Problem Grokking | `james-sullivan/arithmetictransformer` | training dynamics | negative | 0.55 | 0.99 | **0.73** | yes | minutes |
| 24 | Linear probes tell you where quantization will hurt | `itsme-aniketghosh/probe-guided-quantization` | linear probe detection | positive | 0.57 | 0.94 | **0.73** | yes | hours |
| 25 | Proof-of-Concept Debugger for a Small LLM | `peterlai/gpt-circuits` | circuit discovery | method | 0.61 | 0.89 | **0.73** | yes | hours |
| 26 | Evidence for feature-specific error correction in LL | `franciscohs/fsec-paper` | superposition | positive | 0.61 | 0.87 | **0.73** | probably | days |
| 27 | Superweight Damage Repair in OLMo-1B utilizing a Sin | `sunmoonron/super-weight-circuit-patching` | circuit discovery | positive | 0.53 | 1.00 | **0.73** | yes | minutes |
| 28 | SAEs are highly dataset dependent: a case study on t | `ckkissane/sae-dataset-dependence` | sparse autoencoder quality | positive | 0.57 | 0.92 | **0.73** | yes | minutes |

## The three to run first

Chosen from the top 20% for scientific stake, a target the ledger can adjudicate, GPU-relevant compute, and diversity across phenomena. Full scaffolded prompts in `3090-prompts.md`.

| pick | project | why this one | risk |
|---|---|---|---|
| 1 | **Cross-Model Activation Generalizability Isn't Strong (Yet)** — `jaehoonlee0829/cross-model-alignment-geometry` (#1) | A *negative* result against the Platonic Representation Hypothesis on six real 1–3B LLMs; representation geometry is contested 22-vs-5; the repo maps every README number to a script and states its compute (one A40). | Headline is spread across ~5 scripts; gated Llama/Gemma; hours. |
| 2 | **AntiPaSTO: Self-Supervised Honesty Steering** — `wassname/antipasto` (#3) | Activation steering is contested 19-vs-6 and safety-relevant (honesty under eval-awareness); the target is a scalar **with a reported CI** (31.2±5.3 vs 13.0 / 4.5 / 0.0); the repo ships a `gemma1b-24gb` preset for exactly this card and a `uv.lock`. | ~1 h adapter training; Gemma-3-1B is gated (token present). |
| 3 | **Adding noise to a sandbagging model can reveal its true capabilities** — `lovkush-a/arena-sandbagging-mi` (#6) | Sandbagging is the corpus's most evenly contested safety phenomenon (5-vs-6); this is itself a replication of a published method (noise injection, Tice et al.), on an ungated 1.5B model, one script; the author's own notes record prompt- and backend-sensitivity, so a third run is genuinely informative. | Target is qualitative ("for some seeds accuracy rises") → `tolerance: manual`; 100 generation runs → hours. |

Runners-up, each minutes on the card and worth running while a pick above trains: **#2** `uchicago-xlab/superposition-replication` (one CLI, toy model, already found a seed-count instability in the paper it replicates — run it at N=10), **#10** `fractalmachinist/ioi` (GPT-2 small, n=128 matched pairs, the canonical circuit), **#4** `jordanmccann/polymorphism-is-rotation` (ships `python -m replicate verify`).
