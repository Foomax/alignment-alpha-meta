#!/usr/bin/env bash
# Publish one experiment to its fork under github.com/Foomax.
#   publish.sh <slug> ["commit message"]
# What it does (idempotent):
#   1. ensures Foomax/<repo> exists (gh repo fork --clone=false)
#   2. in experiments/<slug>/src: origin -> the fork, upstream -> the authors' repo; branch replication-3090
#      created from the pinned SHA (never touches upstream, never opens PRs/issues)
#   3. copies the experiment folder's small artefacts into src/replication/ (no weights, venvs, caches,
#      big parquet); adds a .gitignore for outputs
#   4. writes README.md with "# human" and "# LLM" sections. The upstream README is preserved as
#      README.upstream.md. Body text comes from experiments/<slug>/README.human.md and README.llm.md if
#      present; otherwise a template is generated from spec.json + ledger.json.
#   5. commits everything and pushes the branch to the fork.
set -euo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; slug="$1"; msg="${2:-replication update $(date -Is)}"
EXP="$REP/experiments/$slug"; SRC="$EXP/src"
[ -d "$SRC/.git" ] || { echo "no src checkout for $slug"; exit 2; }
repo=$(python3 -c "import json;print(json.load(open('$EXP/spec.json'))['repo'])"); name=${repo#*/}
sha=$(python3 -c "import json;print(json.load(open('$EXP/spec.json'))['head_sha'])")
fork="https://github.com/Foomax/$name.git"

gh repo view "Foomax/$name" --json name -q .name >/dev/null 2>&1 || gh repo fork "$repo" --clone=false >/dev/null
cd "$SRC"
if ! git remote get-url upstream >/dev/null 2>&1; then git remote rename origin upstream; fi
git remote get-url origin >/dev/null 2>&1 && git remote set-url origin "$fork" || git remote add origin "$fork"
git rev-parse --verify replication-3090 >/dev/null 2>&1 && git checkout -q replication-3090 || git checkout -q -b replication-3090 "$sha"

# 3. artefacts
mkdir -p replication
rsync -a --delete --exclude 'src/' --exclude '.venv/' --exclude '__pycache__/' --exclude '*.safetensors' --exclude '*.pt' \
      --exclude 'node.out' --exclude '.vram.pid' --exclude '.gpu_started' --exclude 'README.human.md' --exclude 'README.llm.md' \
      --max-size=20m "$EXP/" replication/
cat > .gitignore.replication <<'EOF'
# added by the replication fork: never commit weights, venvs, caches, model dumps
.venv/
outputs/**/*.safetensors
outputs/**/*.pt
outputs/**/*.bin
outputs/**/2_eval_labelled*.parquet
outputs/**/activations/
**/__pycache__/
*.egg-info/
EOF
grep -qxF '.venv/' .gitignore 2>/dev/null || cat .gitignore.replication >> .gitignore
rm -f .gitignore.replication

# 4. README
[ -f README.upstream.md ] || { [ -f README.md ] && git mv -k README.md README.upstream.md 2>/dev/null || cp README.md README.upstream.md 2>/dev/null || true; }
python3 - "$EXP" "$repo" "$sha" > README.md <<'PY'
import json, os, sys
exp, repo, sha = sys.argv[1:4]
spec = json.load(open(f"{exp}/spec.json"))
led = json.load(open(f"{exp}/ledger.json")) if os.path.exists(f"{exp}/ledger.json") else None
def rd(p): return open(p).read().strip() if os.path.exists(p) else None
human, llm = rd(f"{exp}/README.human.md"), rd(f"{exp}/README.llm.md")
print(f"# Replication fork of `{repo}` — {spec.get('title','')}\n")
print(f"This is a fork made for an independent replication on one RTX 3090. Branch `replication-3090` starts at the authors' commit `{sha[:7]}` (pinned; `upstream` remote = the original repo). Nothing here is a contribution to the original project — no PRs, no issues; the authors' README is preserved as `README.upstream.md`. Everything we added lives in `replication/` plus the minimal environment fixes recorded below.\n")
print("# human\n")
if human: print(human)
else:
    print(f"**Claim being checked:** {spec.get('primary_claim','(see spec.json)')}\n")
    if led:
        st = "reproduced" if led.get("claim_reproduced") else ("did NOT reproduce" if led.get("claim_located") else "could not be tested")
        print(f"**What happened:** it installed ({'yes' if led['installs'] else 'no'}), it ran ({'yes' if led['runs'] else 'no'}), and the claim **{st}**. Observed: `{led.get('observed_value')}` vs claimed `{led.get('claimed_value')}`. Blocking reason: `{led.get('blocking_reason')}`. Wall-clock {led.get('wallclock_minutes')} min.\n")
        if led.get("env_fixes"): print("**Things we had to fix to make it run (environment only, never the measurement):**\n" + "\n".join(f"- {f}" for f in led["env_fixes"]) + "\n")
        if led.get("notes"): print("**Notes:** " + led["notes"] + "\n")
    else:
        print("**Status:** queued / running — this section is filled in when the run finishes.\n")
print("# LLM\n")
if llm: print(llm)
else:
    print("Machine-oriented summary for an agent continuing this work.\n")
    print(f"- spec: `replication/spec.json` (post `{spec.get('post_id')}`, repo `{repo}`, pinned `{sha}`, entrypoint `{spec.get('entrypoint')}`, budget {spec.get('budget_minutes')} min, tolerance `{spec.get('tolerance')}`, target `{spec.get('target_value')}`)")
    print("- protocol: `replication/PROMPT.md` (ground rules: pin the commit; one venv per experiment; environment fixes only; no closed-model APIs; time-box; [MEASURED]/[INFERRED]/[UNRESOLVED]; never push to upstream)")
    print("- artefacts: `replication/run.log` (timeline, `== VERDICT` at the end when done), `replication/ledger.json` (the formal entry written by `replication/report.py`), any `replication/*.md` reports and `replication/followups/`")
    if led: print(f"- ledger: installs={led['installs']} runs={led['runs']} claim_located={led['claim_located']} claim_reproduced={led['claim_reproduced']} observed={led.get('observed_value')!r} delta={led.get('delta')} reason={led.get('blocking_reason')} seeds={led.get('seeds_run')} wallclock={led.get('wallclock_minutes')} peak_vram_gb={led.get('peak_vram_gb')}")
    print("- to re-run: follow `replication/PROMPT.md` from a fresh venv; apply the env fixes listed in the ledger first.")
PY

# 5. commit + push
git add -A
if git diff --cached --quiet; then echo "nothing to commit for $slug"; else git commit -q -m "$msg" -m "Replication fork under Foomax; upstream untouched. Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"; fi
git push -q -u origin replication-3090 2>&1 | tail -1 || true
echo "published $slug -> $fork (replication-3090 @ $(git rev-parse --short HEAD))"
