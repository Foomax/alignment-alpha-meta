# Replicate: Creating Interpretable Latent Spaces with Gradient Routing

Source post: `8zDjhJNoFhMuHB5Kc` (2024-12-14, LW karma 26). Repo: `g-w1/gradient-routed-vae` @ `a644302f8abf5c15541380bff7068bf615f1d319`.
Everything below is also in `spec.json`; this file exists so a fresh Claude Opus session can start
from it alone. **Follow `prompts.md` P9 (the replication protocol) — it overrides anything here.**

## The claim you are testing

> Applying gradient routing to an MNIST variational autoencoder (masking all latent dimensions except the one corresponding to the image's label during training) produces a 10-dimensional latent space that specializes one dimension per digit, enabling digit classification via argmax over the encoding at 92.58% accuracy despite no explicit classification loss.

Supporting quote from the post: "we can classify digits to 92.58% accuracy by just taking the argmax over the encoding (which slider is the most positive), which I find pretty amazing."

**Headline metric:** digit classification accuracy via argmax over latent encoding
**Claimed value:** 92.58%
**Direction of the claim:** +
**Uncertainty the post reported:** none
**Tolerance for "reproduced":** `abs:5` — percentage metric: 5 points; post reported no spread, tolerance is a guess

## What the inspection pass found (read-only, 2026-08-26)

- Entrypoint: `vae.py` (confidence: high)
- Produces: final print statement in vae.py: 'Classification accuracy from encoding: {correct/total}', computed via argmax over the ONNX-exported encoder's mean output on the MNIST validation set
- Models: ? (0.003B)
- Estimated VRAM: 1 GB — Plain MLP VAE: encoder 784->2048->512->10, mirrored decoder; a few million parameters total, batch size 128 over 28x28 MNIST images -- negligible VRAM even in fp32.
- Data: MNIST (train+test); availability: download-script
- Estimated runtime: minutes (100 epochs (hardcoded loop `for epoch in tqdm.tqdm(range(100))`) over MNIST's 60000 images with a small MLP, batch size 128 -- this is a classic fast toy-model training loop, minutes on a 3090.)
- Stated compute in the repo: none
- Known blockers: vae.py's save/export section is hardcoded SAVE=False, which tries to load a 'vae.pth' checkpoint that is not committed to the repo (only the already-exported vae_encoder.onnx/vae_decoder.onnx are included) -- a re-runner must flip SAVE=True (or otherwise skip the load) to actually train fresh weights before the final eval block will work end-to-end; no requirements.txt/pyproject.toml; deps must be inferred from the import block
- Inspector's notes: Single flat script (train + ONNX export + eval, using # %% cell markers, no CLI) that is otherwise fully self-contained and trivially cheap to run; the gradient-routing mechanism is the `encode_and_mask` method that masks all latent dims except the label-selected one during the backward pass.

## Budget

**45 minutes** of wall-clock for the run itself (environment setup not counted, but cap that
at 30 minutes). When the budget is exceeded, stop and record `blocking_reason: runtime`.

## Procedure

1. `cd` into this folder. Read `spec.json`. Run `./run.sh`. It clones at the pinned sha, builds a
   venv from the repo's own requirements, runs the entrypoint under `timeout`, and logs to
   `run.log` + `vram.log`.
2. If install fails: fix **only** the environment (a version pin, a missing system package, a
   CUDA-index torch wheel). Record every fix. Do not touch experiment code. If you cannot fix it
   in 30 minutes, `report.py --reason env`.
3. If the entrypoint needs an argument the inspection did not capture, read the README and the
   script's argparse; prefer the configuration the post describes. Record it as a fix.
4. If the run needs a gated model, the HF token is already on this machine; if it is not,
   `--reason model-access`.
5. When it finishes, find the headline number in the output. Compare to the claimed value
   under the tolerance. Then:
   `python3 report.py --observed "<value>" --reason none [--fix "..."]... [--notes "..."]`
   — or with the right `--reason` if it failed. If the metric is not a scalar, pass
   `--reproduced true|false` and say why in `--notes`.
6. Append 3–6 lines to `run.log` under `== VERDICT`: what you observed, what you compared it to,
   what you changed, what you would need to go further.

## Do not

- Do not run more than **1 seed(s)** unless the run is under 10 minutes; if it is, run 3
  and report the spread — that is more valuable than the point estimate.
- Do not substitute a different model, dataset, or judge and call it a replication. Note it as a
  follow-up in `--notes` instead.
- Do not read the post's conclusion into ambiguous output. If you cannot tell which number is
  the headline, `--reason unclear-entrypoint` and say what you saw.
- Do not push, do not open issues, do not contact the authors.
