**Claim being checked.** Take Qwen2.5‑1.5B‑Instruct, tell it to deliberately do badly at grade‑school maths ("sandbag"), then add small random noise to its weights. The post says noise makes an honest model *worse* but can make a sandbagging model *better* — the noise partly undoes the instructed under‑performance. It's itself a replication of a published method (Tice et al.).

**What happened.** It reproduced, more clearly than in the author's own data. Under the normal prompt accuracy fell from 72 % to 51 % as noise grew. Under the sandbag prompt it started at 46 % and rose to 60 % at moderate noise; **9 of 10 seeds** gained more than 5 points (the author's CSVs: 6 of 10). One pre‑registered check (accuracy must never tick *up* under the normal prompt) missed by a single point at the tiniest noise level — inside sampling error, and disclosed up front in the ledger rather than hidden.

**A bonus mechanism.** The sandbag prompt makes the model blurt a bare answer with no reasoning 47 % of the time; noise cuts that to 11 %. The noise erodes the *behaviour* the prompt installs before it erodes competence — which is why the trick works.

**Environment fixes (never the measurement):** pinned `transformers<5` (the repo has no pin; v5 came out after the author's run); one missing import that made the entrypoint crash on every commit (the author ran in a notebook); the two script edits the protocol prescribes (output folder, add noise 0 so the baseline comes from our own run). 103 minutes on the 3090; ~1 minute per 350‑question pass.

Details: `replication/report-03.md`, `replication/analysis.txt`, per‑pass CSVs in `logs/repl_20260826/`.
