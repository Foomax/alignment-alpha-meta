# Replicate: Compositionality and Ambiguity: 
Latent Co-occurrence and Interpretable Subspaces

Source post: `WNoqEivcCSg8gJe5h` (2024-12-20, LW karma 36). Repo: `mclarke1991/sae_cooccurrence` @ `68522cb26f33bb95ca0cc7da6cfa625be2954764`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> SAE latents are not always independent: a small fraction of latents in GPT2-Small and Gemma-2-2b (Gemma Scope) SAEs form co-occurrence clusters that map interpretable subspaces, including cases of compositional encoding (e.g. discrete quantifiers like 'one of'/'some of'/'all of' combine predictably by relative activation strength) and cases where co-occurrence reflects lexical ambiguity (e.g. senses of 'how'); the rate of co-occurrence and the size/prevalence of these clusters both decrease as SAE width increases.

Supporting quote from the post: "we find that these subspaces show latents acting compositionally, as well as being used to resolve ambiguity in language"

**Headline metric:** rate of SAE latent co-occurrence per token vs SAE width
**Claimed value:** co-occurrence rate decreases monotonically as SAE width increases in both GPT2-Small (widths 768-49152) and Gemma-2-2b; cluster (subgraph) size and prevalence also decrease as SAE width increases
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 5 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `src/size_effects/features_active_per_token.py:main() (Fig 3B / Appendix Fig 1 -- SAE latent occurrence-per-token vs width)` (confidence: medium)
- Produces: results/size_effects/*/sae_firing_stats.npy + width_sae_firing_stats_combined_plot.png (Fig 3B); results/*/dataframes/node_info_df_*.csv feeding subgraph_size_vs_width.ipynb (Fig 9)
- Models: gpt2 (gpt2-small) (0.124B), google/gemma-2-2b (2.6B, gated)
- Estimated VRAM: 18 GB — Dense d_sae x d_sae float32 co-occurrence matrix accumulated on GPU: fine at the widths actually used for the occurrence-vs-width plot (GPT2 up to 49152 -> ~9.7GB; Gemma-2-2b Gemma Scope up to 65536 -> ~17.2GB); code comment: batching is done 'to keep execution within memory on e.g. an A100.'
- Data: pretraining-corpus activations streamed via SAE Lens ActivationsStore (whatever corpus the SAE was trained on); availability: hf-hub
- Estimated runtime: hours (n_batches=100-500 at train_batch_size_tokens=4096 per SAE id, repeated across ~8 GPT2 widths and ~9 Gemma SAE ids/thresholds, each a streaming forward pass plus an O(d_sae^2) accumulation.)
- Stated compute in the repo: none
- Known blockers: The 'cluster (subgraph) size/prevalence decreases with width' half of the claim (Fig 9, subgraph_size_vs_width.ipynb) draws on Gemma Scope SAE widths up to 262k/524k/1,048,576 (config_gemma_widths.toml). The co-occurrence matrix is computed DENSE as a [d_sae,d_sae] float32 tensor (compute_cooccurrence_matrices in normalised_cooc_functions.py): width=262k needs ~274GB and width=1M needs ~4.4TB just to hold the matrix -- infeasible on 24GB VRAM or 31GB RAM regardless of GPU. Only widths up to ~65k (Gemma) / ~49k-98k (GPT2) are computable within budget, and the repo's own checked-in results/ directory only goes that far (no 262k/524k/1M result files present).
- Inspector's notes: Gemma-2-2b is gated on HF; GPT2-small and the SAEs (res-jb, Gemma Scope) are public. Two distinct measurements back the claim: the firing/occurrence-rate-vs-width plot (feasible on a 3090) and the subgraph-size-vs-width plot (infeasible past ~65k SAE width due to the dense co-occurrence matrix).

## Budget

**240 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
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
