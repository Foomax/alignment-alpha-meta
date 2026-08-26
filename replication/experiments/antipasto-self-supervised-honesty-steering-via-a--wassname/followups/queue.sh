#!/usr/bin/env bash
# Sequential follow-up queue (one GPU job at a time, each capped at 70 min). Appends to queue.log.
# Wait patterns are anchored so they match only real python/uv processes, never a launcher shell
# whose command line happens to contain the words.
set -uo pipefail
EXP="$(cd "$(dirname "$0")/.." && pwd)"; SRC="$EXP/src"; FU="$EXP/followups"; LOG="$FU/queue.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 PYTORCH_ALLOC_CONF=expandable_segments:True
cd "$SRC"
busy() { pgrep -f '^(uv run python|[^ ]*/python3?) (nbs/train\.py|\.\./baselines_gemma1b\.py)' >/dev/null; }
while busy; do sleep 30; done

run() { # name logfile cmd...
  local name="$1" lf="$2"; shift 2
  echo "== $(date -Is) STEP $name START: $*" | tee -a "$LOG"
  local s=$(date +%s); timeout 70m "$@" > "$FU/$lf" 2>&1; local rc=$?
  local f1; f1=$(tr '\r' '\n' < "$FU/$lf" | sed 's/\x1b\[[0-9;]*m//g' | grep -oE "Steering F1: [^ ]*[0-9.]+|^\|\s+[0-9.]+ \| google[^|]*\| [a-z_]+" | head -1)
  echo "== $(date -Is) STEP $name EXIT $rc after $(( ($(date +%s)-s)/60 )) min | ${f1:-no-F1-line}" | tee -a "$LOG"
}

run 1-paperconfig-retry   fu1_paperconfig_retry.log uv run python nbs/train.py gemma1b-24gb --lr 1e-3 --r 128 --n_modules 64 --max_samples 810 --bs 8 --seed 42 --experiment_name paperconfig
run 5-engineered-prompt   fu5_engineered.log        ../src/.venv/bin/python ../baselines_gemma1b.py prompting_engineered full
run 2-gemma270m           fu2_gemma270m.log         uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --experiment_name fu2-270m
run 3-gemma270m-randdims  fu3_270m_random.log       uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --dim_select_method random --experiment_name fu3-270m-random
run 4-qwen3-0.6b          fu4_qwen06b.log           uv run python nbs/train.py q06b-24gb --seed 42 --experiment_name fu4-q06b
run 6-270m-richer-personas fu6_270m_personas.log    uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --experiment_name fu6-270m-personas --PERSONAS.0 "a scrupulously honest, transparent and truthful" --PERSONAS.1 "a manipulative, deceptive and dishonest"
echo "== $(date -Is) QUEUE DONE" | tee -a "$LOG"
