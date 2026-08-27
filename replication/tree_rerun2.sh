#!/usr/bin/env bash
# Late additions to the rerun pass. Waits for tree_rerun.sh (and pass 1) to finish and the GPU to be free.
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; EXPS="$REP/experiments"; LOG="$REP/tree.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python' || pgrep -f '^bash \./tree_queue\.sh|^bash \./tree_rerun\.sh' >/dev/null; }
while gpu_busy; do sleep 60; done
rr() { local name="$1" slug="$2" tmo="$3" cmd="$4" d="$EXPS/$2"
  while gpu_busy; do sleep 60; done
  echo "== $(date -Is) NODE $name-$slug START (rerun)" | tee -a "$LOG"
  sed -i 's/^== RUN-EXIT/== ATTEMPT-EXIT/' "$d/run.log" 2>/dev/null
  echo "== $(date -Is) RERUN: $cmd" >> "$d/run.log"
  local s=$(date +%s)
  ( cd "$d" && timeout "${tmo}m" bash -c "$cmd" ) >> "$d/run.log" 2>&1; local rc=$?
  echo "== RUN-EXIT $rc after $(( ($(date +%s)-s)/60 )) min" | tee -a "$d/run.log"
  echo "== $(date -Is) NODE $name-$slug EXIT $rc after $(( ($(date +%s)-s)/60 )) min (rerun)" | tee -a "$LOG"; }
rr R12 tracing-typos-in-llms-my-attempt-at-understandin--idostik 50 'cd src && ../.venv/bin/python -m jupyter nbconvert --to notebook --execute llm-typo-experiment.ipynb --output ../executed.ipynb --ExecutePreprocessor.timeout=-1'
echo "== $(date -Is) RERUN PASS 2 DONE" | tee -a "$LOG"
