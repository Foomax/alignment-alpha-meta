# Replicate: Scaling Sparse Feature Circuit Finding to Gemma 9B

Source post: `PkeB4TLxgaNnSmddg` (2025-01-10, LW karma 88). Repo: `nainanijatinz/scalablesaecircuits` @ `f54a4efce908432b8771ea671a248ee30ec2b3af`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Placing sparse autoencoders only at a few residual-stream locations (rather than at every layer/component) combined with a learned binary-mask circuit-finding method (via continuous sparsification) scales SAE-based circuit discovery to Gemma 9B, finds more faithful circuits with fewer latents than existing thresholding methods like Integrated Gradients across code-output-prediction, subject-verb-agreement, and IOI tasks (one circuit achieves 95% faithfulness with <20 total latents), and the resulting minimal circuits reveal exploitable model vulnerabilities (e.g. a successful adversarial dictionary-key prompt).

Supporting quote from the post: "Our discovered circuits paint a clear picture of how Gemma does a given task, with one circuit achieving 95% faithfulness with <20 total latents."

**Headline metric:** circuit faithfulness (ratio of circuit performance to full-model performance) vs. number of latents
**Claimed value:** learned binary masking recovers more performance with fewer latents than Integrated Gradients across all tested tasks (dictionary-key and list-index code output prediction, SVA, IOI); one circuit achieves 95% faithfulness with fewer than 20 total latents
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `ScalableSAECircuits_Colab.ipynb (README's designated 'Main Masking notebook'); per-task variants also exist under task_specific/` (confidence: medium)
- Produces: faithfulness-vs-num-latents frontier plot ('Integrated Gradients' vs 'Learned Masking') in the Colab notebook's Circuit Comparisons/Faithfulness section, and the per-threshold masks/<task>/.../*.json circuit files
- Models: google/gemma-2-9b (9.24B, gated)
- Estimated VRAM: 37 GB — ScalableSAECircuits_Colab.ipynb and task_specific/circ_disc.py call HookedSAETransformer.from_pretrained('google/gemma-2-9b', device=device, cache_dir=hf_cache) with no dtype argument, which defaults to float32 (~37GB for 9.24B params) — already exceeds 24GB before adding 4 attached Gemma-Scope-9B SAEs (d_sae=16384 each) and mask-optimization activation caching. A one-line dtype=torch.bfloat16 patch (not present in the repo) would bring weights to ~18.5GB, making it tight-but-plausible with the SAEs and short sequences (7-41 tokens) added on top.
- Data: data/sva, data/codereason, data/ioi task JSON files (all shipped in-repo); availability: in-repo
- Estimated runtime: hours (No runtime stated for the 9B masking runs; the related gemma-2-2b SLURM job requests an 8-hour wall-clock limit. The 9B pipeline runs binary-mask gradient optimization over multiple sparsity thresholds (5-10) across 4 tasks (dictionary-key, list-index code output, SVA, IOI), each over up to 3000 prompts.)
- Stated compute in the repo: scripts/sae_gap.sh SLURM header: '#SBATCH -G 1', '#SBATCH --constraint=a100', '#SBATCH --mem=100GB', '#SBATCH -t 8:00:00' — but this job runs google/gemma-2-2b, not the 9B headline model; no hardware is stated for the 9B Colab runs.
- Known blockers: No requirements.txt / pyproject.toml / environment.yml anywhere in the repo; dependencies must be inferred from notebook !pip install cells; Main notebook loads gemma-2-9b at default float32 (~37GB), exceeding a 24GB card unless the user patches in bf16 themselves; gemma-2-9b and the Gemma-Scope-9b SAEs are gated on HF Hub (license acceptance required); Repo is a loose collection of one Colab notebook plus several per-task notebooks and dev scripts with inconsistencies (e.g. sae_gap.sh actually runs gemma-2-2b, not the 9B headline model) rather than one clean, single entrypoint
- Inspector's notes: Gemma-2-9B is right at the edge of a single 24GB card and only plausible with an undocumented bf16 patch; as literally shipped (fp32 default) it will not fit. The only concrete hardware evidence in-repo (single A100) is for a smaller side experiment on gemma-2-2b, not the 9B headline runs.

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
