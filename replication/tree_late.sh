#!/usr/bin/env bash
# Generic late-rerun queue. Reads tree_late.txt (lines: name|slug|timeout_min|command run inside experiments/<slug>),
# runs each line not yet in tree_late_done.txt, one at a time, only when no other runner/python holds the GPU.
# Keeps polling the file until tree_late.stop exists, so new reruns can be appended at any time.
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; EXPS="$REP/experiments"; LOG="$REP/tree.log"
LIST="$REP/tree_late.txt"; DONE="$REP/tree_late_done.txt"; touch "$LIST" "$DONE"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python' || pgrep -f '^bash \./tree_queue\.sh|^bash \./tree_rerun2?\.sh' >/dev/null; }
run_line() { local name="$1" slug="$2" tmo="$3" cmd="$4" d="$EXPS/$2"
  while gpu_busy; do sleep 60; done
  echo "== $(date -Is) NODE $name-$slug START (late rerun)" | tee -a "$LOG"
  sed -i 's/^== RUN-EXIT/== ATTEMPT-EXIT/' "$d/run.log" 2>/dev/null
  echo "== $(date -Is) RERUN: $cmd" >> "$d/run.log"
  local s=$(date +%s)
  ( cd "$d" && timeout "${tmo}m" bash -c "$cmd" ) >> "$d/run.log" 2>&1; local rc=$?
  echo "== RUN-EXIT $rc after $(( ($(date +%s)-s)/60 )) min" | tee -a "$d/run.log"
  echo "== $(date -Is) NODE $name-$slug EXIT $rc after $(( ($(date +%s)-s)/60 )) min (late rerun)" | tee -a "$LOG"; }
while [ ! -f "$REP/tree_late.stop" ]; do
  while IFS='|' read -r name slug tmo cmd; do
    [ -z "${name:-}" ] && continue
    grep -qxF "$name" "$DONE" && continue
    run_line "$name" "$slug" "$tmo" "$cmd"
    echo "$name" >> "$DONE"
  done < "$LIST"
  sleep 120
done
echo "== $(date -Is) LATE QUEUE STOPPED" | tee -a "$LOG"
