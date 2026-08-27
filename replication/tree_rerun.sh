#!/usr/bin/env bash
# Second pass over minute-class nodes that failed for runner/env reasons in pass 1. Each rerun uses the
# node's correct invocation (the spec 'entrypoint' strings are descriptive, not literal commands),
# plus environment-only fixes (packages, submodules, PYTHONPATH, PATH, a larger time-box where the
# author's own runtime exceeds the catalogue's 45-min guess). Nothing measured is changed.
# Waits for the first pass (tree_queue.sh) and for a free GPU. One line per node -> tree.log.
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; EXPS="$REP/experiments"; LOG="$REP/tree.log"
export WANDB_MODE=disabled HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_XET=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
gpu_busy() { nvidia-smi --query-compute-apps=process_name --format=csv,noheader 2>/dev/null | grep -qiE 'python' || pgrep -f '^bash \./tree_queue\.sh' >/dev/null; }
while gpu_busy; do sleep 60; done

rr() { # name slug timeout_min "shell command run inside experiments/<slug>"
  local name="$1" slug="$2" tmo="$3" cmd="$4" d="$EXPS/$2"
  while gpu_busy; do sleep 60; done
  echo "== $(date -Is) NODE $name-$slug START (rerun)" | tee -a "$LOG"
  sed -i 's/^== RUN-EXIT/== ATTEMPT-EXIT/' "$d/run.log" 2>/dev/null
  echo "== $(date -Is) RERUN: $cmd" >> "$d/run.log"
  local s=$(date +%s)
  ( cd "$d" && VENV="$d/.venv" timeout "${tmo}m" bash -c "$cmd" ) >> "$d/run.log" 2>&1; local rc=$?
  echo "== RUN-EXIT $rc after $(( ($(date +%s)-s)/60 )) min" | tee -a "$d/run.log"
  echo "== $(date -Is) NODE $name-$slug EXIT $rc after $(( ($(date +%s)-s)/60 )) min (rerun)" | tee -a "$LOG"
}

rr R7  unpacking-multimodal-data-leakage-broken-benchma--ai-forever      45 'cd src && ../.venv/bin/python shift_detection/run_attack.py --dataset vl_mia_img_Flickr_2k --attack bag_of_visual_words'
rr R3  features-of-saes-are-universal-but-only-up-to-an--jordanmccann     45 'cd src && ../.venv/bin/python -m replicate run-fast'
rr R5  saes-are-highly-dataset-dependent-a-case-study-o--ckkissane        45 'uv pip install -q --python .venv/bin/python numpy && cd src && ../.venv/bin/python refusal_dir_recons_fidelity_evals.py'
rr R14 confirming-claims-of-superposition-and-adversari--uchicago-xlab    45 'cd src && ../.venv/bin/python -m synth.run'
rr R13 the-self-hating-attention-head-a-deep-dive-in-gp--mamiglia         45 'uv pip install -q --python .venv/bin/python "sae-lens<6" && cd src && ../.venv/bin/python skew_analysis.py'
rr R10 developmental-stages-in-multi-problem-grokking--james-sullivan     50 'uv pip install -q --python .venv/bin/python neel-plotly && bash ./run.sh'
rr R4  investigating-sensitive-directions-in-gpt-2-an-i--dajale423        45 'git -C src submodule update --init --recursive 2>&1 | tail -1; uv pip install -q --python .venv/bin/python "git+https://github.com/dajale423/e2e_sae.git" && cd src && ../.venv/bin/python scripts/sensitive_direction.py'
rr R8  activation-plateaus-where-and-how-they-emerge--mshinkle            50 'cd src && PATH="$PWD/../.venv/bin:$PATH" bash full_experiment.sh'
rr R6  can-we-interpret-latent-reasoning-using-current---cywinski         95 'cd src && ../.venv/bin/python experiments/4_mean_latent_patching_same_vs_diff.py'
echo "== $(date -Is) RERUN PASS DONE" | tee -a "$LOG"
