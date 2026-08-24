#!/usr/bin/env python3
"""
Recompute every [MEASURED] number in readme.md.

Usage:  python3 meta.py            # full report to stdout
        python3 meta.py > out.txt  # diff against a previous run to detect drift

Inputs (read-only, absolute paths -- edit SRC if you relocate the corpora):
  ~/alignment-forum-scrape/projects.json                          253 records
  ~/scrape-lesswrong/lesswrong_empirical_ai_safety_projects.json  637 records
  ~/neel-nandas-chris-olah/manifest.json                          101 records

This script builds nothing and mutates nothing. It is the warrant for readme.md.
If you disagree with a claim in readme.md, modify this script, not the prose.
"""
import json, re, collections, hashlib, statistics as st, os

HOME = os.path.expanduser("~")
SRC = {
    "AF":   f"{HOME}/alignment-forum-scrape/projects.json",
    "LW":   f"{HOME}/scrape-lesswrong/lesswrong_empirical_ai_safety_projects.json",
    "NNCO": f"{HOME}/neel-nandas-chris-olah/manifest.json",
}

AF = json.load(open(SRC["AF"]))
LW = json.load(open(SRC["LW"]))
NN = json.load(open(SRC["NNCO"]))

POST_ID = re.compile(r"/posts/([A-Za-z0-9]+)/")
GH      = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


def pid(url):
    m = POST_ID.search(url or "")
    return m.group(1) if m else None


def repo(url):
    """Normalised owner/name, lowercased, for cross-corpus repo identity."""
    if not url:
        return None
    m = GH.search(url)
    if not m:
        return None
    return f"{m.group(1)}/{m.group(2)}".lower().rstrip("/").removesuffix(".git")


for r in AF:
    r["_pid"] = pid(r["url"])
for r in LW:
    r["_pid"] = r["_id"]

AFP = {r["_pid"]: r for r in AF}
LWP = {r["_pid"]: r for r in LW}
BOTH   = set(AFP) & set(LWP)
AFONLY = set(AFP) - set(LWP)
LWONLY = set(LWP) - set(AFP)

# Union: LW record wins on collision (superset schema); AF fills the gaps.
UNION = {}
for r in LW:
    UNION[r["_pid"]] = dict(r, _src="LW")
for r in AF:
    UNION.setdefault(r["_pid"], dict(r, _src="AF"))
V = list(UNION.values())


def h(s):
    return hashlib.md5((s or "").encode()).hexdigest()


def half(d):
    y, m = int(d[:4]), int(d[5:7])
    return f"{y}H{1 if m <= 6 else 2}"


PERIODS = ["2024H2", "2025H1", "2025H2", "2026H1", "2026H2"]

# ---------------------------------------------------------------- instruments
# One instrument, applied identically to every corpus. Divergence from the
# source readmes' numbers is an instrument effect, not a population effect.
RIGOR = {
    "seeds_loose":  r"\b(random seed|seeds?\b|across \d+ seeds|seed variance)\b",
    "seeds_strict": r"\b(random seeds?|\d+ seeds|seed variance|across seeds|per-seed|seed-to-seed)\b",
    "errorbar":     r"\b(error bars?|confidence intervals?|standard error|95% ci|stderr|s\.e\.m)\b|±",
    "sig_test":     r"\b(p\s*[<=]\s*0?\.\d|p-value|t-test|mann-whitney|bootstrap|chi-squared|wilcoxon)\b",
    "n_equals":     r"\bn\s*=\s*\d+",
    "ablation":     r"\bablat",
    "baseline":     r"\bbaselines?\b",
    "prereg":       r"\b(pre-?regist)",
    "heldout":      r"\b(held[- ]out|test split|validation set)\b",
    "arxiv":        r"arxiv\.org",
    "limitations":  r"\b(limitations?|caveats?)\b",
    "neg_result":   r"\b(negative results?|did not (?:work|replicate)|failed to (?:find|replicate)|no (?:significant )?effect)\b",
    "multi_model":  r"\b(across (?:several|multiple|\d+) models|model families)\b",
}
TOPIC = {
    "SAE":          r"\b(sparse autoencoder|SAEs?\b|dictionary learning|crosscoder)",
    "agents":       r"\b(agentic|agent scaffold|tool[- ]use|multi[- ]turn agent|AI agents?)\b",
    "reward_hack":  r"\b(reward hack|specification gaming|reward tamper)",
    "cot_monitor":  r"\b(chain[- ]of[- ]thought monitor|CoT monitor|monitorab|CoT faithful|faithfulness of (?:the )?chain)",
    "eval_aware":   r"\b(eval(?:uation)?[- ]aware|knows it(?:'|’)s being (?:tested|evaluated)|sandbagg|situational awareness)",
    "probes":       r"\b(linear probe|probing classifier|probe accuracy)",
    "emergent_mis": r"\b(emergent misalignment)",
    "align_fake":   r"\b(alignment fak)",
    "unlearning":   r"\bunlearn",
    "steering":     r"\b(steering vector|activation steering|activation addition)",
}


