**Claim being checked.** Do different language‑model families secretly compute the same internal representations (the "Platonic Representation Hypothesis")? The post says: not really at 1–3B scale. Two models from the *same* family (Llama‑1B vs Llama‑3B) look very alike inside (0.91 on a 0–1 similarity scale), while pairs from *different* families score only about 0.2.

**What happened.** Reproduced for everything we could run. Same‑family control: **0.914** (post: 0.914). Llama vs Pythia: **0.208** (0.208). Gemma vs Qwen: **0.222** (0.222). Even the averages across all layer pairs match to three decimals, and the statistical tests say every one of these similarities is far above chance — i.e. real but weak, about 4× weaker across families than within. Two of the five comparisons (Llama‑3B vs Pythia‑2.8B, Llama‑3B vs Gemma‑2B) were not run: each comparison took ~100 minutes on this card and the protocol's four‑hour budget ran out; the protocol explicitly says the three we ran are enough to test the claim.

**Environment fixes (never the measurement):** the repo's scripts need the repo root on `PYTHONPATH`; the 22 GB of models were pre‑downloaded over plain HTTP (the fast download path stalls on this machine); CUDA build of torch.

Details: `replication/run.log` (timeline + VERDICT), `replication/ledger.json`, results under `outputs/{eval_c,phase_a,phase_b}/cka/`.
