# Phase 6 — Clothing Catalog & Try-On (Weeks 12–16+)

**Goal:** Switch shirts and pants independently on a saved model.
**Deliverable:** Selectable shirt + pants combinations on a saved model (at least 2 × 2).

> How garments are fitted depends on decision **D1** from Phase 4.
> - If the body is a **template fitted to my scan, with a skeleton** → rig garments once to the same skeleton (skinned meshes), and they follow my real proportions.
> - If the body is a **raw scan** → garments need alignment per scan, and the original clothes will show through. Expect weaker results.
> **CR-02:** single user, garments shown in the fitting room at `/`; shirts and pants only.

---

## Garment assets

### P6-01 · Get 2 shirts + 2 pants (licensed)   `M`
**Depends on:** P1-05
- [ ] Source or model 4 garments (free with license that allows use, or made in Blender)
- [ ] Record source + license in `pipeline/garments/LICENSES.md`

**Done when:** 4 garment source files are available.

### P6-02 · Garment preparation script   `M`
**Depends on:** P6-01
- [ ] `pipeline/blender/prepare_garment.py`: scale to metres, Y-up, origin at feet, decimate to budget, bake textures, export GLB
- [ ] Generate thumbnail render

**Done when:** each garment → GLB + thumbnail meeting the garment spec.

### P6-03 · Rig garments to the body skeleton   `M`
**Depends on:** P6-02, P4-12 (only if template approach)
- [ ] Transfer skin weights from the template body to each garment (Blender Data Transfer)
- [ ] Check deformation in a few poses

**Done when:** garments deform with the template without major clipping.

### P6-04 · Upload garments to catalog   `XS`
**Depends on:** P6-02
- [ ] Replace placeholder seed data with real GLBs + thumbnails
- [ ] Garment files are public catalog assets (OK to serve statically)

**Done when:** catalog shows the 4 real garments.

## Try-on engine

### P6-05 · Load garment on top of body   `S`
**Depends on:** P5-03, P6-04
- [ ] Viewer loads body + one garment GLB into the same scene
- [ ] Bind skinned garment to the body skeleton (template) **or** apply alignment transform (scan)

**Done when:** one shirt shows on the test model.

### P6-06 · Independent shirt & pants slots   `S`
**Depends on:** P6-05
- [ ] Two slots: `top`, `bottom`; swapping one does not reload the body or the other slot
- [ ] Cache loaded garment GLBs in memory

**Done when:** all 4 combinations switch in under the target swap time.

### P6-07 · Alignment using landmarks (scan path or fine-tuning)   `M`
**Depends on:** P6-05
- [ ] Use stored body landmarks (shoulders, hips, waist) to scale/position garments
- [ ] Offsets saved with the current model

**Done when:** garments sit at shoulders/waist on all 3 test subjects.

### P6-08 · Hide body under clothing (reduce clipping)   `S`
**Depends on:** P6-06
- [ ] Hide or shrink body regions covered by the garment (mask by body part / vertex groups)

**Done when:** no visible skin poking through the 4 garments on test models.

### P6-09 · Layering order   `XS`
**Depends on:** P6-06
- [ ] Decide shirt tucked/untucked rule (MVP: shirt over pants); render order/offset

**Done when:** waist area looks consistent in all 4 combinations.

### P6-10 · ⚠️ Evaluate cloth simulation need   `S`
**Depends on:** P6-06…P6-09
- [ ] Score current results; list garments that look wrong
- [ ] Decide: rigid/skinned is enough for MVP, or try offline simulation (e.g. Blender cloth bake per model) later
- [ ] Write `docs/adr/003-garment-fitting.md` (decision D5)

**Done when:** decision recorded.

## UI

### P6-11 · Try-On selectors connected   `S`
**Depends on:** P6-06, P2-16
- [ ] Shirt and pants pickers (thumbnails) update the viewer
- [ ] "None" option for each slot

**Done when:** shirt and pants switch independently in the fitting room.

### P6-12 · Outfit save   `S`
**Depends on:** P6-11
- [ ] Single-row `outfit` table + `GET/PUT /outfit`; restore on reload

**Done when:** the last outfit reappears after reloading the app.

### P6-13 · Catalog → Try-On link   `XS`
**Depends on:** P6-11
- [ ] "Try on" button on a catalog card opens Try-On with that garment selected

**Done when:** works for shirts and pants.

### P6-14 · "Visual preview" disclosure   `XS`
**Depends on:** P6-11
- [ ] Persistent label + info popup: not a size or fit guarantee

**Done when:** visible on Try-On on phone and desktop.

### P6-15 · Screenshot / share image (optional)   `S`
**Depends on:** P6-11
- [ ] Download a PNG of the current view (stays on device; no upload)

**Done when:** PNG downloads.

### P6-16 · E2E test: 2 × 2 combinations   `S`
**Depends on:** all above
- [ ] Playwright: select each of 4 combinations; check the correct garment ids are loaded

**Done when:** covers MVP item A4.