def prevalence(records, patterns):
    n = len(records) or 1
    out = {}
    for k, p in patterns.items():
        rx = re.compile(p, re.I)
        out[k] = round(100 * sum(1 for r in records if rx.search(r["article-content"] or "")) / n, 1)
    return out


def rule(t):
    print(f"\n{'=' * 78}\n{t}\n{'=' * 78}")


# ------------------------------------------------------------------ §1.1 sizes
rule("1.1  CORPUS SIZES AND THE JOIN")
print(f"AF   {len(AF):>4} records   unique post-ids {len(set(AFP)):>4}   id-extraction failures {sum(1 for r in AF if not r['_pid'])}")
print(f"LW   {len(LW):>4} records   unique post-ids {len(set(LWP)):>4}")
print(f"NNCO {len(NN):>4} records   (different unit: blog documents, no post-ids)")
print(f"\nAF n LW (shared post-id) : {len(BOTH)}")
print(f"AF only                  : {len(AFONLY)}   ({100*len(AFONLY)/len(AFP):.1f}% of AF)")
print(f"LW only                  : {len(LWONLY)}   ({100*len(LWONLY)/len(LWP):.1f}% of LW)")
print(f"UNION                    : {len(UNION)}")


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


aft = {norm_title(r["title"]) for r in AF}
lwt = {norm_title(r["title"]) for r in LW}
print(f"title-level overlap      : {len(aft & lwt)}  (title join and id join agree exactly: "
      f"{len(aft & lwt) == len(BOTH)})")

# --------------------------------------------------------- §1.4 O1 independence
rule("1.4/O1  ARE THE TWO CORPORA INDEPENDENT?  (agreement on the 149 shared posts)")
same_content = sum(1 for p in BOTH if h(AFP[p]["article-content"]) == h(LWP[p]["article-content"]))
same_readme  = sum(1 for p in BOTH if h(AFP[p]["github-readme"])   == h(LWP[p]["github-readme"]))
same_title   = sum(1 for p in BOTH if AFP[p]["title"]  == LWP[p]["title"])
same_author  = sum(1 for p in BOTH if AFP[p]["author"] == LWP[p]["author"])
same_karma   = sum(1 for p in BOTH if int(AFP[p]["karma"]) == int(LWP[p]["karma"]))
same_words   = sum(1 for p in BOTH if int(AFP[p]["word_count"]) == int(LWP[p]["word_count"]))
n = len(BOTH)
print(f"byte-identical article-content : {same_content}/{n}")
print(f"byte-identical github-readme   : {same_readme}/{n}")
print(f"identical title / author       : {same_title}/{n}  /  {same_author}/{n}")
print(f"identical karma / word_count   : {same_karma}/{n}  /  {same_words}/{n}")

agree_repo = agree_none = af_x = lw_x = disagree = 0
disagreements = []
for p in sorted(BOTH):
    a, l = repo(AFP[p]["github-link"]), repo(LWP[p]["github-link"])
    if a and l:
        if a == l:
            agree_repo += 1
        else:
            disagree += 1
            disagreements.append((AFP[p]["title"], a, l))
    elif a:
        af_x += 1
    elif l:
        lw_x += 1
    else:
        agree_none += 1
a1 = [1 if repo(AFP[p]["github-link"]) else 0 for p in sorted(BOTH)]
l1 = [1 if repo(LWP[p]["github-link"]) else 0 for p in sorted(BOTH)]
po = sum(x == y for x, y in zip(a1, l1)) / n
pa, pl = sum(a1) / n, sum(l1) / n
pe = pa * pl + (1 - pa) * (1 - pl)
print(f"\nrepo adjudication: same repo {agree_repo} | both null {agree_none} | "
      f"AF-only {af_x} | LW-only {lw_x} | different {disagree}")
