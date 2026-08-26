# Replicate: Exploring how OthelloGPT computes its world model

Source post: `wezSznWnsMhpRF2QH` (2025-02-02, LW karma 8). Repo: `jim-maar/interpretability` @ `73bc8f299f29823ad2ac1d288861dbb21b0e9f4f`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> OthelloGPT's attention heads implement a 'Previous Color Circuit' that copies each tile's color forward from the most recent move at which it was flipped, reconstructing the probed board state with 0.818 accuracy, while a competing hypothesis that monosemantic MLP neurons implement discrete flipping rules failed an ablation test.

Supporting quote from the post: "I think the results show that the previous color circuit is meaningful. But the model actually does something more complicated, so it's better thought of as a rough approximation of what the attention layers are doing."

**Headline metric:** reconstruction accuracy of previous-color-circuit probe vs real attention output
**Claimed value:** 0.818 overall (up to 0.97 for specific layer/position/tile combinations)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:0.05` — unit-interval metric: 0.05 absolute; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `prove_circuits_last_flipped.py (equivalently prove_circuits_last_flipped.ipynb)` (confidence: high)
- Produces: scores_math['Accuracy'] / scores_test['Accuracy'] computed in prove_circuits_last_flipped.py via get_score_from_results (tp+tn)/(tp+tn+fp+fn), aggregated over layer/pos/row/col -- this is exactly the 'reconstruction accuracy of previous-color-circuit probe vs real attention output' metric in the post.
- Models: NeelNanda/Othello-GPT-Transformer-Lens (synthetic_model.pth) (0.025B)
- Estimated VRAM: 3 GB — OthelloGPT is GPT2-small-scale: 8 layers, d_model=512, d_mlp=2048, n_heads=8, d_vocab=61, n_ctx=59 (~25M params); the script runs it with run_with_cache over batches of 200 board sequences (length 59) for 1000 batches per configuration -- trivial VRAM for a model this size.
- Data: board_seqs_int_small.npy / board_seqs_string_small.npy (from the external likenneth/othello_world repo; the git-clone line for it is present but commented out in the script), pretrained linear/flipped/legal/accessible probes (all included in-repo under probes/mid and probes/post, e.g. probes/post/linear/resid_{0..7}_linear.pth); availability: download-script
- Estimated runtime: minutes (1000 batches x 200 games x 7 layers x 2 attention-pattern variants x 2 prediction methods (get_yours_and_mine_pred_math2 vs get_yours_and_mine_pred_old) of forward-cache passes through a ~25M-param model -- large in call count but each pass is cheap; should run in minutes on a 3090.)
- Stated compute in the repo: none
- Known blockers: board_seqs_int_small.npy / board_seqs_string_small.npy are not included in this repo; the `git clone https://github.com/likenneth/othello_world` line that would fetch them is commented out, so a re-runner must uncomment/run it manually (well-known public repo, low friction); the competing-hypothesis ablation test appears to live in flipping_circuit/prove_flipped_circuit_2.py, which loads data/board_seqs_int_train.pth and data/board_seqs_int_valid.pth -- neither this data/ directory nor any script to produce those .pth files exists anywhere in the repo (unlike the othello_world .npy files, there is no documented source for these), and a code comment ('with 60 GB RAM I can do 20.000') suggests the default NUM_GAMES_TRAIN=10000 config is itself close to the 31GB RAM budget
- Inspector's notes: Bachelor's-thesis repo built on the ARENA_3.0 OthelloGPT tutorial; requirements.txt is a broad ARENA course environment (includes unrelated openai/gym/mujoco packages) but no OpenAI/closed-API calls appear in the analyzed scripts. The main previous-color-circuit accuracy claim is well-supported and cheap to reproduce; the disproved MLP-neuron-rule competing hypothesis (a secondary but still claim-relevant result) has an undocumented, missing training/validation dataset.

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
