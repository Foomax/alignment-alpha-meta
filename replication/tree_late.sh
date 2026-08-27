#!/usr/bin/env bash
# Generic late-rerun queue, disk-bounded. Reads tree_late.txt (name|slug|timeout_min|command run inside
# experiments/<slug>), skips names in tree_late_done.txt, runs one at a time when no python/runner holds
# the GPU. For each entry: tree_prep.sh builds the venv if missing (with the full import list), the
# command runs, then the venv is DELETED so only one ~4 GB venv exists at a time (the 17:54 disk-full
# event). Refuses to start an entry with < 12 GB free. Polls the list until tree_late.stop exists.
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; EXPS="$REP/experiments"; LOG="$REP/tree.log"
LIST="$REP/tree_late.txt"; DONE="$REP/tree_late_done.txt"; touch "$LIST" "$DONE"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python' || pgrep -f '^bash \./tree_queue\.sh|^bash \./tree_rerun2?\.sh' >/dev/null; }
free_gb() { df -BG --output=avail / | tail -1 | tr -dc '0-9'; }
run_line() { local name="$1" slug="$2" tmo="$3" cmd="$4" d="$EXPS/$2"
  while gpu_busy; do sleep 60; done
  while [ "$(free_gb)" -lt 12 ]; do echo "== $(date -Is) LOW DISK ($(free_gb) GB) — waiting before $name" | tee -a "$LOG"; sleep 300; done
  echo "== $(date -Is) NODE $name-$slug START (late rerun)" | tee -a "$LOG"
  bash "$REP/tree_prep.sh" "$d" || { echo "== $(date -Is) NODE $name-$slug EXIT 2 after 0 min (prep failed)" | tee -a "$LOG"; return; }
  sed -i 's/^== RUN-EXIT/== ATTEMPT-EXIT/' "$d/run.log" 2>/dev/null
  echo "== $(date -Is) RERUN: $cmd" >> "$d/run.log"
  local s=$(date +%s)
  ( cd "$d" && timeout "${tmo}m" bash -c "$cmd" ) >> "$d/run.log" 2>&1; local rc=$?
  echo "== RUN-EXIT $rc after $(( ($(date +%s)-s)/60 )) min" | tee -a "$d/run.log"
  echo "== $(date -Is) NODE $name-$slug EXIT $rc after $(( ($(date +%s)-s)/60 )) min (late rerun) | disk free after: $(free_gb) GB" | tee -a "$LOG"
  rm -rf "$d/.venv" "$d/src/.venv"; }
while [ ! -f "$REP/tree_late.stop" ]; do
  while IFS='|' read -r name slug tmo cmd; do
    [ -z "${name:-}" ] && continue
    grep -qxF "$name" "$DONE" && continue
    [ -f "$REP/tree_late.stop" ] && break
    run_line "$name" "$slug" "$tmo" "$cmd"
    echo "$name" >> "$DONE"
  done < "$LIST"
  sleep 120
done
echo "== $(date -Is) LATE QUEUE STOPPED" | tee -a "$LOG"
