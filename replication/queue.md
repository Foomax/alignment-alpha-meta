# Replication queue — run order

87 experiments passed selection + inspection. Ranked: certain fit → short runtime → replication value (contested phenomenon, cheap model, negative result, well-specified target). Each row is a folder under `experiments/`.

| # | slug | tier | fit | runtime | VRAM | phenomenon | claim | target |
|---|---|---|---|---|---|---|---|---|
| 1 | `gpt-2-s-ioi-behavior-is-defined-where-the-paper---fractalmachinist` | T1 | yes | minutes | 2 | circuit discovery ⚔ | negative | mean drop 0.23, SD 0.84 (n=128 matched p |
| 2 | `features-of-saes-are-universal-but-only-up-to-an--jordanmccann` | T1 | yes | minutes | 4 | representation geometry ⚔ | positive | 0.976-0.990 on toy model (vs worst-case  |
| 3 | `investigating-sensitive-directions-in-gpt-2-an-i--dajale423` | T1 | yes | minutes | 4 | sparse autoencoder quality ⚔ | negative | SAE(x) KL comparable to cov-random-mixtu |
| 4 | `saes-are-highly-dataset-dependent-a-case-study-o--ckkissane` | T1 | yes | minutes | 3 | sparse autoencoder quality ⚔ | positive | LmSys-trained SAE reconstruction has sig |
| 5 | `can-we-interpret-latent-reasoning-using-current---cywinski` | T1 | yes | minutes | 4 | interpretability tooling ⚔ | positive | model recovers ~20% accuracy (from 55% b |
| 6 | `unpacking-multimodal-data-leakage-broken-benchma--ai-forever` | T1 | yes | minutes | ? | eval methodology critique ⚔ | negative | AUC ≈ 98.6% |
| 7 | `antipasto-self-supervised-honesty-steering-via-a--wassname` | T2 | yes | minutes | 8 | activation steering ⚔ | positive | 31.2±5.3 (AntiPaSTO) vs 13.0 (engineered |
| 8 | `activation-plateaus-where-and-how-they-emerge--mshinkle` | T1 | yes | minutes | 3 | representation geometry ⚔ | positive | freezing MLP block outputs completely el |
| 9 | `comparing-the-effectiveness-of-top-down-and-bott--ak47na` | T1 | yes | minutes | 4 | activation steering ⚔ | positive | top-down ~93% relative improvement over  |
| 10 | `developmental-stages-in-multi-problem-grokking--james-sullivan` | T? | yes | minutes | 1 | training dynamics ⚔ | negative | no distinct additional developmental sta |
| 11 | `a-necessity-check-for-linear-safety-probes--vaiyr` | T1 | yes | minutes | ? | linear probe detection ⚔ | negative | recovers all 17 causal handles that exis |
| 12 | `tracing-typos-in-llms-my-attempt-at-understandin--idostik` | T1 | yes | minutes | 4 | circuit discovery ⚔ | positive | only the subword merging head (L0H3) sho |
| 13 | `the-self-hating-attention-head-a-deep-dive-in-gp--mamiglia` | T1 | yes | minutes | 2 | circuit discovery ⚔ | positive | 33 of 64 eigenvalues negative |
| 14 | `confirming-claims-of-superposition-and-adversari--uchicago-xlab` | T? | yes | minutes | 1 | superposition ⚔ | replication | PGD·optimal cosine similarity = 1.00 acr |
| 15 | `matryoshka-sparse-autoencoders--noanabeshima` | T? | yes | minutes | 1 | dictionary learning method ⚔ | positive | Matryoshka SAEs have higher MMC than van |
| 16 | `an-induction-head-in-disguise-chasing-grammar-in--ameya-bit` | T? | yes | minutes | 1 | circuit discovery ⚔ | negative | B5H0 copying score 0.615 vs next-highest |
| 17 | `a-black-box-made-less-opaque-part-2--thebuleganteng` | T1 | yes | minutes | 1 | representation geometry ⚔ | positive | mean Jaccard similarity across surface f |
| 18 | `superweight-damage-repair-in-olmo-1b-utilizing-a--sunmoonron` | T1 | yes | minutes | 4 | circuit discovery ⚔ | positive | 17.4 (original) -> 2884.3 (ablated) -> 2 |
| 19 | `mechanistic-interpretability-via-learning-differ--ayoakin` | T1 | yes | minutes | 2 | circuit discovery ⚔ | positive | probes successfully predicted the time-p |
| 20 | `matryoshka-nlas-training-activation-verbalizers---syvb` | T2 | yes | minutes | 15 | interpretability tooling ⚔ | method | matryoshka NLA captures most FVE within  |
| 21 | `competitive-ai-safety-is-the-loss-function-to-ma--patrickod32` | T1 | yes | minutes | ? | interpretability tooling ⚔ | method | 0.956 top-5 agreement, 0.90 AUC (seq2fea |
| 22 | `exploring-vocabulary-alignment-of-neurons-in-lla--coolvision` | T1 | yes | minutes | 5 | representation geometry ⚔ | positive | non-symmetric, long-tailed distribution  |
| 23 | `can-we-teach-a-model-to-encode-a-semantic-featur--phusroyal` | T? | yes | minutes | 2 | representation geometry ⚔ | positive | linear probe AUC falls from 0.9996-0.999 |
| 24 | `investigating-echo-tasks-in-qwen-2-5-1-5b-instru--mild-rgb` | T1 | yes | minutes | 6 | circuit discovery ⚔ | positive | head 2 always in top-3 heads across 44 w |
| 25 | `jailbreak-patching-with-soo-style-conceptual-fus--shivasrightfoot` | T1 | yes | minutes | 6 | jailbreaking / adversarial p ⚔ | positive | ~20% (base model) to a little under 90%  |
| 26 | `banana-in-bostrom-out-paperclip-maximization-is---jeffreywilliampo` | T2 | yes | minutes | ? | activation steering ⚔ | positive | paperclip swap 3/3 per batch; doom ablat |
| 27 | `enabling-new-applications-with-today-s-mechanist--ibm` | T1 | yes | minutes | 2 | activation steering ⚔ | method | < +0.001s/token on unoptimized code |
| 28 | `exploring-how-othellogpt-computes-its-world-mode--jim-maar` | T? | yes | minutes | 3 | circuit discovery ⚔ | positive | 0.818 overall (up to 0.97 for specific l |
| 29 | `latent-space-collapse-understanding-the-effects---tenseisoham` | T1 | yes | minutes | 2 | fine-tuning side effects ⚔ | positive | 160.87 (base model) vs 49,802.45 (fine-t |
| 30 | `do-k-sparse-autoencoders-reveal-thinking-pattern--artmtt` | T1 | yes | minutes | 4 | SAE feature interpretability ⚔ | positive | feature 32456: top feature in 28/32 infe |
| 31 | `automated-circuit-interpretation-via-probe-promp--peppinob-ol` | T1 | yes | minutes | ? | attribution / attribution pa | method | concept-aligned subgraphs average 0.5394 |
| 32 | `creating-interpretable-latent-spaces-with-gradie--g-w1` | T? | yes | minutes | 1 | gradient routing for interpr | positive | 92.58% |
| 33 | `cross-model-activation-generalizability-isn-t-st--jaehoonlee0829` | T1 | yes | hours | 10 | representation geometry ⚔ | negative | cross-family max debiased CKA ~0.18-0.22 |
| 34 | `most-of-the-residual-stream-forgets-within-a-tok--fodenthal` | T1 | yes | hours | 10 | representation geometry ⚔ | positive | 17 tokens for time-lagged probes vs 1 to |
| 35 | `adding-noise-to-a-sandbagging-model-can-reveal-i--lovkush-a` | T1 | yes | hours | 8 | sandbagging ⚔ | replication | for some seeds, accuracy of the sandbagg |
| 36 | `the-imposters-among-us-function-vectors-that-ace--star2vec` | T1 | yes | hours | 8 | activation steering ⚔ | negative | margin +0.35 (12 months) and +0.34 (9 mo |
| 37 | `weight-sparse-circuits-may-be-interpretable-yet---jacobcd52` | T? | yes | hours | 4 | circuit discovery ⚔ | negative | ~30 nodes achieve task loss < 0.05 on a  |
| 38 | `sae-regularization-produces-more-interpretable-m--peterlai` | T1 | yes | hours | 1 | dictionary learning method ⚔ | positive | SAE regularization reliably yields bette |
| 39 | `analysis-of-variational-sparse-autoencoders--jadelilyx` | T? | yes | hours | 3 | sparse autoencoder quality ⚔ | negative | TopK consistently outperforms vSAE TopK  |
| 40 | `deep-causal-transcoding-a-framework-for-mechanis--amack315` | T2 | yes | hours | 16 | activation steering ⚔ | method | 62% ASR on robustified Mistral-7B-Instru |
| 41 | `what-is-the-functional-role-of-sae-errors--ambitious-mechin` | T1 | yes | hours | 10 | superposition ⚔ | positive | ablating all residual error nodes: faith |
| 42 | `learning-multi-level-features-with-matryoshka-sa--bartbussmann` | T1 | yes | hours | 12 | dictionary learning method ⚔ | positive | Matryoshka SAEs maintain absorption rate |
| 43 | `avoiding-jailbreaks-by-discouraging-their-repres--guidobergman` | T1 | yes | hours | 16 | jailbreaking / adversarial p ⚔ | positive | baseline 60.55%/59.38% -> activation add |
| 44 | `can-7b-8b-llms-judge-their-own-homework--dmitry-dereshev` | T1 | yes | hours | 6 | eval methodology critique ⚔ | negative | correct judgements ranged 29.5%-59.3% ac |
| 45 | `linear-probes-tell-you-where-quantization-will-h--itsme-aniketghos` | T1 | yes | hours | 6 | linear probe detection ⚔ | positive | guided: 99-100% (100% web-text POS, 99%  |
| 46 | `proof-of-concept-debugger-for-a-small-llm--peterlai` | T1 | yes | hours | 2 | circuit discovery ⚔ | method | cluster resampling circuits contain fewe |
| 47 | `does-routine-compression-undo-llm-unlearning-a-s--hannahtao` | T1 | yes | hours | 8 | machine unlearning robustnes ⚔ | negative | 4-bit quantization on NPO: 22% recovery; |
| 48 | `eval-awareness-steering-detects-the-test-not-the--sahilraut22` | T1 | yes | hours | 18 | sandbagging ⚔ | negative | -1.77pp swing, sub-threshold Spearman rh |
| 49 | `probing-is-not-enough-a-validity-audit-for-any-p--ratnaditya-j` | T1 | yes | hours | 16 | linear probe detection ⚔ | method | AUROC 1.00 -> 0.50 when the <is_free_tie |
| 50 | `whack-a-mole-with-a-broken-hammer-does-a-model-i--star2vec` | T1 | yes | hours | 6 | probe generalisation ⚔ | positive | 88.6% overall (vs 76.9% transcript-only, |
| 51 | `replication-crosscoder-based-stage-wise-model-di--annasoligo` | T1 | yes | hours | 6 | crosscoder / model diffing ⚔ | replication | 71% |
| 52 | `activation-magnitudes-matter-on-their-own-insigh--good-epic` | T1 | yes | hours | 2 | representation geometry ⚔ | positive | tails-only analysis improved average F1  |
| 53 | `exploring-shard-like-behavior-empirical-insights--aristizabal95` | T? | yes | hours | 2 | linear probe detection ⚔ | positive | near-perfect accuracy in most layers, dr |
| 54 | `does-your-llm-trust-you--riteshbhalerao11` | T1 | yes | hours | 18 | activation steering ⚔ | positive | all trust vectors (including orthogonali |
| 55 | `positive-jailbreaks-in-llms--dmitry-dereshev` | T1 | yes | hours | 5 | jailbreaking / adversarial p ⚔ | positive | unified enhancements: harmful totals dro |
| 56 | `do-sparse-autoencoders-saes-transfer-across-base--tommasomncttn` | T1 | yes | hours | 15 | sparse autoencoder quality ⚔ | positive | Gemma-2b: loss delta 0.51 -> 4.21, R^2 0 |
| 57 | `testing-which-llm-architectures-can-do-hidden-se--filyp` | T1 | yes | hours | 2 | hidden serial reasoning | negative | standard Mamba fails to solve the hidden |
| 58 | `transformers-don-t-need-layernorm-at-inference-t--submarat` | T1 | yes | hours | 8 | LayerNorm removal for interp | positive | Small +0.0858, Medium +0.0962, Large +0. |
| 59 | `it-s-owl-in-the-numbers-token-entanglement-in-su--loftusa` | T1 | yes | hours | 20 | subliminal / data-mediated t | positive | subliminal prompting succeeded in 12/18  |
| 60 | `the-termination-circuit-how-reasoning-models-sto--chandram-dutta` | T2 | yes | hours | 24 | CoT termination mechanism | positive | 94% firing rate when the model's own cor |
| 61 | `transformers-resist-their-own-architecture--zachdata` | T1 | yes | hours | 8 | attention token clustering d | positive | random-weight models show monotonically  |
| 62 | `minimal-prompt-induction-of-self-talk-in-base-ll--mduffster` | T1 | yes | hours | 6 | base model role/goal-languag | positive | base model: 0 regex hits for role/goal p |
| 63 | `not-explaining-gpt-2-small-forward-passes-with-e--davidudell` | T1 | yes | unknown | 9 | circuit discovery ⚔ | negative | 2 of 5 |
| 64 | `towards-a-science-of-evals-for-sycophancy--andrejfsantos4` | T1 | yes | unknown | 15 | sycophancy | method | Baseline 75%; Opinion Bias 40.7% (-34.3p |
| 65 | `harmfulness-directions-in-olmo--harmfulness-expl` | T1 | yes | days | 18 | training dynamics ⚔ | positive | mean AUROC 0.5120 (chance level) |
| 66 | `probing-knowledge-recovery-in-unlearned-models--fathmamehnoor` | T1 | yes | days | 20 | machine unlearning robustnes ⚔ | positive | forget-set representation ablation: 57-6 |
| 67 | `machine-unlearning-in-large-language-models-a-co--saketh11111` | T1 | yes | days | 8 | machine unlearning robustnes ⚔ | negative | GA: Forget loss -2.807 vs Retain -2.547; |
| 68 | `unlearning-needs-to-be-more-selective-progress-r--filyp` | T1 | yes | days | 4 | machine unlearning robustnes ⚔ | positive | 40% |
| 69 | `monosemanticity-quantization--rahulschand` | T? | yes | days | 3 | sparse autoencoder quality ⚔ | positive | full precision and 8-bit show similar, g |
| 70 | `paper-does-self-evaluation-enable-wireheading-in--daviddemitriafri` | T1 | yes | days | 20 | reward tampering | positive | Selfgrade condition: inflation reaches 0 |
| 71 | `the-ai-safety-puzzle-everyone-avoids-how-to-meas--patrickod32` | T1 | probably | minutes | 32 | interpretability tooling ⚔ | method | early layers amplify writes up to 176x ( |
| 72 | `what-we-learned-trying-to-diff-base-and-chat-mod--science-of-finet` | T1 | probably | hours | 14 | crosscoder / model diffing ⚔ | negative | 60% (crosscoder reconstruction) vs 88% ( |
| 73 | `exploring-generalization-in-nla-s--kameshkanna` | T1 | probably | hours | 18 | interpretability tooling ⚔ | positive | cosine similarity >0.50 and Recall@10 >0 |
| 74 | `selective-generalization-improving-capabilities---arianaazarbal` | T1 | probably | hours | 20 | narrow-to-broad misalignment | positive | KL divergence penalty and DPO push the P |
| 75 | `interpretable-fine-tuning-research-update-and-wo--amindtothink` | T1 | probably | unknown | 10 | interpretability tooling ⚔ | method | DPO loss goes down significantly in as f |
| 76 | `evidence-for-feature-specific-error-correction-i--franciscohs` | T1 | probably | days | 20 | superposition ⚔ | positive | contrastive directions: mean p=2.42, 95% |
| 77 | `you-don-t-need-error-nodes-you-need-better-featu--evan-lloyd` | T1 | probably | days | 14 | sparse autoencoder quality ⚔ | method | 0.379-0.535 (replacement-aware + LISTA ( |
| 78 | `llm-self-reference-language-in-multilingual-vs-e--mduffster` | T1 | tight | minutes | 30 | representation geometry ⚔ | positive | Llama 3.1 8B: -0.023 (68.8% of layers co |
| 79 | `scaling-sparse-feature-circuit-finding-to-gemma---nainanijatinz` | T1 | tight | hours | 37 | circuit discovery ⚔ | positive | learned binary masking recovers more per |
| 80 | `distillation-robustifies-unlearning--addiefoote` | T1 | tight | hours | 28 | machine unlearning robustnes ⚔ | positive | Unlearn-and-Distill more resistant to re |
| 81 | `finding-features-in-transformers-contrastive-dir--franciscohs` | T1 | tight | hours | 24 | sparse autoencoder quality ⚔ | positive | contrastive directions break through the |
| 82 | `compositionality-and-ambiguity-latent-co-occurre--mclarke1991` | T1 | tight | hours | 18 | SAE feature interpretability ⚔ | positive | co-occurrence rate decreases monotonical |
| 83 | `weight-diff-svd-for-llm-monitoring--fjzzq2002` | T1 | tight | hours | 20 | interpretability tooling ⚔ | positive | 44% to 100% accuracy, FPR ~1%; 9 of 13 m |
| 84 | `intrinsic-dimension-of-prompts-in-llms--ritareasciencepa` | T1 | tight | unknown | 28 | representation geometry ⚔ | positive | rho > 0.5 for GPT-2 (early layers) and P |
| 85 | `when-benchmarks-lie-evaluating-malicious-prompt---maxf-zn` | T1 | tight | unknown | 16 | prompt injection ⚔ | positive | recall: Agentic 99.2% (ours) vs 21.5% (L |
| 86 | `paper-automated-feature-labeling-with-token-spac--seamus-fallows` | T1 | tight | unknown | 20 | interpretability tooling ⚔ | method | converged to the correct single-token la |
| 87 | `mechanistic-estimation-for-wide-random-mlps--alignment-resear` | T? | tight | days | 18 | interpretability tooling ⚔ | positive | outperforms Monte Carlo sampling across  |

## Not queued

- 28 — needs closed API
- 15 — fit=no
- 7 — fit=unknown
- 3 — no entrypoint
- 2 — data missing
