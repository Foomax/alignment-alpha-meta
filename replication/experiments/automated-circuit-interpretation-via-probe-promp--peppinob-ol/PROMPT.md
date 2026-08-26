# Replicate: Automated Circuit Interpretation via Probe Prompting

Source post: `zQqGhKPqaCBZZDCge` (2025-11-01, LW karma 19). Repo: `peppinob-ol/attribution-graph-probing` @ `bbff7525d59a8fea7b10052739494cf7d3363cc1`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> An automated 'probe-prompting' pipeline that measures feature activation responses to concept-varying prompts and groups features into concept-aligned supernodes achieves 0.53 Replacement / 0.83 Completeness on Neuronpedia metrics for 'capitals' attribution-graph circuits in Gemma-2-2B, outperforming geometric (cosine-only, layer-adjacency) clustering baselines on behavioral-coherence interpretability metrics, with entity-swap tests showing early-layer features generalize much more (~80-92% overlap) than late-layer features (~0-50%).

Supporting quote from the post: "our concept-aligned subgraphs attain ~0.53 Replacement and ~0.83 Completeness on Neuronpedia metrics, averaged across runs, and outperform geometric clustering on behavior-based interpretability metrics."

**Headline metric:** Replacement / Completeness scores (Neuronpedia) for concept-aligned subgraphs vs. geometric clustering baselines
**Claimed value:** concept-aligned subgraphs average 0.5394 Replacement and 0.8257 Completeness across 5 prompts, outperforming cosine-only and layer-adjacency clustering on behavioral metrics like Peak Token Consistency (0.425 vs. 0.183/0.301) and Activation Pattern Similarity (0.762 vs. 0.130/0.415)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 9 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `scripts/research/graph_subgraph_scores.py` (confidence: high)
- Produces: output/research/graph_subgraph_scores.csv -- per-entity Replacement/Completeness scores that the post averages to 0.5394 Replacement / 0.8257 Completeness across 5 prompts; the entity-swap generalization numbers come from the similarly CPU-only scripts/experiments/cross_prompt_robustness.py operating on the same committed probe-activation CSVs.
- Models: Gemma-2 2B (CLT-HP transcoder)
- Estimated VRAM: 0 GB — graph_subgraph_scores.py computes Replacement = I_embed/(I_embed+I_error) and Completeness via sparse-matrix power iteration (numpy/scipy) directly over already-generated, pruned Neuronpedia attribution-graph JSON files and node_grouping CSVs -- no torch model forward pass and no GPU are involved in this script.
- Data: Neuronpedia attribution-graph JSON files for the 5 probe-prompting domains (capitals/USA-states, books, products, paintings, sounds), node_grouping classification CSVs (supernode assignments); availability: in-repo
- Estimated runtime: minutes (Not stated explicitly, but implied by the pure CPU numpy/scipy computation over graphs of at most a few thousand nodes.)
- Stated compute in the repo: none
- Known blockers: To regenerate the attribution graphs from scratch (rather than reuse what's already committed under output/graph_data/), scripts/00_neuronpedia_graph_generation.py and 01_probe_prompts.py call Neuronpedia's hosted graph-generation/activation API (needs NEURONPEDIA_API_KEY) rather than running circuit-tracer locally -- this is an external paid service, not local GPU compute; requirements.txt uses loose >= pins for most packages; only circuit-tracer is pinned to an exact git tag; The repo checkout is ~5.7GB (mostly output/ batch results, some of it duplicated), well within the 150GB disk budget but worth noting
- Inspector's notes: Surprising finding: the exact headline Replacement/Completeness numbers need zero GPU and zero API calls to reproduce, because the attribution-graph JSON and feature-grouping CSVs that graph_subgraph_scores.py consumes are already committed in the repo's output/ directory. Only from-scratch graph regeneration would touch Neuronpedia's (non-OpenAI/Anthropic/Google) hosted API; a separate, much larger Stage-3 causal-validation pipeline (33k steering runs) does use a local Gemma-2-2b + CLT via circuit-tracer on a GPU, but is not required for this specific claim.

## Budget

**45 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
at 30 minutes). When the budget is exceeded, stop and record `blocking_reason: runtime`.

## Procedure

1. `cd` into this folder. Read `spec.json`. Run `./run.sh`. It clones at the pinned sha, builds a
   venv from the repo's own requirements, runs the entrypoint under `timeout`, and logs to
   `run.log` + `vram.log`.
2. If install fails: fix **only** the environment (a version pin, a missing system package, a
   CUDA-index torch wheel). Record every fix. Do not touch experiment code. If you cannot fix it
   in 30 minutes, `report.py --reason env`.
3. If the entrypoint needs an argument the inspection did not capture, read the README and the
   script's argparse; prefer the configuration the post describes. Record it as a fix.
4. If the run needs a gated model, the HF token is already on this machine; if it is not,
   `--reason model-access`.
5. When it finishes, find the headline number in the output. Compare to the claimed value
   under the tolerance. Then:
   `python3 report.py --observed "<value>" --reason none [--fix "..."]... [--notes "..."]`
   — or with the right `--reason` if it failed. If the metric is not a scalar, pass
   `--reproduced true|false` and say why in `--notes`.
6. Append 3–6 lines to `run.log` under `== VERDICT`: what you observed, what you compared it to,
   what you changed, what you would need to go further.

## Do not

- Do not run more than **1 seed(s)** unless the run is under 10 minutes; if it is, run 3
  and report the spread — that is more valuable than the point estimate.
- Do not substitute a different model, dataset, or judge and call it a replication. Note it as a
  follow-up in `--notes` instead.
- Do not read the post's conclusion into ambiguous output. If you cannot tell which number is
  the headline, `--reason unclear-entrypoint` and say what you saw.
- Do not push, do not open issues, do not contact the authors.
