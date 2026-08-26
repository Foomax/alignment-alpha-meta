#!/usr/bin/env bash
# 270M ablation suite (hand-off.md C3 + C4). Waits until (a) the sentinel written when experiment 03
# starts exists AND (b) no *python* process holds the GPU (desktop apps also show up in
# nvidia-smi's compute-apps list, so filter by process name), then runs one job at a time.
set -uo pipefail
EXP="$(cd "$(dirname "$0")/.." && pwd)"; SRC="$EXP/src"; FU="$EXP/followups"; LOG="$FU/queue.log"
SENTINEL="$EXP/../adding-noise-to-a-sandbagging-model-can-reveal-i--lovkush-a/.gpu_started"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 PYTORCH_ALLOC_CONF=expandable_segments:True
cd "$SRC"
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python'; }
while [ ! -f "$SENTINEL" ]; do sleep 60; done
sleep 180
while gpu_busy; do sleep 60; done
run() { local name="$1" lf="$2"; shift 2
  echo "== $(date -Is) STEP $name START: $*" | tee -a "$LOG"
  local s=$(date +%s); timeout 70m "$@" > "$FU/$lf" 2>&1; local rc=$?
  local f1; f1=$(tr '\r' '\n' < "$FU/$lf" | sed 's/\x1b\[[0-9;]*m//g' | grep -oE "Steering F1: [^ ]*[0-9.]+" | head -1)
  echo "== $(date -Is) STEP $name EXIT $rc after $(( ($(date +%s)-s)/60 )) min | ${f1:-no-F1-line}" | tee -a "$LOG"; }
run A1-270m-no_rot_v      fuA1_270m_no_rot_v.log   uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --no_rot_v --experiment_name fuA1-270m-norotv
run A2-270m-no_coh        fuA2_270m_no_coh.log     uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --no_coh  --experiment_name fuA2-270m-nocoh
run A3-270m-no_mono       fuA3_270m_no_mono.log    uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 42 --no_mono --experiment_name fuA3-270m-nomono
run A4-270m-default-s43   fuA4_270m_default_s43.log uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 43 --experiment_name fuA4-270m-s43
run A5-270m-random-s43    fuA5_270m_random_s43.log uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 43 --dim_select_method random --experiment_name fuA5-270m-random-s43
echo "== $(date -Is) ABLATION QUEUE DONE" | tee -a "$LOG"
