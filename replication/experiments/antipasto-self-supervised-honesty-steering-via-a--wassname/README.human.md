**Claim being checked.** AntiPaSTO trains a small adapter inside Gemma‑3‑1B so a dial makes the model more (+1) or less (−1) honest, from just the words "honest"/"dishonest". The paper reports a steering score of **31.2 ± 5.3** on 1,360 unseen moral dilemmas, beating prompting (4.5) and the classic "add a vector" method (0.0).

**What happened.** The shipped code runs perfectly and, on the headline model, scores **2.0 ± 1.7** over three seeds. Plain prompting scored 13.5 and an engineered prompt 17.9 — both beat it. Only "ActAdd = 0" held. The three seeds learned nearly the same adapter (cosine 0.7–0.9), so this isn't bad luck.

**Why, as far as we can tell.** The repo's Gemma‑1B preset is not the configuration the paper describes (learning rate, rank, module count and pair count all differ, and the paper's values never appear in the git history). Re‑running with the paper's own hyperparameters gives ≈21 before a "coherence" penalty and 0.7 after it, because the honest‑steered model starts answering in **bold** (`**Yes**`) and the scorer only recognises a plain ` Yes`. Counting bold answers gives 14.1; at best ≈26. The same code *does* reproduce the paper's number on the smaller Gemma‑270M (41.7 vs 38.7).

**Ablations on 270M (two seeds).** Fixing the rotation breaks it (9.7, robust); random dimension selection is a coin flip (43.6 / 2.7); the coherence and monotonicity barrier losses never switch on at this scale and can be removed without loss. The paper's "every component is load‑bearing" table is one clear yes, one sometimes, two noes here.

**Environment fixes (never the measurement):** a hung Hugging Face xet download (use `HF_HUB_DISABLE_XET=1`); the baseline scripts evaluate the wrong model in `--quick` mode (wrapper `replication/baselines_gemma1b.py`); eval batch 32 OOMs on 24 GB (batch 8); a cache‑name bug in the repeng script; a scheduler off‑by‑one when batches/epoch isn't divisible by the accumulation factor.

Full write‑ups: `replication/human.md` (plain language) and `replication/LLM-report.md` (dense, with every number and path).
