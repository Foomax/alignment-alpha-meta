# handoff-6 — after node 22 (2026-08-27 15:25)

- Node 22 (`coolvision/interp`, Llama-3.2-1B neuron–vocabulary alignment) **reproduced** (qualitative claim quantified from plotly traces; ledgered).
- Nodes 20, 21 were plumbing (chain entrypoint; Colab `/content` paths) → R20, R21 in the late queue (`tree_late.txt`, now 6 entries: R15, R17, R18, R19, R20, R21).
- Pass 1 is on node 23 (`phusroyal`); 24–32 remain. Then `tree_rerun.sh` (9 nodes), `tree_rerun2.sh` (node 12), and the late queue drain in that order, all automatically, one GPU job at a time.
- Ledger: 9 rows — 6 reproduced (01, 03, ioi, probe-necessity, induction-head, coolvision), 1 not (02), 1 unclear-entrypoint (ak47na), 1 pending rerun (ai-forever defaults ≠ headline config).
- Docs: handoff-0…6, lessons-1…3, human-oversight §0–9. Mechanics unchanged from handoff-4.
