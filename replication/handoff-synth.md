# handoff-synth (v2) — operating instructions + research direction (2026-08-28 04:40)

Supersedes v1 and handoff-0…26 (kept as history). Read this first; it bakes in `lessons-synth.md`. §A = how to operate. §B = where the research is and what to do next (read this — it changes the plan).

═══════════════════════════════════════════════════════════════════
## §A — OPERATING

### A0. Non-negotiable rules
1. Environment-only fixes, on copies, each a `--fix` line. Never change prompts/thresholds/dataset-slices/metrics/seed-counts/model.
2. No hosted-model APIs (even keyless) → `api-key`.
3. Pin the `spec.json` commit; no `git pull`.
4. One venv per experiment, built and **deleted** by the queue; never touch the base env.
5. Never push to authors' repos / open issues / contact authors. Push only to the three allowlisted `Foomax` forks via `publish.sh`; create no new forks.
6. Commit only `replication/` in `Foomax/alignment-alpha-meta` (master). Leave the user's other root files.
7. Don't stop for human guidance — write it in `human-oversight.md`, keep the GPU busy.
8. After every finished run/juncture: `handoff-N.md` + `lessons-N.md` (next: handoff-27, lessons-23) + a `human-oversight.md` section; commit; push.
9. Tiers: `[MEASURED]`/`[INFERRED]`/`[UNRESOLVED]`; no superlatives; a ledger entry is the goal, not a success.

