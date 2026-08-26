# human-oversight.md — things a human should know or decide (running log)

Plain-language explanations of what the machine is doing, and step-by-step instructions for anything that needs *you*. I do not stop for these; I note them here and keep the GPU busy. Newest at the bottom.

---

## 0. What is running right now (2026-08-27 07:25)

Think of a bakery with one oven (the graphics card). The queue of "cakes" is:

1. **Project 01 — "do different model families think alike?"** Six models were downloaded (22 GB, took 1 h 46 min). The first bake failed instantly because the recipe's own scripts couldn't find the recipe folder (a path setting, `PYTHONPATH`); fixed, re-baking now. Expect ~45 min.
2. **31 quick projects**, one after another, each in its own sandbox. Two of them failed in seconds on the first pass for boring reasons (a sandbox that never got created; a notebook that assumed `pip` exists). The queue was paused, the runner fixed, and it restarts from the first quick project once the oven is free.

Scorecard so far: 2 rows (AntiPaSTO — did not reproduce; noise‑injection sandbagging — reproduced). Everything is committed to `Foomax/alignment-alpha-meta` as it happens.

## 1. Decisions already taken on your behalf (say so if you disagree)

| # | decision | why | to reverse |
|---|---|---|---|
| 1.1 | **The "key repo" is `alignment-literature-meta-analysis` = `Foomax/alignment-alpha-meta`, and it is already yours** (you created it; `origin` points at your account). Nothing to fork. The three project forks (`AntiPaSTO`, `arena-sandbagging-mi`, `cross-model-alignment-geometry`) stay; no new forks will be created. | Your instruction "just the key repo" + "fork the single key repo needed to execute all the prompts" | If you meant a *different* repo, tell me which and I'll fork it. |
| 1.2 | Quick projects that would need a paid/closed API (OpenAI/Anthropic keys) will be **run anyway** and recorded as `api-key` failures rather than skipped. | The protocol says record the reason; running costs minutes and sometimes the API turns out to be optional. | Say "skip api-key projects" and I'll add them to `tree_done.txt`. |
| 1.3 | Automatic environment fixes are allowed: installing a missing Python package, `pip`/`jupyter` for notebooks, sanitising a Python version string. Never prompts, thresholds, datasets or metrics. | The replication ground rules (environment-only fixes). | — |
| 1.4 | Committing as we go: only the `replication/` folder of the meta repo, never your other uncommitted files at the repo root. | You have work in progress there (`meta.py`, `readme.md`, `summary.md`, `p3/`, …). | Say "commit everything" if you want those included. |

## 2. Things only you can do (none blocking right now)

- ✅ Hugging Face licences: Gemma (accepted 08‑26), Llama‑3.2 (accepted 08‑27). If a quick project needs another gated model, it will show up here with the exact link to click.

## 3. Step-by-step: how to read the scorecard yourself

1. Open `replication/ledger_summary.json` or run `python3 replication/ledger.py` — it prints "attempted N, installs N, runs N, reproduced N" and the failure taxonomy.
2. For any project, open `replication/experiments/<project>/ledger.json`. The fields that matter: `installs`, `runs`, `claim_reproduced`, `observed_value` vs `claimed_value`, `blocking_reason`, `env_fixes`, `notes`.
3. `run.log` in the same folder is the timeline; the `== VERDICT` block at its end is the one-paragraph judgement.
4. `handoff-N.md` files (technical) and this file (plain language) are the narrative.

---
