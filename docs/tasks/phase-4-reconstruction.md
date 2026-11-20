# Phase 4 — 3D Reconstruction Proof of Concept (Weeks 6–9) ⚠️

**Goal:** Find out what 3D person representation is actually possible from **MacBook built-in camera** captures (fixed camera, person turns, 8 body views + 5 face close-ups), and pick one.

> **Updated 20 Nov 2026:** builds on the Phase 3 feasibility gate (P3-05 smoke test). With a fixed camera, **approach B (body-template fitting) is primary**, and photogrammetry is a comparison only.
**Deliverable:** Rotatable prototype model with documented limitations, plus **decision D1** (body representation).

> This is the riskiest phase. Do research tasks P4-01…P4-04 early, in parallel with Phase 2, if you can.
> Use only consenting adult test subjects or licensed sample data.

---

## Research

### P4-01 · ⚠️ Shortlist reconstruction approaches   `S`
**Depends on:** P0-07
- [ ] List candidates in 3 families:
  - **A. Photogrammetry** (comparison only): Apple Object Capture with person masks, COLMAP. Expected weak: turning person is not rigid, only one camera height
  - **B. Parametric body fitting (primary)**: fit a body template to silhouettes + 2D keypoints from the 8 views, then project the texture from the photos + face close-ups. **No reshaping beyond what the photos show; no generic avatar.**
  - **C. Video/turn-based human reconstruction** (research): only if it runs on Apple silicon with a usable license
- [ ] For each: Mac support (CUDA needed?), license (commercial OK?), input needs, output format
- [ ] Save as `docs/experiments/reconstruction-shortlist.md`

**Done when:** at least 2 approaches are selected to test, with reasons.

### P4-02 · 🔒 License check   `XS`
**Depends on:** P4-01
- [ ] Record the license of every model/tool to be tested (SMPL/SMPL-X are non-commercial unless licensed)

**Done when:** each candidate is marked "OK for prototype" and "OK for commercial: yes/no/needs license".

### P4-03 · Define evaluation scorecard   `S`
**Depends on:** P1-06
- [ ] Score 1–5: face likeness, body silhouette, mesh cleanliness (holes, noise), **can new garments be fitted** (clothing baked in?), rig-ability, compute time, file size
- [ ] Same 3 test subjects × same capture sets for all methods

**Done when:** scorecard template exists in `docs/experiments/scorecard.md`.

### P4-04 · Prepare standard test dataset   `S`
**Depends on:** P3-20
- [ ] 3 consenting adults, captured with the Phase 3 MacBook-camera workflow, good conditions
- [ ] Stored encrypted under `data/`; consent recorded

**Done when:** 3 accepted capture sessions are available.

## Experiments

### P4-05 · Approach A (comparison): Apple Object Capture with person masks   `M`
**Depends on:** P4-04
- [ ] Small Swift CLI (or sample app) in `pipeline/object-capture/` that runs `PhotogrammetrySession` on a folder
- [ ] Output USDZ → convert to GLB (Blender import USD → export glTF)
- [ ] Measure runtime and size

**Done when:** 3 models produced and scored.

### P4-06 · Approach A2: COLMAP (+ OpenMVS) — optional comparison   `M`
**Depends on:** P4-04
- [ ] Run on the same 3 datasets (CPU on Mac may be slow — record it)

**Done when:** results scored, or documented as "not practical on this Mac."

### P4-07 · Approach B (primary): Body-template fitting   `M`
**Depends on:** P4-04, P4-02
- [ ] Get pose/shape estimate from captures (MediaPipe landmarks or an image-to-body-model method that runs on Mac)
- [ ] Produce a body template mesh in the person's pose and shape
- [ ] Export GLB with skeleton

**Done when:** 3 template bodies produced and scored (silhouette + rig-ability).

### P4-08 · Approach B2: Texture the template from photos   `M`
**Depends on:** P4-07
- [ ] Project front/side/back photos onto the template UVs; blend seams
- [ ] Focus on face likeness

**Done when:** textured template models produced and scored for likeness.

### P4-09 · Approach C: Hybrid test (if A and B both partly work)   `M`
**Depends on:** P4-05, P4-07
- [ ] Align the template to the photogrammetry scan; transfer texture/detail

**Done when:** scored, or skipped with a written reason.

### P4-10 · Mesh cleanup with Blender script   `S`
**Depends on:** best result from P4-05…P4-09
- [ ] `pipeline/blender/cleanup.py` (run headless: `blender -b -P`): remove floaters, decimate to a triangle budget, fix scale (metres), Y-up, origin at feet, export GLB
- [ ] Keep the output small enough for the browser (< ~10–20 MB)

**Done when:** a script turns raw output into a viewer-ready GLB.

### P4-11 · Load results in the viewer   `XS`
**Depends on:** P4-10, P0-04
- [ ] Compare models side by side at `/viewer-demo` (local only, never in `static/` for real people)

**Done when:** all candidate GLBs rotate in the browser.

## Decision

### P4-12 · ⚠️ Compare and decide (D1, D2)   `S`
**Depends on:** P4-05…P4-11
- [ ] Fill the scorecard; pick representation + tool
- [ ] Write `docs/adr/001-body-representation.md` and `docs/adr/002-reconstruction-tool.md`
- [ ] If nothing works well enough: write what is needed (GPU, different capture, paid service) and its cost → go back to [04-risks-and-costs.md](../04-risks-and-costs.md)

**Done when:** ADRs written and the plan for Phases 5–6 is confirmed or changed.

## Integration

### P4-13 · Reconstruction adapter in backend   `M`
**Depends on:** P4-12, P3-10
- [ ] `services/reconstruction/` with an interface `run(session_id) -> glb_bytes, metrics`
- [ ] Implement the chosen method (call CLI/script via subprocess)
- [ ] Decrypt inputs to a temp dir, **delete temp files after**, encrypt outputs

**Done when:** a real job converts an accepted capture into a stored encrypted GLB.

### P4-14 · Job progress + failure handling   `S`
**Depends on:** P4-13
- [ ] Progress steps (preparing / reconstructing / cleaning / saving)
- [ ] Timeouts; clear error message on failure; model status `failed`

**Done when:** a broken input ends in `failed` with a readable reason, not a crash.

### P4-15 · Model review step   `S`
**Depends on:** P4-13
- [ ] Automatic checks: triangle count, bounding box height plausible (1.2–2.2 m), no huge holes
- [ ] Status `review` → `ready` (manual approve endpoint for admin in prototype)

**Done when:** an obviously broken model can't reach `ready`.

### P4-16 · Document limitations   `S`
**Depends on:** P4-12
- [ ] `docs/model-limitations.md`: what looks wrong (hair, hands, loose clothes, back of head), typical runtime, what users must do for best results
- [ ] Short user-facing version for the My Model screen

**Done when:** both versions are written.