### A1. State (2026-08-28 04:40)
- **Ledger: 25 attempted, 24 installed, 16 ran, 17 located, 14 reproduced** (`python3 replication/ledger.py`). Taxonomy: none 16 (14 reproduced + 2 ran-but-not: AntiPaSTO config-drift, jordanmccann partial), runtime 3, env 2, unclear-entrypoint 2, api-key 1, vram 1.
- **Reproduced (14):** cross-model-geometry, sandbagging-03, ioi, probe-necessity, induction-head, coolvision, mild-rgb, ai-forever, codi, matryoshka-saes(toy), phusroyal, seq2feature, mshinkle, peppinob. **Not-reproduced ran (2):** AntiPaSTO (config drift; 270M reproduces, 1B doesn't), jordanmccann (toy+Haar ✓, Pythia-EV ✗).
- **Repo:** `~/alignment-literature-meta-analysis/replication/` (=`$R`). Forks: `Foomax/{AntiPaSTO,arena-sandbagging-mi,cross-model-alignment-geometry}` branch `replication-3090`. Mirror: `/media/user/466CD2B96CD2A34B/home/alignment-replication-3090-2026-08/` every 10 min. Memory notes in `~/.claude/projects/-home-user-prompts/memory/`.

### A2. Running now (detached; survive sessions)
- `$R/tree_late.sh` — disk-bounded queue: reads `tree_late.txt` (`name|slug|timeout_min|cmd`), skips `tree_late_done.txt`, waits while GPU busy or <25 GB free, per entry `tree_prep.sh`→cmd→**delete venv**; one line/node to `tree.log`. Stop: `touch $R/tree_late.stop`.
- Remaining tail (final attempts, ~9): R12c, R14d, R18c, R25d, R28d, R29d, R30d, R4d, R5d. **These are the hard version-drift/gated/runtime cases — see §B: do not keep requeuing past 2–3 tries.**
- `$R/tree_publish.sh` — commits `replication/` after each node. `$R/mirror.sh --loop`.
- Helpers: `tree_prep.sh` (env), `tree_imports.py` (AST import scan), `tree_autofix.py` (module→pkg map), `nb_colab_stub.py` (Colab sys.modules stub w/ `__spec__`), `publish.sh`, `ledger.py`.

### A3. Judgement loop (per `NODE … EXIT` line)
`tail -40 $R/tree.log`; read `$d/run.log` (strip ANSI, `tr '\r' '\n'`, `awk '/RERUN:/{f=1}f'`), `autofixes.txt`, `prep.log`. Decide: system-failure (fix env/disk, don't ledger) → my-invocation (translate entrypoint, requeue) → environment (fix per `lessons-synth` Part 3, requeue; **cap 2–3, then ledger the reason**) → it-ran (judge). To judge: match `target_value` on the *named measure*, extract from `executed.ipynb`/HTML-plotly/CSVs, append `== VERDICT` + `report.py --observed … --reproduced … --reason … --notes …`, add a `human-oversight.md` section, write handoff-N/lessons-N, commit+push. Fork slugs → update `README.{human,llm}.md` + `publish.sh`.

═══════════════════════════════════════════════════════════════════
## §B — RESEARCH DIRECTION (critical evaluation + next 1–2 steps)

### B1. What the data says now
25 attempts is a real sample. Of the **17 that ran far enough to test the claim, 14 reproduced (82%)**. The 3 that didn't are: 1 hosted-API artefact (jlens, not a science failure), 1 config-drift (AntiPaSTO — the repo no longer ships the paper's 1B config, though it reproduces on 270M), 1 partial (jordanmccann — 2 of 3 components exact). So **genuine scientific non-reproductions ≈ 2 of ~15 real tests.** Everything else that failed (8 nodes: env×2, runtime×3, unclear-entrypoint×2, vram×1) failed on *engineering or hardware*, never on the science.

**Headline meta-finding (defensible now):** *When the code runs at all, published alignment-forum empirical work reproduces at a high rate to the stated precision. The binding constraint on reproducibility is engineering rot — prose "entrypoints", version drift, uncommitted artefacts, Colab assumptions, and hardware/time budgets — not scientific fragility.* That is exactly what readme.md R5 asked the ledger to measure, and it is the actual product.

### B2. Where the current trajectory is going wrong
The last ~10 nodes have been 2–3-requeue grinds on the hardest dependency-drift/gated/multi-hour cases. Each adds a taxonomy row but **near-zero new scientific signal** — they confirm "engineering rot," which is already established. Continuing to grind the tail is the low-value path (lessons-synth P13).

### B3. Next steps, in priority order (1–2 ahead)
1. **Let the tail drain, then STOP requeuing.** When `tree_late.txt` is empty, ledger any remaining failures with their honest reason. Do not open new requeue rounds.
2. **Write the aggregate meta-report** (`replication/META-REPORT.md`): reproduction rate, the failure taxonomy, the **quality tiers** (lessons-synth Part 4: T-exact vs T-recompute vs T-partial vs T-not — several "reproduced" rows are recomputes of committed artefacts, not from-scratch; this distinction sharpens the claim), and the headline finding. This is the deliverable, not more rows. ~1–2 h, CPU only.
3. **Add the quality-tier field to each `ledger.json`** (a 30-min pass) so the aggregate is machine-summarisable and the "82% reproduced" number is honest about *how* each was reproduced.
4. **Then, selectively, 2–3 high-value "hours"-class experiments** from `queue.md` (38 untouched, vs 34 minute-class mostly done). The ledger is light on hours-class and on *negative* claims; pick the contested negatives / safety-relevant ones that would most move the meta-picture — NOT all 38. Candidates to scan first: the negative-claim, ⚔-contested, ≤16 GB rows.
5. **Package the harness** (`tree_*.sh`, `*_imports.py`, `nb_colab_stub.py`, `publish.sh`) with `lessons-synth.md` as its manual — a reusable replication harness is arguably a bigger contribution than 5 more marginal rows (lessons-synth P14).
6. **Deferred, post-replication, human-gated:** the two clear findings (AntiPaSTO config-drift, jordanmccann Pythia-EV gap) are worth a concise author-facing note *when the ledger is published* — via the existing forks, never during (rule A0.5). Also: AntiPaSTO 01 evals D/E (~100 min each) and a 3rd 270M seed remain the only high-value GPU follow-ups from the protocol trio.

### B4. The one thing to ask the user
Whether to (a) stop after the tail + write the meta-report (recommended — the finding is in), or (b) push into the hours-class queue for a bigger sample. Everything else is decided.

## §C — Do-not
Don't grind requeues past 2–3; don't relaunch `tree_queue.sh`/`tree_rerun*.sh` (done); don't ledger from disk-full-window lines; don't create forks/PRs/issues; don't commit outside `replication/`; don't paste tokens into notebooks; don't "fix" author code beyond imports/paths/device on copies; pause the agent, not the GPU.
