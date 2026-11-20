# Phase 5 — 360° Viewer & Local Persistence (CR-02)

> **Rewritten 20 Nov 2026 (CR-02):** no profiles or accounts. One current model stored locally until Discard.

**Goal:** Show the generated model of the real person in a smooth 360° viewer, and keep it available across reloads and restarts until discarded.
**Deliverable:** The generated model loads in the fitting room, rotates and zooms, and is still there after a restart.

---

### P5-01 · Current model API   `S`
**Depends on:** P4-13
- [ ] `GET /models/current` → status, created_at, metrics, failure reason, job id (404 when none)

**Done when:** tests cover none / processing / ready / failed.

### P5-02 · 🔒 GLB streaming from localhost   `S`
**Depends on:** P5-01
- [ ] `GET /models/current/asset` decrypts and streams `model/gltf-binary`, `Cache-Control: no-store`; no file paths exposed

**Done when:** the GLB downloads via the app; the response can't be cached.

### P5-03 · Viewer loads the generated model   `S`
**Depends on:** P5-02, P2R-05
- [ ] `ModelViewer` loads the private URL; loading and error states
- [ ] On error: show the error. **Never fall back to the sample model.**

**Done when:** the fitting room shows the generated model.

### P5-04 · Viewer controls polish   `S`
- [ ] Orbit rotate, zoom limits, no camera below the floor, auto-frame, Reset view, optional auto-rotate
- [ ] No body/face edit controls (FR-07)

**Done when:** smooth on the MacBook in Chrome and Safari.

### P5-05 · Lighting and colour accuracy   `S`
- [ ] HDR environment, soft shadow, sRGB output; compare skin and clothing colour with the captured photos

**Done when:** colours look true to the photos (owner judgement).

### P5-06 · Performance   `S`
- [ ] Meshopt/Draco compression if large; load ≤ 5 s (Q7), ≥ 30 fps (Q9)

**Done when:** targets met or the gap is documented.

### P5-07 · Generation progress UI   `S`
**Depends on:** P4-14
- [ ] Fitting room polls `GET /jobs/{id}`: queued / processing % / ready / failed (with reason, Try again / Rescan)

**Done when:** a job can be watched to the end without refreshing.

### P5-08 · Local persistence and rescan   `S`
**Depends on:** P5-03
- [ ] After restarting backend + browser, the current model and outfit reappear
- [ ] Rescan: old model kept until the new one is `ready`, then old files deleted (one current model)

**Done when:** restart test passes; no orphan files after a rescan.

### P5-09 · E2E test: scan fixture → generate → reload   `S`
- [ ] Playwright using a fixture GLB instead of a real scan

**Done when:** covers A2 (fixture path) and A3.