print(f"binary has-repo Cohen's kappa  : {(po - pe) / (1 - pe):.4f}   (AF rate {pa:.3f}, LW rate {pl:.3f})")
for t, a, l in disagreements:
    print(f"  DISAGREEMENT: {t[:58]}\n                AF={a}\n                LW={l}")

# ------------------------------------------------------- §1.3b prestige strata
rule("1.3b  PRESTIGE STRATIFICATION  (AF promotion as the stratifier)")
strata = [("AF-only", [AFP[p] for p in AFONLY]),
          ("shared",  [AFP[p] for p in BOTH]),
          ("LW-only", [LWP[p] for p in LWONLY])]
print(f"{'stratum':9} {'n':>4} {'med karma':>10} {'mean karma':>11} {'repo%':>7} {'readme%':>8} "
      f"{'solo%':>6} {'7+auth':>7} {'mean auth':>10} {'med words':>10}")
for lbl, rs in strata:
    k = [int(r["karma"]) for r in rs]
    w = [int(r["word_count"]) for r in rs]
    au = [len(re.split(r",\s*", r["author"])) for r in rs]
    solo = sum(1 for r in rs if "," not in (r["author"] or ""))
    print(f"{lbl:9} {len(rs):>4} {st.median(k):>10.1f} {st.mean(k):>11.1f} "
          f"{100*sum(1 for r in rs if r['github-link'])/len(rs):>6.1f}% "
          f"{100*sum(1 for r in rs if r['github-readme'])/len(rs):>7.1f}% "
          f"{100*solo/len(rs):>5.0f}% "
          f"{sum(1 for a in au if a >= 7):>7} {st.mean(au):>10.2f} {st.median(w):>10.0f}")

# ------------------------------------------------------ §1.3d coverage over time
rule("1.3d  AF-IN-LW COVERAGE BY HALF-YEAR  (recall of the LW pipeline against a known in-scope set)")
ca = collections.Counter(half(AFP[p]["date"]) for p in AFP)
cl = collections.Counter(half(LWP[p]["date"]) for p in LWP)
cb = collections.Counter(half(AFP[p]["date"]) for p in BOTH)
print(f"{'period':8} {'AF n':>5} {'LW n':>5} {'shared':>7} {'AF captured by LW':>19}")
for p in PERIODS:
    cov = f"{100*cb[p]/ca[p]:.0f}%" if ca[p] else "-"
    print(f"{p:8} {ca[p]:>5} {cl[p]:>5} {cb[p]:>7} {cov:>19}")

print("\nAF posts missed by the LW pipeline, top 15 by karma:")
for p in sorted(AFONLY, key=lambda p: -int(AFP[p]["karma"]))[:15]:
    r = AFP[p]
    print(f"  {r['karma']:>4}  {r['date']}  {r['title'][:60]:60} [{r['project_type']}]")
print(f"\n  of the {len(AFONLY)} missed: {sum(1 for p in AFONLY if int(AFP[p]['word_count'])<1000)} are <1000 words, "
      f"{sum(1 for p in AFONLY if int(AFP[p]['karma'])>100)} are >100 karma, "
      f"{sum(1 for p in AFONLY if ',' not in AFP[p]['author'])} are single-author")

# ------------------------------------------------ §1.3c one instrument, all corpora
rule("1.3c  ONE INSTRUMENT APPLIED TO EVERY STRATUM  (rigor markers, % of posts)")
cols = [("AF-only", [AFP[p] for p in AFONLY]), ("shared", [AFP[p] for p in BOTH]),
        ("LW-only", [LWP[p] for p in LWONLY]), ("AF all", AF), ("LW all", LW), ("UNION", V)]
scores = [(lbl, prevalence(rs, RIGOR)) for lbl, rs in cols]
print(f"{'marker':14}" + "".join(f"{lbl:>9}" for lbl, _ in scores))
for k in RIGOR:
    print(f"{k:14}" + "".join(f"{s[k]:>9}" for _, s in scores))
