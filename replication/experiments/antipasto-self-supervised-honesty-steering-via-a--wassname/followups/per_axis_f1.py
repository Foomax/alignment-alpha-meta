#!/usr/bin/env python3
"""Follow-up E: per-value-axis Steer F1 (paper Table 4 'wins 5 of 6 axes') from an adapter run's
saved 2_eval_labelled.parquet, using the repo's own metric function with a different target column.
Usage: python per_axis_f1.py <adapter_dir> [<adapter_dir> ...]   (CPU only; run from src/)
"""
import sys, re
import pandas as pd, numpy as np
sys.path.insert(0, ".")
from antipasto.train.daily_dilemas import _compute_steering_f1_for_method
AXES = {"Honesty": r"Value/Honesty$", "Ambitious": r"Virtue/Ambition$", "Courageous": r"Virtue/Courage$",
        "Friendly": r"Virtue/Friendliness$", "Responsible": r"[Rr]esponsib", "Traditional": r"[Tt]radition"}
out = []
for d in sys.argv[1:]:
    df = pd.read_parquet(f"{d}/2_eval_labelled.parquet")
    df = df[df["coeff"].notna() & (df["method"] == "AntiPaSTO (ours)")]
    cols = [c for c in df.columns if c.startswith("logscore_")]
    pm = df.groupby("coeff")["pmass"].mean()
    row = {"run": d.rstrip("/").split("/")[-1]}
    for name, pat in AXES.items():
        matches = [c for c in cols if re.search(pat, c)]
        if not matches:
            row[name] = np.nan; continue
        # if several columns match (e.g. several 'responsib*' values) report the one with most valid rows
        best = max(matches, key=lambda c: int((df[c].notna() & (df[c] != 0)).sum()))
        r = _compute_steering_f1_for_method(df, 1.0, best, pm[1.0], pm[-1.0], pm[0.0])
        row[name] = round(float(r["steering_f1"]), 1)
        row[name + "_col"] = best.replace("logscore_", "")
        row[name + "_n"] = int((df.loc[df.coeff==0, best].notna() & (df.loc[df.coeff==0, best] != 0)).sum())
    out.append(row)
res = pd.DataFrame(out).set_index("run")
pd.set_option("display.width", 250)
print(res[[a for a in AXES]].to_string())
print("\nn valid dilemma-rows at coeff 0 per axis:", {a: int(res[a + "_n"].iloc[0]) for a in AXES if a + "_n" in res})
print("\ncolumns used:", {a: res[a + "_col"].iloc[0] for a in AXES if a + "_col" in res})
print("\npaper Table 4 (AntiPaSTO, n=3): Honesty 31.2±5.3  Ambitious 8.9±5.3  Courageous 7.3±9.5  Friendly 12.8±15.1  Responsible 14.4±3.0  Traditional 8.3±4.4")
