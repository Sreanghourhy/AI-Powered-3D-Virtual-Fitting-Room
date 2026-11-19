# Phase 1 — Requirements & Prototype Design (Week 1)

**Goal:** Agree on what is built and how success is measured, before writing much code.
**Deliverable:** Approved requirements, UI mockups, test cases.

**Outputs:** [user-flows.md](../user-flows.md) · [consent-v1.md](../consent-v1.md) · [capture-steps.md](../capture-steps.md) · [garment-format.md](../garment-format.md) · [05-mvp-acceptance.md](../05-mvp-acceptance.md) (targets) · [wireframes/](../wireframes/README.md) · [test-cases.md](../test-cases.md)

---

### P1-01 · Finalize requirements list   `S` ✅
**Depends on:** —
- [x] Review [01-project-overview.md](../01-project-overview.md) FR-01…FR-09
- [x] Mark each Must / Should / Could / Later (added FR-10…FR-15 and NFR-01…NFR-05)
- [x] Write the out-of-scope list explicitly
- [x] **Owner sign-off**: approved 20 Nov 2026 (see Sign-off table in 01-project-overview.md)

**Done when:** requirements are reviewed and signed off (even if by yourself, with a date).

### P1-02 · Write user flows   `S` ✅
**Depends on:** P1-01
- [x] Flow 1: first visit → sign up → consent → capture → processing → My Model
- [x] Flow 2: return visit → sign in → Try-On → swap shirt/pants
- [x] Flow 3: delete profile
- [x] Flow 4: capture rejected → retake guidance
- [x] Save as `docs/user-flows.md` (simple text or Mermaid diagrams)

**Done when:** all 4 flows are documented, step by step.

### P1-03 · 🔒 Write consent text v1   `S` ✅
**Depends on:** P1-01
- [x] What is captured, purpose, storage location, retention ("until you delete"), deletion method, backup purge time
- [x] Adults only statement
- [x] "Visual preview, not size guarantee" disclaimer
- [x] Save as `docs/consent-v1.md`

**Done when:** text is short, plain language, and versioned (`v1`).

### P1-04 · Finalize capture instructions   `S` ✅
**Depends on:** P0-06
- [x] Turn `docs/capture-guide.md` into on-screen steps (short sentences + diagram idea per step)
- [x] Decide: photo set, video, or both for MVP
- [x] Decide required views: front, left, back, right + overlaps; min/max number of photos

**Done when:** capture steps and limits are fixed for the MVP.

### P1-05 · Define garment data format   `S` ✅
**Depends on:** —
- [x] Format: GLB, Y-up, metres, origin at feet, same scale as body model
- [x] Max triangle count and texture size (e.g. ≤ 30k tris, ≤ 2048px textures)
- [x] Metadata: id, name, category (`top`/`bottom`), thumbnail, sizes (optional), license/source
- [x] Update `src/lib/types/garment.ts` to match (MVP uses `top` and `bottom` only)
- [x] Save as `docs/garment-format.md`

**Done when:** spec exists and the TypeScript type matches it.

### P1-06 · Define success criteria with numbers   `XS` ✅
**Depends on:** P1-01
- [x] Fill in exact targets in [05-mvp-acceptance.md](../05-mvp-acceptance.md) (capture success %, load time, swap time)

**Done when:** every metric has a number.

### P1-07 · Wireframe: Capture screen   `S` ✅
**Depends on:** P1-04
- [x] Phone layout: camera preview, silhouette/pose guide overlay, step indicator (e.g. "3 of 8: turn left"), quality warnings, retake button

**Done when:** wireframe saved in `docs/wireframes/` (text wireframe, image, or Figma link).

### P1-08 · Wireframe: My Model screen   `XS` ✅
**Depends on:** P1-02
- [x] Status states (processing with progress / ready / failed), 360° preview, Rescan, Export, Delete buttons, limitations notice

**Done when:** wireframe saved.

### P1-09 · Wireframe: Catalog + Try-On screens   `S` ✅
**Depends on:** P1-02
- [x] Catalog: grid with Shirts / Pants tabs
- [x] Try-On: viewer + two independent selectors (shirt, pants) + "visual preview" label; desktop and phone layouts

**Done when:** wireframes saved for both screens, both layouts.

### P1-10 · Write test cases   `S` ✅
**Depends on:** P1-02, P1-06
- [x] One test case per MVP acceptance item (A1–A6)
- [x] Negative cases: blurry capture, dark capture, another user's model URL, deleted account login
- [x] Save as `docs/test-cases.md`

**Done when:** each acceptance item has at least one test case with steps and expected result.