print("\nsource-readme claims for comparison:")
print("  AF readme: seeds/variance 5.9 | stat test or interval 19.4 | limitations 43.9 | arxiv 84.2 | negative 9.9 | multi-model 18.2")
print("  LW readme: seeds 17 | error bars 16 | n= 13 | prereg 2 | ablation 24 | baseline 52 | held-out 20 | arxiv 72")

# ------------------------------------------------------------- topic trends
rule("1.3e  TOPIC PREVALENCE BY HALF-YEAR, ONE INSTRUMENT (% of posts in period)")
for lbl, rs in [("UNION", V), ("AF subset", AF), ("LW subset", LW)]:
    g = collections.defaultdict(list)
    for r in rs:
        g[half(r["date"])].append(r)
    print(f"\n-- {lbl}  n: " + "  ".join(f"{p}={len(g[p])}" for p in PERIODS))
    print(f"{'topic':14}" + "".join(f"{p:>9}" for p in PERIODS))
    for k, pat in TOPIC.items():
        rx = re.compile(pat, re.I)
        row = []
        for p in PERIODS:
            sub = g[p]
            row.append(f"{100*sum(1 for r in sub if rx.search(r['article-content'] or ''))/len(sub):.0f}%" if sub else "-")
        print(f"{k:14}" + "".join(f"{x:>9}" for x in row))

# --------------------------------------------------------- artifact layer
rule("1.3f  THE ARTIFACT LAYER AND THE INVISIBLE DEPENDENCY LAYER")
for lbl, rs in [("AF", AF), ("LW", LW), ("UNION", V)]:
    mention = [r for r in rs if GH.search(r["article-content"] or "")]
    null_m = [r for r in mention if not r["github-link"]]
    print(f"{lbl:6} n={len(rs):>3}  mention github {len(mention):>3} ({100*len(mention)/len(rs):.0f}%)  "
          f"assigned own-repo {sum(1 for r in rs if r['github-link']):>3}  "
          f"mentions-but-null {len(null_m):>3} ({100*len(null_m)/len(mention):.0f}% of mentioners discarded)")

ra = collections.Counter(filter(None, (repo(r["github-link"]) for r in AF)))
rl = collections.Counter(filter(None, (repo(r["github-link"]) for r in LW)))
print(f"\ndistinct own-project repos: AF {len(ra)}  LW {len(rl)}  shared {len(set(ra)&set(rl))}  union {len(set(ra)|set(rl))}")
print(f"repos claimed by >1 union post: {sorted([k for k in set(ra)|set(rl) if ra[k]+rl[k] > 2])}")

cited = collections.Counter()
for r in V:
    for o, rp in set(GH.findall(r["article-content"] or "")):
        cited[f"{o}/{rp}".lower()] += 1
own = set(ra) | set(rl)
print("\nmost-cited repos across the union (distinct posts citing; * = never an own-project repo):")
for k, c in cited.most_common(18):
    print(f"  {c:>3}  {k}{'' if k in own else '  *'}")

# ------------------------------------------------------------- NNCO frame
rule("1.4/O3  THE NNCO SAMPLING FRAME AGAINST THE OTHER TWO CORPORA")
print(f"NNCO records {len(NN)}  technical {sum(1 for r in NN if r['technical'])}")
print("by author:", dict(collections.Counter(r["author"] for r in NN)))
print("technical by author:", dict(collections.Counter(r["author"] for r in NN if r["technical"])))
print("domains:", dict(collections.Counter(re.sub(r"^https?://", "", r["url"]).split("/")[0] for r in NN)))
nn_words = sum(int(r["words"]) for r in NN if r["author"] == "Neel Nanda" and r["technical"])
ol_words = sum(int(r["words"]) for r in NN if r["author"] == "Chris Olah" and r["technical"])
print(f"technical words: Nanda {nn_words:,}  Olah {ol_words:,}")

nanda = [r for r in V if "neel nanda" in (r["author"] or "").lower()]
print(f"\nNeel Nanda in AF u LW : {len(nanda)} posts, {sum(int(r['word_count']) for r in nanda):,} words, "
      f"{min(r['date'] for r in nanda)} -> {max(r['date'] for r in nanda)}")
