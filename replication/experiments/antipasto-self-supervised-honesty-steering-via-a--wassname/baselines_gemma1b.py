#!/usr/bin/env python3
"""Environment/entrypoint fix: run the repo's unmodified baseline scripts, but on the model the
claim is about (google/gemma-3-1b-it). As shipped, --quick evaluates EVAL_BASELINE_MODELS[:1]
(Qwen3-0.6B) and eval_baseline_repeng.py loops over ALL ten models even in --quick mode.
Nothing about prompts, thresholds, metrics or the dataset slice is changed here.

Usage (from src/): ../.venv/bin/python ../baselines_gemma1b.py prompting|repeng
"""
import sys, importlib.util, pathlib
src = pathlib.Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src))
which = sys.argv[1]
path = src / "nbs" / f"eval_baseline_{which}.py"
spec = importlib.util.spec_from_file_location(f"eval_baseline_{which}", path)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.EVAL_BASELINE_MODELS = ["google/gemma-3-1b-it"]
# VRAM fix: the scripts floor the eval batch at max(32, bs); on a 24GB card the fp32 logits for
# calc_nll (32 x ~320 tokens x 262k vocab) OOM. Batch size does not change what is measured.
_orig_eval = mod.evaluate_daily_dilemma
def _eval_small_batch(*a, **k):
    k["batch_size"] = 8
    return _orig_eval(*a, **k)
mod.evaluate_daily_dilemma = _eval_small_batch
from antipasto.config import TrainingConfig
mode = sys.argv[2] if len(sys.argv) > 2 else "quick"
config = TrainingConfig(model_name="google/gemma-3-1b-it", quick=(mode == "quick"), use_wandb=False)
mod.main(config)
