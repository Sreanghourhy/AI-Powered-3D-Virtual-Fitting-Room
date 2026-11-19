# Phase 5 — Saved Profiles & 360° Viewer (Weeks 10–11)

**Goal:** Scan once, reopen later, rotate the model.
**Deliverable:** A customer's saved GLB loads in Three.js after sign-out/sign-in, with rotate and zoom.

---

### P5-01 · body_models API   `S`
**Depends on:** P4-13
- [ ] `GET /models/me` → latest model (status, created_at, metrics, job id)
- [ ] Owner-only; 404 for others

**Done when:** tests pass for owner, other user, no model.

### P5-02 · 🔒 Secure GLB streaming   `S`
**Depends on:** P5-01
- [ ] `GET /models/{id}/asset` decrypts and streams `model/gltf-binary`
- [ ] `Cache-Control: private, no-store`; owner check
- [ ] No public URL, no file path exposed

**Done when:** owner downloads the GLB; another user gets 404; the response is not cacheable.

### P5-03 · Viewer loads private model   `S`
**Depends on:** P5-02, P0-04
- [ ] `ModelViewer` accepts a URL or an ArrayBuffer; fetch with credentials
- [ ] Loading spinner + error state

**Done when:** `/my-model` shows the user's own model.

### P5-04 · Viewer controls polish   `S`
**Depends on:** P5-03
- [ ] Orbit rotate (mouse + touch), pinch zoom, min/max zoom, no camera below floor
- [ ] Auto-frame the model (fit camera to bounding box)
- [ ] "Reset view" button; optional slow auto-rotate
- [ ] **No** controls for body or face editing (FR-08)

**Done when:** works smoothly on phone and desktop.

### P5-05 · Lighting & materials   `S`
**Depends on:** P5-03
- [ ] Environment lighting (HDR) + soft shadow; correct colour space (sRGB)

**Done when:** skin and clothing colours look natural compared to the photos.

### P5-06 · Performance   `S`
**Depends on:** P5-03
- [ ] Measure load time; enable Draco or Meshopt compression in the export step if large
- [ ] Hit the load-time target from Phase 1

**Done when:** model loads under the target on local network.

### P5-07 · Processing status UI   `S`
**Depends on:** P4-14, P2-17
- [ ] My Model shows queued / processing (progress %) / review / ready / failed
- [ ] Poll `GET /jobs/{id}` every few seconds
- [ ] Failed → reason + "Rescan" button

**Done when:** a tester can watch a job finish without refreshing.

### P5-08 · Return visit flow   `XS`
**Depends on:** P5-03
- [ ] After login, users with a `ready` model go straight to Try-On / My Model

**Done when:** sign out → sign in → same model shows, no rescan.

### P5-09 · Rescan (replace model)   `S`
**Depends on:** P5-07
- [ ] Start a new capture; old model stays until new one is `ready`, then old files are deleted

**Done when:** after rescan only one model and no orphan files remain.

### P5-10 · Limitations notice on My Model   `XS`
**Depends on:** P4-16
- [ ] Show short user-facing limitations text

**Done when:** text visible next to the viewer.

### P5-11 · E2E test: scan → save → reopen   `S`
**Depends on:** all above
- [ ] Playwright test (using a pre-made test GLB fixture instead of a real scan)

**Done when:** test passes and covers MVP items A2 and A3.
