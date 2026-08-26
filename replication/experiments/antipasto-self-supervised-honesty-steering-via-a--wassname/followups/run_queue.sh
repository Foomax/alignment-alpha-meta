#!/usr/bin/env bash
# Sequential follow-up queue. Waits for any running nbs/train.py to finish, then runs each step,
# one job on the GPU at a time. Each step is capped at 70 min. Results are appended to queue.log.
set -uo pipefail
EXP="$(cd "$(dirname "$0")/.." && pwd)"; SRC="$EXP/src"; LOG="$EXP/followups/queue.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 PYTORCH_ALLOC_CONF=expandable_segments:True
cd "$SRC"
while pgrep -f "nbs/train.py" >/dev/null; do sleep 30; done
run() { # name, logfile, cmd...
  local name="$1" lf="$2"; shift 2
  echo "== $(date -Is) STEP $name START: $*" | tee -a "$LOG"
  local s=$(date +%s); timeout 70m "$@" > "$EXP/followups/$lf" 2>&1; local rc=$?
  local f1=$(tr '\r' '\n' < "$EXP/followups/$lf" | sed 's/\x1b\[[0-9;]*m//g' | grep -E "Main metric - Steering F1|main_score" -A2 | grep -oE "F1: [^ ]*[0-9.]+|^\|\s+[0-9.]+ \| google[^|]*\| [a-z_]+" | head -1)
  echo "== $(date -Is) STEP $name EXIT $rc after $(( ($(date +%s)-s)/60 )) min | $f1" | tee -a "$LOG"
}
run 5-engineered-prompt-full  fu5_engineered.log     ../src/.venv/bin/python ../baselines_gemma1b.py prompting_engineered full
run 2-gemma270m               fu2_gemma270m.log      uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --experiment_name fu2-270m
run 3-gemma270m-randomdims    fu3_270m_random.log    uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --dim_select_method random --experiment_name fu3-270m-random
run 4-qwen3-0.6b              fu4_qwen06b.log        uv run python nbs/train.py q06b-24gb --seed 42 --experiment_name fu4-q06b
echo "== $(date -Is) QUEUE DONE" | tee -a "$LOG"
