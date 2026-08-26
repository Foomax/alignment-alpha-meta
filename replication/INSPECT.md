# Repo feasibility inspection contract

You are one of several inspection agents. You get a list of candidate experiments (post + repo).
For **each**, decide whether a competent engineer with **one RTX 3090 (24 GB VRAM), 31 GB RAM,
~150 GB free disk, Linux, no cloud credits, no closed-model API keys** could re-run the
experiment that produced the post's headline number, and what it would take.

## Inputs

- Your assignment: `/home/user/alignment-literature-meta-analysis/replication/inspect/assign_N.json`
  — a list of objects with `post_id`, `repo`, `head_sha`, `title`, `primary_claim`, `metric`,
  `target_value`, `models`, `workload`, `tier`.
- The post text, if you need it: `/home/user/alignment-literature-meta-analysis/p3/posts/<post_id>.md`

## Procedure per repo

1. Shallow-clone into the scratchpad, pinned to `head_sha`:
   `git clone --depth 1 https://github.com/<repo> /tmp/claude-1000/-home-user-alignment-literature-meta-analysis/a21c0252-eab3-408a-93de-663a99b5679b/scratchpad/inspect/<owner>__<name>`
   (if the clone fails, record `status: "clone-failed"` and move on).
2. Read: README, `requirements*.txt` / `pyproject.toml` / `environment.yml` / `setup.py`, and
   the top-level file tree. Skim the scripts / notebooks whose names match the headline
   experiment. **Do not run anything. Do not install anything.**
3. Answer the schema below from what you read. Where the repo does not say, say `null` — do not
   guess a VRAM figure from vibes. If the README states compute used (e.g. "ran on an A100"),
   quote it.

## Output — one JSON object per repo, appended to a list, written to
`/home/user/alignment-literature-meta-analysis/replication/inspect/result_N.json`

```json
{
  "post_id": "...", "repo": "owner/name", "head_sha": "...",
  "status": "ok|clone-failed|empty|no-code",
  "language": "python|notebook|mixed|other",
  "entrypoint": "path/to/script_or_notebook that produces the headline number, or null",
  "entrypoint_confidence": "high|medium|low",
  "env": {"has_requirements": true, "pinned_versions": false, "python_version": "3.10|null",
          "key_deps": ["transformer_lens", "sae_lens", "torch", "..."],
          "stated_compute": "verbatim quote or null"},
  "models_needed": [{"hf_id": "google/gemma-2-2b or null", "params_b": 2.0, "gated": true}],
  "vram_estimate_gb": 8,
  "vram_basis": "why: e.g. 'bf16 inference of 2B + SAE activations cache'",
  "fits_3090": "yes|probably|tight|no|unknown",
  "data": {"needed": ["dataset names"], "available": "in-repo|hf-hub|download-script|missing|unknown",
           "gated": false},
  "est_runtime": "minutes|hours|days|unknown",
  "est_runtime_basis": "what in the repo says so",
  "needs_closed_api": false,
  "needs_closed_api_for": "e.g. 'GPT-4o as judge' or null",
  "headline_artifact": "which table/figure/number in the post the entrypoint produces, or null",
  "blockers": ["specific things that would stop a replication"],
  "notes": "<= 3 sentences of anything else decision-relevant"
}
```

## Rules

- **Fidelity over optimism.** A repo that needs an 8×A100 run to make the headline number is a
  `no`, even if a tiny version would run. Say what the tiny version would and would not test.
- **`needs_closed_api` is a hard flag.** If any step calls OpenAI / Anthropic / Google APIs (a
  judge model, a data-generation step, the model under test), set it true and say what for.
  The replication budget has no API keys.
- **Gated models** (Llama, Gemma) are fine — note `gated: true` so the runner knows to accept
  a licence — but they are not blockers.
- **Notebooks count as code** but flag `language: notebook`; it affects how the runner executes.
- If the headline number comes from something the repo does not contain (e.g. "we also ran it
  on our internal cluster"), the entrypoint is `null` and that is the finding.
- Do everything inline; do not spawn subagents. Delete nothing. Write only to your `result_N.json`.

Reply with: assignment number, count inspected, count `fits_3090: yes|probably`, and the two
most surprising things you found.
