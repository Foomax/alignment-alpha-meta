#!/usr/bin/env bash
# Standalone environment prep for one experiment dir (same logic as tree_queue.sh's prep_env):
# clone at the pinned SHA if missing, create .venv with a sanitised Python version, install
# pip/setuptools/wheel, torch (cu124 index), requirements*.txt, editable project, notebook stack for
# .ipynb entrypoints, and the full import list from tree_imports.py. Logs to <dir>/prep.log.
# Usage: tree_prep.sh <experiment_dir>
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; d="$1"; spec="$d/spec.json"; src="$d/src"; venv="$d/.venv"; plog="$d/prep.log"
export HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1
repo=$(python3 -c "import json;print(json.load(open('$spec'))['repo'])")
sha=$(python3 -c "import json;print(json.load(open('$spec'))['head_sha'])")
py=$(python3 -c "import json,re;v=str(json.load(open('$spec')).get('python_version') or '');m=re.search(r'(3\.\d+)',v);print(m.group(1) if m else '3.11')")
entry=$(python3 -c "import json;print(json.load(open('$spec')).get('entrypoint') or '')")
{ echo "== prep $(date -Is) repo=$repo sha=$sha py=$py"
  if [ ! -d "$src/.git" ]; then git clone -q "https://github.com/$repo" "$src" && git -C "$src" checkout -q "$sha" || { echo "CLONE-FAILED"; exit 1; }; fi
  if [ ! -x "$venv/bin/python" ]; then uv venv -q "$venv" --python "$py" || uv venv -q "$venv" --python 3.11 || { echo "VENV-FAILED"; exit 1; }; fi
  uv pip install -q --python "$venv/bin/python" pip setuptools wheel
  uv pip install -q --python "$venv/bin/python" torch --index-url https://download.pytorch.org/whl/cu124 >/dev/null 2>&1 || echo "TORCH-INSTALL-FAILED (cu124 index)"
  "$venv/bin/python" -c "import torch;print('torch', torch.__version__)" 2>&1 | tail -1
  for f in requirements.txt requirements-dev.txt; do
    [ -f "$src/$f" ] || continue
    if ! uv pip install -q --python "$venv/bin/python" -r "$src/$f" >/dev/null 2>&1; then
      echo "requirements file $f did not resolve as a whole; installing line by line"
      grep -vE '^\s*(#|$|-e |--)' "$src/$f" | sed 's/#.*//' | while read -r req; do
        uv pip install -q --python "$venv/bin/python" "$req" >/dev/null 2>&1 || echo "  SKIPPED unresolvable requirement: $req"
      done
    fi
  done
  if [ -f "$src/pyproject.toml" ] || [ -f "$src/setup.py" ]; then uv pip install -q --python "$venv/bin/python" -e "$src" 2>&1 | tail -3; fi
  case "$entry" in *.ipynb*) uv pip install -q --python "$venv/bin/python" jupyter nbconvert ipykernel matplotlib ipympl 2>&1 | tail -2 ;; esac
  imports=$(python3 "$REP/tree_imports.py" "$src" --exclude google,e2e_sae,replicate 2>/dev/null)
  if [ -n "$imports" ]; then
    if ! uv pip install -q --python "$venv/bin/python" $imports >/dev/null 2>&1; then
      echo "import list did not resolve as a batch; installing per package"
      for pkg in $imports; do uv pip install -q --python "$venv/bin/python" "$pkg" >/dev/null 2>&1 || echo "  SKIPPED unresolvable import package: $pkg"; done
    fi
  fi
  echo "== prep done $(date -Is) ($(du -sh "$venv" | cut -f1))"; } >> "$plog" 2>&1
exit 0
