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

## 4. Quick project #1 (`ioi`, GPT‑2 small) — reproduced exactly (07:35)

**What it claims.** A famous "circuit" in GPT‑2 small handles sentences like "When Mary and John went to the store, John gave a drink to ___" (answer: Mary). The post adds a stray extra "Mary" somewhere irrelevant and asks whether the circuit gets confused. Answer: only slightly — the model's preference for the right name drops by 0.23 on its internal scale, and accuracy goes 95.4 % → 94.5 %.

**What we got.** 0.231, 95.3 % → 94.5 %, same statistics to the third decimal. The model is deterministic, so this is the "boring good" outcome: a well‑written notebook that does what it says.

**What needed fixing (nothing scientific).** The repo has no list of required packages, and notebooks run in a fresh sandbox don't have `pip`. The runner now installs those automatically; the first two attempts died on that, the third ran in 3 minutes.

**Needs you?** No.

## 5. Project 01 ("do model families think alike?") — reproduced (14:30)

**What it claims.** Same‑family models look alike inside (0.91), different families barely (≈0.2).

**What we got.** 0.914 for the same‑family pair, 0.208 and 0.222 for the two cross‑family pairs we ran — identical to the post to three decimals. Two of the five pairs weren't run: each pair took ~100 minutes (my estimate was 15 — the similarity statistics, not the model runs, are the slow part) and the protocol's 4‑hour budget ran out. The protocol says the three we ran are enough to test the claim.

**Needs you?** No. If you ever want the last two pairs, it's ~3.5 hours of GPU with everything already downloaded.

## 6. The quick‑project queue is noisy by design (14:30)

Of the first 13 quick projects, 3 ran and 10 failed within seconds. Nearly all failures are *plumbing*: the catalogue's "entrypoint" is sometimes a description ("run `python -m replicate run-fast`…") that the generic runner tries to execute literally; some repos list no dependencies; one needs a package from the author's own GitHub rather than PyPI; one needs 90 minutes, not 45. I'm queuing a second pass with the correct invocation for each. Expect the scorecard to look bad *before* that pass and better after it — the taxonomy records both.

**Needs you?** Not yet. Two projects will likely end as "can't run without external stuff": one expects pre‑generated model completions and a Weights & Biases artifact; one notebook looked like it had a typo (`true` instead of `True`) — on closer inspection it was my runner feeding the notebook file to Python as if it were a script; it's being re-run properly.

## 7. Quick project `quotesbyniche` (ameya-bit, "an induction head in disguise") — reproduced exactly (14:50)

A tiny character‑level model trained on Nietzsche; the post says one attention head is a "copying" head (score 0.615, everyone else ≤ 0.35) whose weights also nudge `)` after `(`. We got 0.615, 0.347 and the same bracket nudges (+0.556 / −0.105). Nothing needed fixing. **Needs you?** No.
