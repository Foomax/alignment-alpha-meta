#!/bin/bash
# H57 sneaky-mamba: env-only build fix (mamba-ssm needs torch at build => --no-build-isolation,
# CUDA_HOME=/usr for nvcc 12.0). Then run the author's THREE parameterised arms (the top-of-file
# `architecture` switch: mamba=standard/fails, switcher=cross-channel/solves, transformer=GPT2),
# each timeout-capped. Toggling the author's own condition switch is a documented deviation from
# strict env-only, and is the only way to reproduce a cross-arm comparison. Nothing else touched.
set -o pipefail
cd "$(dirname "$0")/src" || exit 9
PY=../.venv/bin/python ; PIP="../.venv/bin/pip"
export HF_HUB_DISABLE_XET=1 WANDB_MODE=disabled TOKENIZERS_PARALLELISM=false CUDA_HOME=/usr
echo "=== build deps ==="
$PIP install -q wheel packaging ninja setuptools 2>&1 | tail -1
$PIP install -q -r prerequirements.txt 2>&1 | tail -1
echo "=== build causal-conv1d + mamba-ssm (--no-build-isolation, CUDA_HOME=$CUDA_HOME) ==="
$PIP install -q --no-build-isolation causal-conv1d 2>&1 | tail -3
$PIP install -q --no-build-isolation mamba-ssm 2>&1 | tail -4
$PIP install -q wandb accelerate ipykernel 2>&1 | tail -1
$PY -c "import mamba_ssm; print('mamba_ssm import OK')" || { echo "BUILD-FAIL: mamba_ssm not importable"; exit 3; }
cp sneaky_mamba/doublethink_train.py sneaky_mamba/_dt_base.py
for arch in mamba switcher transformer; do
  echo "###### ARM=$arch (num_layers=4) ######"
  sed "s/^architecture = .*/architecture = \"$arch\"/" sneaky_mamba/_dt_base.py > sneaky_mamba/doublethink_train.py
  timeout 30m $PY sneaky_mamba/doublethink_train.py 2>&1 | grep -aE "seq\.len|Traceback|Error|error:|ValueError|RuntimeError|OutOfMemory|CUDA" | tail -30
  echo "###### END ARM=$arch pipestatus=${PIPESTATUS[0]} ######"
done
cp sneaky_mamba/_dt_base.py sneaky_mamba/doublethink_train.py
echo "=== H57 sweep done ==="
