# lessons-4 — from nodes 23–24 (2026-08-27 15:30)

New:
1. **Read which measure the claim is about before judging a "top-k" claim.** Node 24's notebook reports two rankings (direct logit attribution vs zero-ablation); the head the post names is top-3 in 44/44 by ablation and absent by DLA. The spec's `headline_artifact` names the cell; the claim text names the method ("across ablation experiments"). Judge on the named method, record the other in the notes — a ledger reader deserves the disagreement.
2. **"~90 %" sub-claims are usually the modal case.** Always report mean, min and the fraction of items where the claim holds (43/44 top-1 here) — that is what makes "reproduces with a footnote" reproducible by the next reader.
3. **When a spec's entrypoint field contains the literal command in parentheses, use it verbatim** (node 23: "`uv run python -m src.predefined_manifold run --device cuda`"). The thin runner cannot; a 2-line parser (`re.search(r"`([^`]+)`", entrypoint)`) would have saved the round trip for nodes 3, 20, 23.
4. **Repos with a `uv.lock` should be run with `uv sync && uv run`**, not with a hand-built venv — pinned deps are the closest thing to the author's environment (same choice as AntiPaSTO).

Confirmed: lessons-2 #1 (entrypoint = pointer), lessons-1 D5 (deterministic small-model analyses reproduce cleanly; 1 min for a 44-word ablation survey on a 1.5B model in bf16).
