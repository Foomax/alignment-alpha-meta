# Replicate: Positive jailbreaks in LLMs

Source post: `KLqiDczfZsmhzEhax` (2025-01-29, LW karma 6). Repo: `dmitry-dereshev/positive-jailbreaks-llm-failure-modes` @ `cadbd53880e9c2f3979710e45757a75a7fd0e583`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Prepending certain LLM instructions unrelated to safety (a 'unified enhancements' persona instruction) can reduce successful responses to harmful JailbreakBench prompts while leaving harmless-prompt performance roughly the same or improved for one of three tested 7B-scale LLMs (Ghost 7B), demonstrating 'positive jailbreaks' that improve safety without an explicit safety instruction; a second instruction ('fractal leaping') instead degraded performance on both harmful and harmless queries across all three models.

Supporting quote from the post: "This work observed two such LLM + instruction combos, though there are likely other LLM-token combos that would show the same results."

**Headline metric:** count of competent+complete responses out of 100 harmful / 100 harmless JailbreakBench prompts, vs baseline
**Claimed value:** unified enhancements: harmful totals dropped 36->23 (Ghost), 32->14 (Falcon), 42->23 (OpenOrca); harmless totals: 78->80 (Ghost, +2), 62->57 (Falcon, -5), 76->74 (OpenOrca, -2)
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 15 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `benchmark_llms.py` (confidence: medium)
- Produces: Per-model response CSVs from benchmark_llms.py, scored into 'competent and complete' counts as tabulated in 'Analysis Summary.ods' / '2024-12-29 Validate Judgement.csv'
- Models: ghost-7b-v0.9.1-Q4_0.gguf (GPT4All model hub) (7B), gpt4all-falcon-newbpe-q4_0.gguf (GPT4All model hub) (7B), mistral-7b-openorca.gguf2.Q4_0.gguf (GPT4All model hub) (7B)
- Estimated VRAM: 5 GB — Q4_0-quantized 7B GGUF models run via GPT4All with device="cuda"; each is roughly 4-5GB.
- Data: JailbreakBench malicious/benign prompt CSVs (100 each); availability: in-repo
- Estimated runtime: hours (Not stated; inferred from 10 models x 2 datasets x 2 system prompts x 100 prompts x up to 2048 generated tokens each via GPT4All (only 3 of the 10 models are relevant to this specific post).)
- Stated compute in the repo: none
- Known blockers: The headline 'competent+complete' counts are produced by human grading of each generated response (README: '...vs. a human judge assessing their responses'); the repo's code generates raw responses but contains no scripted grader that reproduces the final counts; No requirements.txt or pyproject.toml anywhere in the repo; GGUF model weight files are not included and must be obtained separately from the GPT4All model hub (allow_download=False is set in the scripts, so paths must be supplied manually)
- Inspector's notes: Mechanically cheap to rerun (local, open-weight, quantized 7B models on GPU), but exactly reproducing the reported harmful/harmless totals requires redoing the same manual/human grading step the original author did, since that scoring logic isn't in the code.

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
