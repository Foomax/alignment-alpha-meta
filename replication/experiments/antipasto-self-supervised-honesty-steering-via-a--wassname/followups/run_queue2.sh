#!/usr/bin/env bash
# Second queue: waits for run_queue.sh and any train.py to finish, then runs follow-up 6.
set -uo pipefail
EXP="$(cd "$(dirname "$0")/.." && pwd)"; SRC="$EXP/src"; LOG="$EXP/followups/queue.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 PYTORCH_ALLOC_CONF=expandable_segments:True
cd "$SRC"
while pgrep -f "run_queue.sh" >/dev/null || pgrep -f "nbs/train.py" >/dev/null; do sleep 30; done
name="6-gemma270m-richer-personas"; lf="fu6_270m_personas.log"
echo "== $(date -Is) STEP $name START" | tee -a "$LOG"
s=$(date +%s); timeout 70m uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --experiment_name fu6-270m-personas \
  --PERSONAS.0 "a scrupulously honest, transparent and truthful" --PERSONAS.1 "a manipulative, deceptive and dishonest" > "$EXP/followups/$lf" 2>&1; rc=$?
f1=$(tr '\r' '\n' < "$EXP/followups/$lf" | sed 's/\x1b\[[0-9;]*m//g' | grep -oE "Steering F1: [^ ]*[0-9.]+" | head -1)
echo "== $(date -Is) STEP $name EXIT $rc after $(( ($(date +%s)-s)/60 )) min | $f1" | tee -a "$LOG"
echo "== $(date -Is) QUEUE2 DONE" | tee -a "$LOG"
