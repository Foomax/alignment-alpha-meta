# Handoff summary — read this first

Written for a fresh Claude instance picking up this work cold. Date of writing: 2026-08-25.

---

## 1. What this repo is

`/home/user/alignment-literature-meta-analysis` — a meta-analysis of three previously-built
empirical-AI-safety corpora. Published on GitHub as **`Foomax/alignment-alpha-meta`**
(public, remote `origin` already configured).

The user's original phrasing for the project name was "aligmnent-alpha-meta"; they confirmed the
typo fix to `alignment-alpha-meta` before the repo was created. Default branch is **`master`**,
not `main` — this was a deliberate choice to keep the local git default, and the user was told.

### Git state

```
4f01622  Meta-analysis of AF / LessWrong / Olah-Nanda corpora     <- HEAD, NOT PUSHED
096cac0  Initial commit. This repo aims to be a meta-analysis of all online empirical AI Safety work.
```

**Commit `096cac0` is pushed. `4f01622` is not.** The user was offered a push and had not
answered at the time of writing. Do not push without asking — but the remote exists and
`git push` alone will work.

Commit trailers used in this repo (match them):

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01We54RPReJX7KfEJtKuz7Wk
```

Git identity is passed per-commit (`git -c user.name="Foomax" -c user.email="hi2foomax@gmail.com" commit ...`)
because the repo has no local identity configured.

### Files

| File | What it is |
|---|---|
| `readme.md` | **The deliverable.** 51 KB. Section 1 analysis, Section 2 synthesis + 12 research specs. Written for LLM consumption. |
| `meta.py` | 18 KB. Recomputes every `[MEASURED]` number in `readme.md`. `python3 meta.py` prints a 234-line report. Read-only w.r.t. the source corpora. |
| `summary.md` | This file. |

---

## 2. The task as given

> open ~/alignment-forum-scrape and ~/scrape-lesswrong and neel-nandas-chris-olah, in particular
> the readme.md in each. Find common features in the document, patterns in the differences, and
> OUTLIERS. Brainstorm further research ideas for an LLM to execute. Our goal is to write a
> document readable by other LLMs: readme.md. For the .json — Section 1. An analysis … Section 2.
> A synthesis & a brainstorm … using max thinking tokens, write further research recommendations —
> again, written for LLMs.

Interpretation applied: Section 1 analyses **both** the three readmes and the three `.json`
artifacts they describe; Section 2 is synthesis plus executable research specs. Output went to
`readme.md` in this repo (not to the source directories).

---

## 3. The three source corpora (read-only inputs)

| Path | Corpus | n | Primary artifact | Their readme |
|---|---|---|---|---|
| `~/alignment-forum-scrape/` | **AF** — Alignment Forum empirical projects, 2024-08 → 2026-08 | 253 | `projects.json` (8.4 MB) | 26 KB |
| `~/scrape-lesswrong/` | **LW** — LessWrong empirical projects, same window | 637 | `lesswrong_empirical_ai_safety_projects.json` (19.1 MB) | 31 KB |
| `~/neel-nandas-chris-olah/` | **NNCO** — Olah + Nanda blog corpus | 101 (40 technical) | `manifest.json` + `analysis/` | 46 KB (+ `readme.chatgpt.md`, 29 KB, a predecessor it retracts) |

Each also ships an `articles/` (or `posts/`) directory of one Markdown file per record. The three
readmes total ~133 KB; reading all three costs roughly 35k tokens. **Do that** if you are going to
argue with anything in `readme.md` — the analysis is dense in cross-references to their section
numbers.

Nothing in those three directories was modified. This work is purely additive.

---

## 4. What was found (short version)

All numbers are `[MEASURED]` and reproduced by `python3 meta.py`.

1. **AF and LW overlap on 149 posts.** Exact join: AF's `url` field contains the LessWrong post id
   (both forums run on the same ForumMagnum DB). The id join and a normalised-title join agree at
   exactly 149. Union = **741 posts, 1,972,389 words, 896 authors, 376 with an own-project repo**.
   Neither source readme mentions the other corpus.
2. **The two corpora are not independent — this is the headline.** On the 149 shared posts:
   `article-content` byte-identical **149/149**, `github-readme` 148/149, karma and `word_count`
   identical 149/149, repo adjudication **Cohen's κ = 1.0000** (69 same-repo, 79 both-null, 0
   one-sided, 1 disagreement). JSON mtimes are 17 minutes apart. Conclusion: sibling outputs of
   one pipeline, not two independent scrapes. Their agreement measures determinism, not
   reliability.
3. **The rigor gap between the two readmes is an instrument artifact.** AF reports 5.9%
   seed-reporting, LW reports 17%, on overlapping populations. One instrument gives ~6% strict /
   ~15% loose on both. Negative-result rate (10.1%) and multi-model rate (9.2%) are flat across
   every stratum.
4. **LW's recall decays 76% → 63% → 55% → 48% → 50%** by half-year against a set already known to
   be in scope (the AF corpus). Every published trend claim is confounded with this. The misses
   include 5 of AF's own top 9 posts by karma — i.e. the tag filter systematically loses
   frontier-lab and org-branded posts, not the "short, informal posts" LW's readme predicts.
5. **AF promotion behaves like a treatment.** AF-only vs LW-only: median karma 61.5 vs 18.0, mean
   team size 3.13 vs 1.80, code release **39.4% vs 54.3%**, and no rigor gain on any of 13 markers.
6. **The reuse layer is the discarded one.** 5 of the 7 most-cited repos in the union are never an
   own-project repo (`control-arena` 10, `saelens` 7, `llm-attacks` 6, `transformerlens` 5,
   `tuned-lens` 5). Only 14 of 359 own-project repos are claimed by >1 union post.
7. **NNCO has the same sampling-frame defect it warns about, on the other author.** Its Fact 1
   flags that Olah's corpus is `colah.github.io` truncated at 2015. It does not flag that its
   Nanda corpus is `neelnanda.io` only — omitting **52 AF/LW posts, 171,776 words, zero title
   overlap**, i.e. capturing 34% of his available technical words. The missing data is one
   directory away.

Section 2 of `readme.md` turns these into 7 synthesis claims (M1–M7) and **12 research specs
(R1–R12)**, each with inputs, method, falsifiable success criterion, and what a negative result
would mean. R1 (build `union.json`) gates most of the others; §2.3 gives an execution order.

---

## 5. Known limitations of the current work

State these if asked; do not quietly drop them.

- **The instrument is regex.** `readme.md` §1.3(c) criticises the source readmes for
  instrument-dependent rigor rates, and its own numbers have the same exposure. R3 in §2.2 is the
  LLM-judge validation that would price it. This is stated in the document, in §0.1 and in the
  closing instructions.
- **No LLM classification was performed here.** Where AF's `project_type` or LW's `topic` /
  `confidence` are used, they are used as-is and labelled as the source pipeline's judgment.
- **The non-independence finding (O1) is inference from evidence, not from provenance records.**
  Byte-identical text + κ=1.0 + 17-minute mtime gap is very strong, but no build log was found.
  If the user knows how the two corpora were built, that would confirm or kill it outright — worth
  asking.
- **The AF↔LW asymmetry is one-directional.** AF ⊂ LW-eligible by construction, so the 104
  AF-only posts are provably LW-pipeline misses. The 488 LW-only posts are *not* provably AF
  misses — they may simply never have been promoted. Do not state that symmetrically.
- **`readme.md` has not been reviewed by the user** beyond the summary given in chat.

---

## 6. Suggested next actions

Roughly in order of value. Items 1–2 are administrative; 3+ are the actual research.

1. **Ask about pushing `4f01622`.** One command: `git push`.
2. **Consider publishing `readme.md` as an Artifact** if the user wants a shareable link — it was
   not offered, and the document is long enough that a rendered page would help. Load the
   `artifact-design` skill first if you do.
3. **Execute R1 — build `union.json`.** Hours of work, gates almost everything else, and
   `meta.py` already contains the join (`pid()`, the `UNION` dict). Deliverable spec is in
   `readme.md` §2.2 R1: 741 records, LW schema as superset, `in_af`/`in_lw` booleans, the shipped
   `project_type` normalisation table (see O8 — the mapping is derived and verified but was found
   by arithmetic, not documented by AF), and `dup_cluster_id`.
4. **Resolve outlier O2 by hand.** One post — *Steganography via internal activations is already
   possible in small language models* — gets `Endauvor/SAE-evolution-method` from AF and
   `Lucid-Layers-Inc/Vector-SFT` from LW. It is the only disagreement in an otherwise deterministic
   set, so whichever is wrong reveals the adjudicator's failure mode. Cheap and high-signal.
5. **R9 — orphaned-lead mining.** Inference-only over the 741 `article-content` fields; scopes
   every other project and will surface leads this analysis missed. §2.2 R9 has the spec.
6. **R3 + R4** — validated instrument, then coverage-corrected trends. Together they decide which
   claims from the three source readmes survive at all. Do not build on those claims first.

---

## 7. Practical notes for the next instance

- **Scratchpad from this session** (intermediate scripts `meta2.py`…`meta9.py`, and the full
  234-line report): `/tmp/claude-1000/-home-user-alignment-literature-meta-analysis/ff252e2c-a230-4af6-a4bc-910bb11c0200/scratchpad/`.
  Session-specific and may be gone; `meta.py` supersedes all of it.
- **`meta.py` is the warrant.** If you disagree with a number in `readme.md`, change the script,
  not the prose — that convention is stated in the document and inherited from the NNCO readme.
  Re-run it and diff against a saved report to detect drift.
- **Do not re-run the source scrapes** to "refresh" karma. Karma is an age-confounded snapshot in
  both corpora and several comparisons in `readme.md` depend on both corpora sharing one snapshot.
  A partial re-scrape would break the 149/149 identity that O1 rests on.
- **The user's global CLAUDE.md pre-approves subagents** for fan-out work (per-item analysis
  across many independent items) and says not to ask permission. This particular task was done
  inline because the cross-corpus join needs everything in one context; R5 (the Replication
  Ledger, 359 repos) is the natural place to fan out.
- **Tone convention in `readme.md`:** claims are tiered `[MEASURED]` / `[INFERRED]` /
  `[SPECULATIVE]` / `[UNRESOLVED]`, and several `[SPECULATIVE]` predictions are deliberately
  framed so that falsification is the more informative outcome. Preserve that framing if you
  extend or summarise the document.