print(f"  as first author     : {sum(1 for r in nanda if (r['author'] or '').split(',')[0].strip() == 'Neel Nanda')}")
print(f"  with own repo       : {sum(1 for r in nanda if r['github-link'])}")
tot = nn_words + sum(int(r["word_count"]) for r in nanda)
print(f"  NNCO captures {100*nn_words/tot:.0f}% of Nanda's available technical words")
un_titles = {norm_title(r["title"]) for r in V}
print(f"  NNCO titles also present in AF u LW: {sum(1 for r in NN if norm_title(r['title']) in un_titles)}")
print(f"  NNCO records hosted on lesswrong/alignmentforum: "
      f"{sum(1 for r in NN if 'lesswrong' in r['url'] or 'alignmentforum' in r['url'])}")

# --------------------------------------------------------------- union shape
rule("1.2  UNION AGGREGATES")
allA, firstA = collections.Counter(), collections.Counter()
for r in V:
    parts = [a.strip() for a in re.split(r",\s*", r["author"] or "") if a.strip()]
    if parts:
        firstA[parts[0]] += 1
    for a in parts:
        allA[a] += 1
ks = [int(r["karma"]) for r in V]
ws = [int(r["word_count"]) for r in V]
print(f"posts {len(V)}  words {sum(ws):,}  median words {st.median(ws):.0f}")
print(f"karma median {st.median(ks):.0f}  mean {st.mean(ks):.1f}  min {min(ks)}  max {max(ks)}")
print(f"with own repo {sum(1 for r in V if r['github-link'])} ({100*sum(1 for r in V if r['github-link'])/len(V):.1f}%)  "
      f"with README {sum(1 for r in V if r['github-readme'])}")
print(f"distinct authors {len(allA)}  distinct first authors {len(firstA)}  "
      f"single-author posts {sum(1 for r in V if ',' not in (r['author'] or ''))} "
      f"({100*sum(1 for r in V if ',' not in (r['author'] or ''))/len(V):.0f}%)")
print(f"authors appearing exactly once {sum(1 for c in allA.values() if c == 1)} "
      f"({100*sum(1 for c in allA.values() if c == 1)/len(allA):.0f}%)")
print(f"top-20 authors hold {100*sum(c for _, c in allA.most_common(20))/sum(allA.values()):.0f}% "
      f"of {sum(allA.values())} author-slots")
print("top 15 by author-slots:", allA.most_common(15))

print("\ntop 12 union posts by karma:")
for r in sorted(V, key=lambda r: -int(r["karma"]))[:12]:
    tag = "AF+LW" if r["_pid"] in BOTH else r["_src"]
    print(f"  {r['karma']:>4} {r['date']} [{tag:>5}] repo={'Y' if r['github-link'] else 'n'} {r['title'][:60]}")

# ---------------------------------------------------------- label hygiene
rule("1.4/O9  LABEL HYGIENE")
raw = collections.Counter(r["project_type"] for r in AF)
print(f"AF project_type: {len(raw)} raw labels in the JSON, 7 rows in the AF readme table")
for k, c in raw.most_common():
    print(f"  {c:>3}  {k}")
print("\nLW confidence:", dict(collections.Counter(r["confidence"] for r in LW)))
print("LW confidence x in-AF:", dict(collections.Counter((r["confidence"], r["_pid"] in BOTH) for r in LW)))
print("LW github_readme_status:", dict(collections.Counter(r["github_readme_status"] for r in LW)))

# ---------------------------------------------------------- near-duplicates
rule("1.4/O7  NEAR-DUPLICATE POSTS IN THE UNION")
def toks(t):
    return {w for w in re.findall(r"[a-z]+", (t or "").lower()) if len(w) > 4}
index = collections.defaultdict(list)
for r in V:
    for w in toks(r["title"]):
        index[w].append(r)
seen, dups = set(), []
for w, rs in index.items():
    if len(rs) > 12:
        continue
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            a, b = rs[i], rs[j]
            key = tuple(sorted((a["_pid"], b["_pid"])))
            if key in seen:
                continue
            seen.add(key)
            ta, tb = toks(a["title"]), toks(b["title"])
            if len(ta | tb) and len(ta & tb) / len(ta | tb) >= 0.6 \
               and a["author"].split(",")[0] == b["author"].split(",")[0]:
                dups.append((round(len(ta & tb) / len(ta | tb), 2), a["date"], b["date"],
                             a["title"][:52], b["title"][:52]))
for d in sorted(dups, reverse=True):
    print("  ", d)
print(f"  total near-duplicate pairs (same first author, Jaccard >= 0.6): {len(dups)}")
