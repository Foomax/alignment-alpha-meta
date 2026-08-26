#!/usr/bin/env bash
# Runs after queue.sh: follow-up 7 (bold-tolerant re-score) on the paper-config adapter and, as a
# control, on the shipped-preset seed-44 adapter. Appends STEP lines to queue.log.
set -uo pipefail
EXP="$(cd "$(dirname "$0")/.." && pwd)"; SRC="$EXP/src"; FU="$EXP/followups"; LOG="$FU/queue.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 PYTORCH_ALLOC_CONF=expandable_segments:True
cd "$SRC"
busy() { pgrep -f '^bash \./queue\.sh|^(uv run python|[^ ]*/python3?) (nbs/train\.py|\.\./baselines_gemma1b\.py|\.\./followups/rescore_bold\.py)' >/dev/null; }
while busy; do sleep 30; done
run() { local name="$1" lf="$2"; shift 2
  echo "== $(date -Is) STEP $name START: $*" | tee -a "$LOG"
  local s=$(date +%s); timeout 70m "$@" > "$FU/$lf" 2>&1; local rc=$?
  local f1; f1=$(grep -oE "SUMMARY .*" "$FU/$lf" | tail -1)
  echo "== $(date -Is) STEP $name EXIT $rc after $(( ($(date +%s)-s)/60 )) min | ${f1:-no-summary}" | tee -a "$LOG"; }
run 7-rescore-bold-paperconfig fu7_rescore_paperconfig.log ../src/.venv/bin/python ../followups/rescore_bold.py outputs/adapters/20260826_093640_paperconfig
run 7c-rescore-bold-seed44-control fu7c_rescore_seed44.log ../src/.venv/bin/python ../followups/rescore_bold.py outputs/adapters/20260826_080947_g1b-antisym-r64-seed44
echo "== $(date -Is) QUEUE-AFTER DONE" | tee -a "$LOG"
