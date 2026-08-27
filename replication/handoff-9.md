# handoff-9 — resumed after the usage pause (2026-08-27 17:05)

## New since handoff-8
- **Mirror**: `replication/mirror.sh --loop` copies the repo (minus venvs), `~/prompts`, and the assistant memory to `/media/user/466CD2B96CD2A34B/home/alignment-replication-3090-2026-08/` every 10 min (NTFS; `--no-links`). `last-mirror.txt` = last sync; `touch mirror.stop` ends it.
- **Pass 1 done** (nodes 25–32 finished 15:41) and **rerun pass 1 done** except R6 (`cywinski/codi`, 95-min box, running). Results: R7 ✓ reproduced (AUC 0.9887; ledgered). R3 needs `replicate fetch-artifacts`; R4's `e2e_sae` wheel lacks `scripts/` (needs an editable clone); R5/R8/R14/R25/R30/R32 each died one module short; R10's `neel-plotly` is GitHub-only; R13 (`skew_analysis.py`) needs > 45 min; R27 pins `torch==2.3.1` (cu121); R28/R29 hit transformers-5 / datasets-5 API removals.
- **`tree_imports.py`**: scans every `.py`/`.ipynb` in a repo for top-level imports → pip names (stdlib/local filtered, module→package map shared with `tree_autofix.py`). Late-queue commands now call it to pre-install everything in one go.
- **Late queue** (`tree_late.txt`, 20 entries, 0 done): R15, R17, R18, R19, R20, R21, R23, R3b, R4b, R5b, R8b, R10b, R13b(120 min), R14b, R25, R27, R28, R30, R32, R29 (fine-tune + logit-lens chain, 90 min). `tree_rerun2.sh` (R12) runs before it. Expect ~10–14 h of GPU if every box is used; most will be minutes.
- Node 26 (`jlens-basin-swaps`): script ran in <1 min and shows the paperclip swap (baseline "…lasting peace" → "…maximize the number of paperclips"); the doom-ablation and temperature counts are not in that script — judge as partial when ledgering (pending a read of the script, this turn).
- Node 31 (`attribution-graph-probing`): `graph_subgraph_scores.py --datasets <dirs under output/>` over the committed graph data — needs the right dataset dirs (see run.log / oversight); no API needed for the committed graphs.

## Ledger: 11 rows — 8 reproduced (01, 03, ioi, probe-necessity, induction-head, coolvision, mild-rgb, ai-forever), 1 not, 1 unclear-entrypoint, 1 pending (26).
## Continue: judge `tree.log` lines as they arrive (`handoff-4` loop); numbering next: handoff-10, lessons-6.
