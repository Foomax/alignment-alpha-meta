# lessons-16 — from R8b (2026-08-27 22:10)

New:
1. **A chain that fails at its last step may have already produced the headline.** The plateau/freeze plots (steps 15–18) were done; only the final Jacobian script (step 22) OOM'd. Check which artefacts exist before treating a non-zero chain exit as a failure — grep the chain script for the step that makes the `headline_artifact` and see if its output is present.
2. **Reading the plot images is the correct tool for a qualitative curve-shape claim.** "MLP-frozen eliminates the plateau" is a statement about three curves; three image reads settled it more convincingly than any number. Use it when the claim is visual and the repo saves only PNGs — but delete the underlying tensors afterward.
3. **`bash -e` chains that dump activations are a disk risk mid-run.** R8b wrote ~35 GB of `.pt` interpolation tensors during the run (disk dropped to 30 GB); the plots are the artefact. Delete `src/activations` (or the repo's intermediate dir) immediately after judging, before the next node preps.
4. **A vmap'd full-residual Jacobian of a large model will OOM on 24 GB** even when the rest of the pipeline fits; that sub-step is `vram`/UNRESOLVED, not a failure of the headline.

Confirmed: lessons-3 #1 & lessons-7 #2 (judge from artefacts), lessons-6 #3 (compound claim split across scripts), lessons-8 #5 (intermediates are not results).
