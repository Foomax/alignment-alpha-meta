#!/usr/bin/env bash
# Experiment 01 pipeline per ~/prompts/3090/01-cross-model-geometry.md. Waits for the model downloads,
# builds the venv, then runs extraction -> CKA -> corrected permutation tests for evals C, A, B, D, E.
# Appends everything to run.log; report.py parses INSTALL-EXIT / RUN-EXIT from it.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$HERE/src"; VENV="$HERE/.venv"; LOG="$HERE/run.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$SRC"   # env fix: scripts/*.py import `src.*` relative to the repo root
BUDGET_MIN=240
log() { echo "== $(date -Is) $*" | tee -a "$LOG"; }

log "start jaehoonlee0829/cross-model-alignment-geometry@bfacecff2e21872a839ab4fb1dc54ed901d684f6 (run01.sh)"
while ! grep -q "^DOWNLOADS-EXIT 0" "$HERE/downloads.log" 2>/dev/null; do
  if grep -q "^DOWNLOADS-EXIT [1-9]" "$HERE/downloads.log" 2>/dev/null; then log "DOWNLOADS FAILED, continuing (hf_hub will retry per model)"; break; fi
  sleep 60
done
log "downloads: $(grep -c '^DONE' "$HERE/downloads.log") models ready"

if [ ! -x "$VENV/bin/python" ]; then
  uv venv -q "$VENV" --python 3.11 2>&1 | tee -a "$LOG"
  uv pip install -q --python "$VENV/bin/python" torch --index-url https://download.pytorch.org/whl/cu124 2>&1 | tail -2 | tee -a "$LOG"
  # requirements.txt pulls sae-lens and nnsight (unused by these scripts); try the full file, fall back to everything else
  if ! uv pip install -q --python "$VENV/bin/python" -r "$SRC/requirements.txt" 2>&1 | tail -3 | tee -a "$LOG"; then
    log "ENV FIX: requirements.txt failed to resolve; installing without sae-lens/nnsight"
    grep -vE "^(sae-lens|nnsight)" "$SRC/requirements.txt" > "$HERE/requirements.noheavy.txt"
    uv pip install -q --python "$VENV/bin/python" -r "$HERE/requirements.noheavy.txt" 2>&1 | tail -3 | tee -a "$LOG"
  fi
  rc=$?; echo "INSTALL-EXIT $rc" | tee -a "$LOG"
  "$VENV/bin/python" -c "import torch, transformers; print('torch', torch.__version__, torch.cuda.get_device_name(0), '| transformers', transformers.__version__)" 2>&1 | tee -a "$LOG"
fi

( nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -l 30 > "$HERE/vram.log" 2>/dev/null & echo $! > "$HERE/.vram.pid" )
start=$(date +%s); overall=0
cd "$SRC"
for cfg in eval_c phase_a phase_b phase_d phase_e; do
  elapsed=$(( ($(date +%s)-start)/60 ))
  if [ $elapsed -ge $BUDGET_MIN ]; then log "BUDGET EXHAUSTED before $cfg (${elapsed} min) — stopping"; overall=124; break; fi
  log "EVAL $cfg START (elapsed ${elapsed} min)"
  s=$(date +%s)
  timeout $(( (BUDGET_MIN-elapsed) ))m "$VENV/bin/python" scripts/run_extraction.py --config configs/$cfg.yaml 2>&1 | tee -a "$LOG" | grep -E "Extracting|Done|Error|Traceback|OutOfMemory" ; r1=${PIPESTATUS[0]}
  if [ $r1 -ne 0 ]; then log "EVAL $cfg extraction EXIT $r1"; overall=$r1; continue; fi
  "$VENV/bin/python" scripts/run_cka.py --config configs/$cfg.yaml 2>&1 | tee -a "$LOG" | grep -E "CKA|Layer|Error|Traceback" | head -20; r2=${PIPESTATUS[0]}
  "$VENV/bin/python" scripts/run_corrected_permutation_tests.py --config configs/$cfg.yaml 2>&1 | tee -a "$LOG" | grep -E "Observed|p-value|p=|CORRECTED|Error|Traceback" | head -20; r3=${PIPESTATUS[0]}
  log "EVAL $cfg EXIT extraction=$r1 cka=$r2 perm=$r3 after $(( ($(date +%s)-s)/60 )) min"
  [ $r2 -ne 0 ] || [ $r3 -ne 0 ] && overall=1
done
kill "$(cat "$HERE/.vram.pid")" 2>/dev/null; rm -f "$HERE/.vram.pid"
echo "== RUN-EXIT $overall after $(( ($(date +%s)-start)/60 )) min" | tee -a "$LOG"
exit $overall
