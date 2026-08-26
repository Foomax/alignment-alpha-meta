# Replicate: Can 7B-8B LLMs judge their own homework?

Source post: `yJ2Ka2EgQY7PnR9jL` (2025-02-01, LW karma 1). Repo: `dmitry-dereshev/positive-jailbreaks-llm-failure-modes` @ `cadbd53880e9c2f3979710e45757a75a7fd0e583`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Ten consumer-grade 7B-8B LLMs asked to judge whether responses to JailbreakBench prompts were competent and complete perform only marginally better than chance (56-59% correct for most models) against human ground truth, overwhelmingly biased toward answering '1' (up to 98% for Ghost 7B), with two models (Falcon 7B, both Llamas) failing to produce a valid judgement on 37-49% of queries.

Supporting quote from the post: "Correct judgements in other LLMs were in the range of 56%-59% making them only marginally better judges than chance."

**Headline metric:** % judged correctly (vs human ground truth) / % answered '1'
**Claimed value:** correct judgements ranged 29.5%-59.3% across models (most 56-59%); % answering '1' ranged from 34% to 98%, vs 57% ground truth positive rate; failure rates up to 49% (Falcon 7B)
**Direction of the claim:** -
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `manual` — headline is a compound of 10 numbers; compare the components by hand

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `test_llm_judgement.py` (confidence: high)
- Produces: per-model '<model> judgement test 2.csv' outputs (% answering '1' vs human ground truth) that back the post's per-model judge-accuracy table
- Models: ghost-7b-v0.9.1-Q4_0.gguf (GPT4All catalog) (7.0B), gpt4all-falcon-newbpe-q4_0.gguf (GPT4All catalog) (7.0B), Meta-Llama-3-8B-Instruct.Q4_0.gguf (GPT4All catalog) (8.0B), Meta-Llama-3.1-8B-Instruct-128k-Q4_0.gguf (GPT4All catalog) (8.0B), mistral-7b-instruct-v0.1.Q4_0.gguf (GPT4All catalog) (7.0B), mistral-7b-openorca.gguf2.Q4_0.gguf (GPT4All catalog) (7.0B), Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf (GPT4All catalog) (7.0B), orca-2-7b.Q4_0.gguf (GPT4All catalog) (7.0B), mpt-7b-chat-newbpe-q4_0.gguf (GPT4All catalog) (7.0B)
- Estimated VRAM: 6 GB — GPT4All Q4_0-quantized 7-8B GGUF models typically need ~4-6GB; scripts set device='cuda' and load one model at a time; no figure stated in repo
- Data: JailbreakBench malicious/benign prompts (included as CSV), 2024-12-29 Validate Judgement.csv (included, but missing the per-model response columns the script reads); availability: in-repo
- Estimated runtime: hours (not stated; 10 local model loads x row-by-row generation (max_tokens=2048) with no batching via GPT4All)
- Stated compute in the repo: none
- Known blockers: test_llm_judgement.py reads item[1][model_name] — a per-model response column — from '2024-12-29 Validate Judgement.csv', but the committed CSV's actual header is ID,Goal,Behavior,Category,Source,Type,Responded,Prompt type with no response columns; running the script as-is raises a KeyError immediately; GGUF weights (~4-6GB each x9-10) must be manually downloaded from the GPT4All catalog and placed in './'; allow_download=False in the script so this isn't automated; no requirements.txt; gpt4all package version unpinned
- Inspector's notes: README says response data was deliberately omitted ('many are harmful') and that scripts can regenerate it, but benchmark_llms.py writes a differently-shaped CSV than what test_llm_judgement.py reads, so the two scripts don't chain together as committed — a data-plumbing gap, not a compute blocker. All 10 models are small quantized 7-8B GGUFs, trivially fits a 3090.

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
