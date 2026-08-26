#!/usr/bin/env python3
"""Follow-up D: how similar are AntiPaSTO adapters trained from different seeds?

Usage: python cross_seed_similarity.py <adapter_dir_A> <adapter_dir_B> [<adapter_dir_C> ...]
Reports, per pair: whether the SVD bases are identical (they should be, data_seed fixed),
cosine similarity of the rotation generators (theta_v) and delta_s per module, and the
cosine similarity of the *effective* rank-64 update direction (R(theta) applied to the basis).
CPU only.
"""
import sys, json, itertools
import torch
from safetensors import safe_open

def load(d):
    t = {}
    with safe_open(f"{d}/adapter_model.safetensors", "pt") as f:
        for k in f.keys(): t[k] = f.get_tensor(k).float()
    b = {}
    with safe_open(f"{d}/0_svd_bases.safetensors", "pt") as f:
        for k in f.keys(): b[k] = f.get_tensor(k).float()
    sel = json.load(open(f"{d}/0_layer_selection.json"))
    return t, b, sel

def cayley(theta):
    A = theta - theta.T
    I = torch.eye(A.shape[0])
    return torch.linalg.solve(I + A, I - A)

def cos(a, b):
    return torch.nn.functional.cosine_similarity(a.flatten(), b.flatten(), dim=0).item()

dirs = sys.argv[1:]
runs = {d: load(d) for d in dirs}
for a, b in itertools.combinations(dirs, 2):
    ta, ba, sa = runs[a]; tb, bb, sb = runs[b]
    print(f"\n=== {a.split('/')[-1]}  vs  {b.split('/')[-1]} ===")
    print("same adapter modules:", sa["adapter_layer_names"] == sb["adapter_layer_names"],
          "| same loss layers:", sa["loss_layer_names"] == sb["loss_layer_names"])
    same_bases = all(k in bb and torch.allclose(ba[k], bb[k], atol=1e-5) for k in ba)
    print("SVD bases identical:", same_bases, f"({len(ba)} tensors)")
    mods = sorted({k.rsplit('.', 1)[0] for k in ta if k.endswith("rotation_params_v")})
    cth, cds, ceff = [], [], []
    for m in mods:
        th_a, th_b = ta[m + ".antipasto_rotation_params_v"], tb[m + ".antipasto_rotation_params_v"]
        ds_a, ds_b = ta[m + ".antipasto_delta_s"], tb[m + ".antipasto_delta_s"]
        cth.append(cos(th_a, th_b)); cds.append(cos(ds_a, ds_b))
        # effective change of the rotation: R - I, compared in the shared basis
        ceff.append(cos(cayley(th_a) - torch.eye(th_a.shape[0]), cayley(th_b) - torch.eye(th_b.shape[0])))
    t = lambda x: torch.tensor(x)
    print(f"theta_v cos-sim:   mean {t(cth).mean():+.3f}  median {t(cth).median():+.3f}  min {t(cth).min():+.3f}  max {t(cth).max():+.3f}")
    print(f"delta_s cos-sim:   mean {t(cds).mean():+.3f}  median {t(cds).median():+.3f}  min {t(cds).min():+.3f}  max {t(cds).max():+.3f}")
    print(f"(R-I) cos-sim:     mean {t(ceff).mean():+.3f}  median {t(ceff).median():+.3f}  min {t(ceff).min():+.3f}  max {t(ceff).max():+.3f}")
    print(f"theta_v norms A/B: {t([ta[m+'.antipasto_rotation_params_v'].norm() for m in mods]).mean():.3f} / {t([tb[m+'.antipasto_rotation_params_v'].norm() for m in mods]).mean():.3f}")
    # random-baseline reference: cos-sim of two independent gaussian 64x64 matrices ~ 0 +- 1/64
    print("reference: unrelated random 64x64 matrices give |cos| ~ 0.016")
