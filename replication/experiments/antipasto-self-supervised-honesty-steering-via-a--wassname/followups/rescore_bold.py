#!/usr/bin/env python3
"""Follow-up 7: re-evaluate a saved AntiPaSTO adapter on the full DailyDilemmas set with a
bold-tolerant choice measurement.

THIS IS A METRIC CHANGE (labelled follow-up, not part of the ledger). The repo measures P(Yes)/P(No)
at the first generated position only. With the paper-config adapter at coeff +1, 79% of answers
start with a markdown '**' token, so the first-position choice mass collapses (pmass 0.18) and the
Steer F1 pmass_ratio term multiplies the score by 0.035.

Here we compute, per row, a proper mixture:
    P(Yes) = P(Yes at t0) + P('**' at t0) * P(Yes at t1 | '**' at t0)      (same for No)
by running one extra forward pass with the most likely '**' variant appended. Everything else
(dataset, labels, prompts, F1 code, thresholds) is the repo's own. Run from src/:
    ../src/.venv/bin/python ../followups/rescore_bold.py <adapter_dir>
Writes <adapter_dir>/2_eval_labelled_bold_tolerant.parquet and prints both tables.
"""
import sys, torch, pandas as pd
sys.path.insert(0, ".")
from antipasto.peft_utils.load import load_adapter
from antipasto.peft_utils.adapter_scaling import ScaleAdapter
from antipasto.eval import get_choice_ids, get_choice_logprobs, gen_with_choices as _orig_gen
import antipasto.train.daily_dilemas as dd
from antipasto.train.train_adapter import (load_and_process_daily_dilemmas_eval_dataset, load_labels,
                                           process_daily_dilemma_results, evaluate_daily_dilemma)
from antipasto.train.daily_dilemas import format_main_results_table
from antipasto.config import TrainingConfig

STAR_IDS = [1018, 5213]  # '**' and ' **' in the Gemma-3 tokenizer (verified)


def gen_bold_tolerant(model, tokenizer, input_ids, attention_mask, choice_ids, continue_n_tokens=0, warn_low_pmass=True):
    outputs, seq_nll, logp_A, _ = _orig_gen(model, tokenizer, input_ids, attention_mask, choice_ids,
                                            continue_n_tokens=continue_n_tokens, warn_low_pmass=warn_low_pmass)
    with torch.no_grad():
        out = model(input_ids, attention_mask=attention_mask)
        logp_last = out.logits[:, -1].float().log_softmax(-1)
        star_lp = logp_last[:, STAR_IDS]                      # [b, 2]
        p_star = star_lp.exp().sum(-1)                        # [b]
        star_tok = torch.tensor(STAR_IDS, device=input_ids.device)[star_lp.argmax(-1)]
        ids2 = torch.cat([input_ids, star_tok[:, None]], 1)   # left-padded, so appending is safe
        am2 = torch.cat([attention_mask, torch.ones_like(star_tok[:, None])], 1)
        out2 = model(ids2, attention_mask=am2)
        logp_B = get_choice_logprobs(out2.logits[:, -1].float(), choice_ids)  # [b, 2]
    p = logp_A.float().exp() + p_star[:, None] * logp_B.exp()
    logp = p.clamp_min(1e-30).log()
    return outputs, seq_nll, logp, logp[:, 1] - logp[:, 0]


def run(adapter_dir, bold_tolerant):
    dd.gen_with_choices = gen_bold_tolerant if bold_tolerant else _orig_gen
    model, tokenizer, _ = load_adapter(adapter_dir, quantization_type=None)
    choice_ids = get_choice_ids(tokenizer)
    config = TrainingConfig(model_name="google/gemma-3-1b-it", use_wandb=False)
    dataset_dd, dataset_dd_pt = load_and_process_daily_dilemmas_eval_dataset(
        tokenizer, max_tokens=config.eval_max_tokens, eval_max_n_dilemmas=None)
    df_labels = load_labels(dataset_dd)
    results = []
    for coeff in [-1.0, 0.0, 1.0]:
        with ScaleAdapter(model, coeff=coeff):
            d = evaluate_daily_dilemma(model, dataset_dd_pt, tokenizer, choice_ids, batch_size=8, verbose=False)
        d["coeff"] = coeff; d["method"] = "AntiPaSTO (ours)"; d["model_id"] = config.model_name
        results.append(d)
    df = pd.concat(results, ignore_index=True)
    df_lab = process_daily_dilemma_results(df, dataset_dd, df_labels)[0]
    md, _, main = format_main_results_table(df_lab, config=config, target_method="AntiPaSTO (ours)", show_alt_measures=False)
    tag = "bold_tolerant" if bold_tolerant else "standard"
    df_lab.to_parquet(f"{adapter_dir}/2_eval_labelled_{tag}.parquet", index=False)
    print(f"\n===== {tag} | {adapter_dir} =====")
    print("pmass by coeff:", df.groupby("coeff")["pmass"].mean().round(3).to_dict())
    print(md.split("Steering Quality on")[0])
    print(f"MAIN Steer F1 ({tag}): {main}")
    del model; torch.cuda.empty_cache()
    return main


if __name__ == "__main__":
    adapter_dir = sys.argv[1]
    f_std = run(adapter_dir, bold_tolerant=False)
    f_bold = run(adapter_dir, bold_tolerant=True)
    print(f"\nSUMMARY {adapter_dir}: standard Steer F1 = {f_std}; bold-tolerant Steer F1 = {f_bold}")
