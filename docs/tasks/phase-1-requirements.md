# Phase 1 — Requirements & Prototype Design (Week 1)

**Goal:** Agree on what is built and how success is measured, before writing much code.
**Deliverable:** Approved requirements, UI mockups, test cases.

---

### P1-01 · Finalize requirements list   `S`
**Depends on:** —
- [ ] Review [01-project-overview.md](../01-project-overview.md) FR-01…FR-09
- [ ] Mark each Must / Should / Later
- [ ] Write the out-of-scope list explicitly

**Done when:** requirements are reviewed and signed off (even if by yourself, with a date).

### P1-02 · Write user flows   `S`
**Depends on:** P1-01
- [ ] Flow 1: first visit → sign up → consent → capture → processing → My Model
- [ ] Flow 2: return visit → sign in → Try-On → swap shirt/pants
- [ ] Flow 3: delete profile
- [ ] Flow 4: capture rejected → retake guidance
- [ ] Save as `docs/user-flows.md` (simple text or Mermaid diagrams)

**Done when:** all 4 flows are documented, step by step.

### P1-03 · 🔒 Write consent text v1   `S`
**Depends on:** P1-01
- [ ] What is captured, purpose, storage location, retention ("until you delete"), deletion method, backup purge time
- [ ] Adults only statement
- [ ] "Visual preview, not size guarantee" disclaimer
- [ ] Save as `docs/consent-v1.md`

**Done when:** text is short, plain language, and versioned (`v1`).

### P1-04 · Finalize capture instructions   `S`
**Depends on:** P0-06
- [ ] Turn `docs/capture-guide.md` into on-screen steps (short sentences + diagram idea per step)
- [ ] Decide: photo set, video, or both for MVP
- [ ] Decide required views: front, left, back, right + overlaps; min/max number of photos

**Done when:** capture steps and limits are fixed for the MVP.

### P1-05 · Define garment data format   `S`
**Depends on:** —
- [ ] Format: GLB, Y-up, metres, origin at feet, same scale as body model
- [ ] Max triangle count and texture size (e.g. ≤ 30k tris, ≤ 2048px textures)
- [ ] Metadata: id, name, category (`top`/`bottom`), thumbnail, sizes (optional), license/source
- [ ] Update `src/lib/types/garment.ts` to match (MVP uses `top` and `bottom` only)
- [ ] Save as `docs/garment-format.md`

**Done when:** spec exists and the TypeScript type matches it.

### P1-06 · Define success criteria with numbers   `XS`
**Depends on:** P1-01
- [ ] Fill in exact targets in [05-mvp-acceptance.md](../05-mvp-acceptance.md) (capture success %, load time, swap time)

**Done when:** every metric has a number.

### P1-07 · Wireframe: Capture screen   `S`
**Depends on:** P1-04
- [ ] Phone layout: camera preview, silhouette/pose guide overlay, step indicator (e.g. "3 of 8: turn left"), quality warnings, retake button

**Done when:** wireframe saved in `docs/wireframes/` (image or Figma link).

### P1-08 · Wireframe: My Model screen   `XS`
**Depends on:** P1-02
- [ ] Status states (processing with progress / ready / failed), 360° preview, Rescan, Export, Delete buttons, limitations notice

**Done when:** wireframe saved.

### P1-09 · Wireframe: Catalog + Try-On screens   `S`
**Depends on:** P1-02
- [ ] Catalog: grid with Shirts / Pants tabs
- [ ] Try-On: viewer + two independent selectors (shirt, pants) + "visual preview" label; desktop and phone layouts

**Done when:** wireframes saved for both screens, both layouts.

### P1-10 · Write test cases   `S`
**Depends on:** P1-02, P1-06
- [ ] One test case per MVP acceptance item (A1–A6)
- [ ] Negative cases: blurry capture, dark capture, another user's model URL, deleted account login
- [ ] Save as `docs/test-cases.md`

**Done when:** each acceptance item has at least one test case with steps and expected result.
