# lessons-11 — from R20 (2026-08-27 19:20)

New:
1. **Never patch a bash script that a live process is executing.** bash reads the file incrementally by offset; rewriting the same inode (Write tool, `open(p,"w")`, `sed -i` without a temp? — `sed -i` is safe, it creates a new inode) corrupts the running instance mid-script. R20's spurious "prep failed" came from exactly this. Patch → write `x.sh.new` → `mv x.sh.new x.sh`. Long-running loops that `bash`-invoke helper scripts on every iteration are the most exposed.
2. **Read the setup script before queuing a chain.** Thirty seconds of reading `setup_box.sh` showed `/root/.hf_token`, `/workspace`, six 7B checkpoints, and a 48 GB-card assumption — all of which make the node a `vram`/scale row, not a rerun. A queued attempt would have spent hours downloading before failing.
3. **Catalogue VRAM estimates can miss the base model entirely** (15 GB listed vs 2 × 7B in bf16). Sanity-check `vram_estimate_gb` against the model ids in `spec.json["models"]` and any `qwen2.5-7b`-style names in checkpoint ids.
4. **Withdrawing a queued entry is a `sed -i '/^NAME|/d'` on the list file** — safe while the queue runs because the loop holds the old inode until its next pass.

Confirmed: lessons-synth P1 (system before science), P3 (environments are budgets), lessons-1 A5 (author-stated hardware wins).
