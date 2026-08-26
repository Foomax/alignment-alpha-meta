# Replicate: It's Owl in the Numbers: Token Entanglement in Subliminal Learning

Source post: `m5XzhbZjEuF9uRgGR` (2025-08-06, LW karma 41). Repo: `loftusa/owls` @ `d14954773195585a1e2e4347d4321e89a46bad15`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Subliminal learning is driven by entangled tokens created by the softmax bottleneck: increasing a concept token's probability (e.g. 'owl') also increases the probability of seemingly unrelated entangled tokens (e.g. '087'), and prompting a model with an entangled numeric token alone can induce the corresponding animal preference without any fine-tuning ('subliminal prompting')

Supporting quote from the post: "When we increase the probability of a concept token like "owl", we also increase the probability of seemingly unrelated tokens like "087"."

**Headline metric:** success rate of inducing target animal preference; token probability shift
**Claimed value:** subliminal prompting succeeded in 12/18 animals vs 7/18 for subliminal learning; prompting 'You love the number 087' raised P(owl) into the top-5 tokens from ~1%, and 'You love the number 23' raised P(cat) from ~1% to 90%
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 10 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `animals.py (headline subliminal-prompting results); experiments/Subliminal Learning.py has the fuller entanglement-discovery analysis` (confidence: high)
- Produces: results/<model>/subliminal_prompting.csv and final.csv, matching the 'P(owl) raised into top-5' / success-rate claims
- Models: meta-llama/Llama-3.2-1B-Instruct (1.0B, gated), Qwen/Qwen2.5-7B-Instruct (7.0B), google/gemma-2-9b-it (9.0B, gated), allenai/OLMo-2-1124-7B-Instruct (7.0B)
- Estimated VRAM: 20 GB — animals.py loads models with torch_dtype='bfloat16'; largest model used is Gemma-2-9b-it (~18GB weights in bf16). Pure inference (forward passes only, no backward/training), small batched prompts.
- Data: animal/number/tree word lists (in-repo: animals.py, utils/animals_utils.py, data/animal_preference_numbers); availability: in-repo
- Estimated runtime: hours (No stated runtime; inferred from being a pure-inference logit/probability sweep over ~18 animals x number tokens per model, consistent with results/ CSVs already present for 4 models (gemma-2-9b-it, Llama-3.1-8B-Instruct, OLMo-2-1124-7B-Instruct, Qwen2.5-7B-Instruct))
- Stated compute in the repo: none
- Known blockers: The '7/18 for subliminal learning' baseline (actual gradient-based fine-tuning, as opposed to prompting) does not appear to be implemented in this repo — no LoRA/Trainer/SFT code found anywhere in the .py files; it likely comes from the original Cloud et al. paper rather than being reproduced here; Llama-3.2-1B-Instruct and Gemma-2-9b-it require HF gated-model access
- Inspector's notes: The subliminal-PROMPTING half of the claim (pure inference, no fine-tuning) is directly and cheaply reproducible, with results already checked into results/ for 4 models. The subliminal-LEARNING (fine-tuning) comparison number used for the 12/18 vs 7/18 headline figure does not appear to have in-repo reproduction code.

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
