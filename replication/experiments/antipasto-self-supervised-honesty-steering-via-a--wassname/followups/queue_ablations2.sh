#!/usr/bin/env bash
# Second seed for the three 270M ablations (hand-off.md slack use). Waits for queue_ablations.sh
# to finish and for no python process on the GPU. One job at a time.
set -uo pipefail
EXP="$(cd "$(dirname "$0")/.." && pwd)"; SRC="$EXP/src"; FU="$EXP/followups"; LOG="$FU/queue.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 PYTORCH_ALLOC_CONF=expandable_segments:True
cd "$SRC"
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python'; }
q1_alive() { pgrep -f '^bash \./queue_ablations\.sh' >/dev/null; }
while q1_alive || gpu_busy; do sleep 60; done
run() { local name="$1" lf="$2"; shift 2
  echo "== $(date -Is) STEP $name START: $*" | tee -a "$LOG"
  local s=$(date +%s); timeout 70m "$@" > "$FU/$lf" 2>&1; local rc=$?
  local f1; f1=$(tr '\r' '\n' < "$FU/$lf" | sed 's/\x1b\[[0-9;]*m//g' | grep -oE "Steering F1: [^ ]*[0-9.]+" | head -1)
  echo "== $(date -Is) STEP $name EXIT $rc after $(( ($(date +%s)-s)/60 )) min | ${f1:-no-F1-line}" | tee -a "$LOG"; }
run A6-270m-no_rot_v-s43  fuA6_270m_no_rot_v_s43.log uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 43 --no_rot_v --experiment_name fuA6-270m-norotv-s43
run A7-270m-no_coh-s43    fuA7_270m_no_coh_s43.log   uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 43 --no_coh  --experiment_name fuA7-270m-nocoh-s43
run A8-270m-no_mono-s43   fuA8_270m_no_mono_s43.log  uv run python nbs/train.py gemma270m-80gb --bs 24 --seed 43 --no_mono --experiment_name fuA8-270m-nomono-s43
echo "== $(date -Is) ABLATION QUEUE 2 DONE" | tee -a "$LOG"
