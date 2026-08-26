#!/usr/bin/env bash
# Thin runner. Everything experiment-specific lives in spec.json; this script only wires it up.
# Usage: ./run.sh            (from inside experiments/<slug>/)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SPEC="$HERE/spec.json"
j() { python3 -c "import json,sys; v=json.load(open('$SPEC'))$1; print(v if v is not None else '')"; }
REPO=$(j "['repo']"); SHA=$(j "['head_sha']"); ENTRY=$(j "['entrypoint']"); PY=$(j "['python_version']")
BUDGET_MIN=$(j "['budget_minutes']")
SRC="$HERE/src"; VENV="$HERE/.venv"; LOG="$HERE/run.log"
start=$(date +%s); echo "== $(date -Is) start $REPO@$SHA" | tee "$LOG"

if [ ! -d "$SRC/.git" ]; then
  git clone -q "https://github.com/$REPO" "$SRC" 2>&1 | tee -a "$LOG"
  git -C "$SRC" checkout -q "$SHA" 2>&1 | tee -a "$LOG" || { echo "CHECKOUT-FAILED" | tee -a "$LOG"; exit 2; }
fi
if [ ! -x "$VENV/bin/python" ]; then
  uv venv -q "$VENV" --python "${PY:-3.11}" 2>&1 | tee -a "$LOG"
  # Torch first, from the CUDA index, so a repo's unpinned `torch` line does not pull a CPU wheel.
  uv pip install -q --python "$VENV/bin/python" torch --index-url https://download.pytorch.org/whl/cu124 2>&1 | tee -a "$LOG"
  for f in requirements.txt requirements-dev.txt; do
    [ -f "$SRC/$f" ] && uv pip install -q --python "$VENV/bin/python" -r "$SRC/$f" 2>&1 | tee -a "$LOG"
  done
  [ -f "$SRC/pyproject.toml" ] && uv pip install -q --python "$VENV/bin/python" -e "$SRC" 2>&1 | tee -a "$LOG"
  echo "INSTALL-EXIT $?" | tee -a "$LOG"
fi

echo "== entrypoint: $ENTRY (budget ${BUDGET_MIN}m)" | tee -a "$LOG"
cd "$SRC"
( nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -l 30 > "$HERE/vram.log" 2>/dev/null & echo $! > "$HERE/.vram.pid" )
case "$ENTRY" in
  *.ipynb) timeout "${BUDGET_MIN:-120}m" "$VENV/bin/python" -m jupyter nbconvert --to notebook --execute "$ENTRY" --output "$HERE/executed.ipynb" --ExecutePreprocessor.timeout=-1 2>&1 | tee -a "$LOG"; rc=${PIPESTATUS[0]} ;;
  *.sh)    timeout "${BUDGET_MIN:-120}m" bash "$ENTRY" 2>&1 | tee -a "$LOG"; rc=${PIPESTATUS[0]} ;;
  *)       timeout "${BUDGET_MIN:-120}m" "$VENV/bin/python" $ENTRY 2>&1 | tee -a "$LOG"; rc=${PIPESTATUS[0]} ;;
esac
kill "$(cat "$HERE/.vram.pid")" 2>/dev/null; rm -f "$HERE/.vram.pid"
echo "== RUN-EXIT $rc after $(( ($(date +%s)-start)/60 )) min" | tee -a "$LOG"
exit $rc
