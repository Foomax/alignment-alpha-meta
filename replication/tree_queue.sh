#!/usr/bin/env bash
# The execution tree: experiment 01 (run01.sh) then every slug in tree_minute_class.txt via its run.sh.
# One GPU job at a time. For minute-class nodes, an automatic ENVIRONMENT-ONLY fix loop: if run.sh
# fails and the log shows a missing Python module (or missing jupyter for notebook entrypoints), the
# package is installed into that experiment's own venv and run.sh is re-run (max 3 rounds). Every
# auto-fix is appended to <exp>/autofixes.txt so the ledger can record it. Appends one line per
# finished node to tree.log (monitored).
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; EXPS="$REP/experiments"; LOG="$REP/tree.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python'; }

node01() {
  local d="$EXPS/cross-model-activation-generalizability-isn-t-st--jaehoonlee0829"
  while gpu_busy; do sleep 60; done
  echo "== $(date -Is) NODE 01-cross-model-geometry START" | tee -a "$LOG"
  local s=$(date +%s); ( cd "$d" && bash ./run01.sh ) > "$d/node.out" 2>&1; local rc=$?
  echo "== $(date -Is) NODE 01-cross-model-geometry EXIT $rc after $(( ($(date +%s)-s)/60 )) min" | tee -a "$LOG"
}

node_min() { # idx slug
  local i="$1" slug="$2" d="$EXPS/$2"
  if [ ! -x "$d/run.sh" ]; then echo "== $(date -Is) NODE $i-$slug SKIP no run.sh" | tee -a "$LOG"; return; fi
  while gpu_busy; do sleep 60; done
  echo "== $(date -Is) NODE $i-$slug START" | tee -a "$LOG"
  local s=$(date +%s) rc=1 round=0 fixes=""
  : > "$d/autofixes.txt"
  while :; do
    ( cd "$d" && bash ./run.sh ) > "$d/node.out" 2>&1; rc=$?
    [ $rc -eq 0 ] && break
    round=$((round+1)); [ $round -gt 3 ] && break
    local pk; pk=$(python3 "$REP/tree_autofix.py" "$d/run.log" "$d/node.out" 2>/dev/null)
    [ -z "$pk" ] && break
    # do not install the same package twice
    local new=""; for p in $pk; do case " $fixes " in *" $p "*) ;; *) new="$new $p";; esac; done
    [ -z "${new// /}" ] && break
    echo "AUTOFIX round $round: uv pip install$new" | tee -a "$d/autofixes.txt"
    uv pip install -q --python "$d/.venv/bin/python" $new >> "$d/autofixes.txt" 2>&1 || { echo "  (install failed)" >> "$d/autofixes.txt"; break; }
    fixes="$fixes$new"
    # run.sh only re-runs the entrypoint (clone + venv already exist); keep the old run.log as history
    mv "$d/run.log" "$d/run.attempt$round.log" 2>/dev/null
  done
  echo "== $(date -Is) NODE $i-$slug EXIT $rc after $(( ($(date +%s)-s)/60 )) min | autofix rounds=$round$( [ -n "$fixes" ] && echo " installed:$fixes")" | tee -a "$LOG"
}

node01
i=1
while read -r slug; do
  [ -z "$slug" ] && continue
  i=$((i+1))
  node_min "$i" "$slug"
done < "$REP/tree_minute_class.txt"
echo "== $(date -Is) TREE DONE" | tee -a "$LOG"
