#!/usr/bin/env bash
# Minute-class execution queue (experiment 01 is run separately via its run01.sh).
# For each slug in tree_minute_class.txt (skipping those listed in tree_done.txt):
#   1. env prep (environment-only, replicates run.sh's install block with a sanitised Python version):
#      uv venv --python X.Y ; pip/setuptools/wheel ; torch (cu124 index) ; requirements*.txt ; pyproject -e ;
#      for .ipynb entrypoints also jupyter nbconvert ipykernel matplotlib ipympl
#   2. run.sh (sees the venv, only runs the entrypoint with the spec's timeout)
#   3. auto-fix loop (max 3): missing modules reported in the logs are installed and run.sh re-run.
#      Every auto-fix is appended to <exp>/autofixes.txt for the ledger.
# One GPU job at a time (nvidia-smi python-process check). One line per finished node -> tree.log.
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; EXPS="$REP/experiments"; LOG="$REP/tree.log"; DONE="$REP/tree_done.txt"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python'; }
sleep "${TREE_INITIAL_SLEEP:-180}"

prep_env() { # dir -> creates .venv and installs deps; logs to <dir>/prep.log; returns 0/1
  local d="$1" spec="$1/spec.json" src="$1/src" venv="$1/.venv" plog="$1/prep.log"
  local repo sha py entry
  repo=$(python3 -c "import json;print(json.load(open('$spec'))['repo'])")
  sha=$(python3 -c "import json;print(json.load(open('$spec'))['head_sha'])")
  py=$(python3 -c "import json,re;v=str(json.load(open('$spec')).get('python_version') or '');m=re.search(r'(3\.\d+)',v);print(m.group(1) if m else '3.11')")
  entry=$(python3 -c "import json;print(json.load(open('$spec')).get('entrypoint') or '')")
  { echo "== prep $(date -Is) repo=$repo sha=$sha py=$py"
    if [ ! -d "$src/.git" ]; then git clone -q "https://github.com/$repo" "$src" && git -C "$src" checkout -q "$sha" || { echo "CLONE-FAILED"; return 1; }; fi
    if [ ! -x "$venv/bin/python" ]; then
      uv venv -q "$venv" --python "$py" || uv venv -q "$venv" --python 3.11 || { echo "VENV-FAILED"; return 1; }
    fi
    uv pip install -q --python "$venv/bin/python" pip setuptools wheel
    uv pip install -q --python "$venv/bin/python" torch --index-url https://download.pytorch.org/whl/cu124 2>&1 | tail -2
    for f in requirements.txt requirements-dev.txt; do [ -f "$src/$f" ] && { uv pip install -q --python "$venv/bin/python" -r "$src/$f" 2>&1 | tail -3; }; done
    [ -f "$src/pyproject.toml" ] && { uv pip install -q --python "$venv/bin/python" -e "$src" 2>&1 | tail -3; }
    [ -f "$src/setup.py" ] && [ ! -f "$src/pyproject.toml" ] && { uv pip install -q --python "$venv/bin/python" -e "$src" 2>&1 | tail -3; }
    case "$entry" in *.ipynb*) uv pip install -q --python "$venv/bin/python" jupyter nbconvert ipykernel matplotlib ipympl 2>&1 | tail -2 ;; esac
    echo "== prep done $(date -Is)"; } >> "$plog" 2>&1
  return 0
}

node_min() { # idx slug
  local i="$1" slug="$2" d="$EXPS/$2"
  [ -x "$d/run.sh" ] || { echo "== $(date -Is) NODE $i-$slug SKIP no run.sh" | tee -a "$LOG"; return; }
  while gpu_busy; do sleep 60; done
  echo "== $(date -Is) NODE $i-$slug START" | tee -a "$LOG"
  local s=$(date +%s) rc=1 round=0 fixes=""
  : > "$d/autofixes.txt"
  prep_env "$d" || { echo "== $(date -Is) NODE $i-$slug EXIT 2 after $(( ($(date +%s)-s)/60 )) min | prep failed (see prep.log)" | tee -a "$LOG"; return; }
  while :; do
    ( cd "$d" && bash ./run.sh ) > "$d/node.out" 2>&1; rc=$?
    [ $rc -eq 0 ] && break
    round=$((round+1)); [ $round -gt 3 ] && break
    local pk; pk=$(python3 "$REP/tree_autofix.py" "$d/run.log" "$d/node.out" 2>/dev/null)
    [ -z "$pk" ] && break
    local new=""; for p in $pk; do case " $fixes " in *" $p "*) ;; *) new="$new $p";; esac; done
    [ -z "${new// /}" ] && break
    echo "AUTOFIX round $round: uv pip install$new" | tee -a "$d/autofixes.txt"
    uv pip install -q --python "$d/.venv/bin/python" $new >> "$d/autofixes.txt" 2>&1 || { echo "  (install failed)" >> "$d/autofixes.txt"; break; }
    fixes="$fixes$new"
    mv "$d/run.log" "$d/run.attempt$round.log" 2>/dev/null
  done
  echo "== $(date -Is) NODE $i-$slug EXIT $rc after $(( ($(date +%s)-s)/60 )) min | autofix rounds=$round$( [ -n "$fixes" ] && echo " installed:$fixes")" | tee -a "$LOG"
}

i=1
while read -r slug; do
  [ -z "$slug" ] && continue
  i=$((i+1))
  grep -qxF "$slug" "$DONE" 2>/dev/null && continue
  node_min "$i" "$slug"
done < "$REP/tree_minute_class.txt"
echo "== $(date -Is) TREE DONE" | tee -a "$LOG"
