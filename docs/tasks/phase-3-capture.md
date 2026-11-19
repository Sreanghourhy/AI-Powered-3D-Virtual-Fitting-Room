# Phase 3 — Camera Capture & Upload (Weeks 4–5)

**Goal:** A guided multi-angle capture on the phone, checked for quality, uploaded securely to the MacBook.
**Deliverable:** Repeatable capture workflow with quality checks.

---

## Setup

### P3-01 · Local HTTPS so the phone can use the camera   `S`
**Depends on:** P2-18
- [ ] Browsers allow `getUserMedia` only on HTTPS (or `localhost`)
- [ ] Create a local certificate (e.g. `mkcert`), install the root CA on the phone
- [ ] Run Vite with `--host` + HTTPS; proxy API to FastAPI
- [ ] Document the steps in `docs/dev-https.md`

**Done when:** the phone opens `https://<mac-ip>:5173` without warnings and can access the camera.

## Backend

### P3-02 · Capture tables   `XS`
**Depends on:** P2-02
- [ ] `capture_sessions` and `capture_files` models + migration

**Done when:** migration applies.

### P3-03 · 🔒 Capture session + upload API   `M`
**Depends on:** P3-02, P2-05, P2-08
- [ ] `POST /captures` (requires consent)
- [ ] `POST /captures/{id}/files` (multipart; `view` field)
- [ ] Limits: max file size, max files per session, allowed MIME types + magic-byte check
- [ ] Store via encrypted `StorageService`
- [ ] Owner-only access

**Done when:** tests cover happy path, too-large file, wrong type, another user's session (404).

### P3-04 · 🔒 Strip EXIF and normalize images   `S`
**Depends on:** P3-03
- [ ] Re-encode images (Pillow; `pillow-heif` for HEIC), drop EXIF/GPS, apply orientation
- [ ] For video: store as-is for now; extract frames later (P3-07)

**Done when:** test confirms uploaded image has no EXIF after processing.

### P3-05 · Quality check: blur   `S`
**Depends on:** P3-04
- [ ] OpenCV variance of Laplacian; threshold tuned on sample images
- [ ] Save score in `quality_json`

**Done when:** blurry sample fails and sharp sample passes.

### P3-06 · Quality check: lighting / exposure   `S`
**Depends on:** P3-04
- [ ] Mean brightness + % of over/under-exposed pixels
- [ ] Simple backlight detection (subject much darker than background)

**Done when:** dark and backlit samples fail with a clear reason.

### P3-07 · Video frame extraction   `S`
**Depends on:** P3-04
- [ ] Extract sharp frames at an interval (skip blurry ones using P3-05)

**Done when:** a 30 s orbit video produces N sharp frames.

### P3-08 · Quality check: person & pose (MediaPipe)   `M`
**Depends on:** P3-04
- [ ] MediaPipe Pose Landmarker: exactly one person, full body visible (head to feet landmarks)
- [ ] Estimate facing direction (front/side/back) from shoulder/hip landmarks
- [ ] Save landmarks + estimated view in `quality_json`

**Done when:** cropped-feet and two-person samples fail; view estimates are right on the sample set.

### P3-09 · Coverage & motion check per session   `S`
**Depends on:** P3-08
- [ ] Session passes only if front, left, back, right (+ overlaps) are all covered
- [ ] Flag subject motion: big pose change between consecutive frames

**Done when:** a session missing the back view is rejected with "Back view missing."

### P3-10 · Submit endpoint   `S`
**Depends on:** P3-05…P3-09
- [ ] `POST /captures/{id}/submit` runs all checks → `accepted` or `rejected` with reasons
- [ ] On accept: create a `body_models` row + queue a reconstruction job (dummy handler until Phase 4)

**Done when:** accepted session creates a queued job; rejected returns a list of fixes.

## Frontend

### P3-11 · Camera component   `M`
**Depends on:** P3-01
- [ ] `components/capture/Camera.svelte`: rear/front camera switch, highest resolution available, capture photo to Blob
- [ ] Handle permission denied and unsupported browser

**Done when:** a photo is captured on iPhone Safari and Android Chrome.

### P3-12 · Guided capture steps UI   `M`
**Depends on:** P3-11, P1-07
- [ ] Step-by-step flow ("Step 3 of 8 — turn to your left") with silhouette overlay
- [ ] Self-timer option and "helper holds the phone" mode
- [ ] Review thumbnails and retake per step

**Done when:** a tester can complete all steps without reading the docs.

### P3-13 · Live hints in the browser (optional but helpful)   `S`
**Depends on:** P3-11
- [ ] Quick client-side brightness check before capture ("Too dark — move to a brighter place")

**Done when:** dark scenes show a warning before the photo is taken.

### P3-14 · Upload with progress + retry   `S`
**Depends on:** P3-03, P3-12
- [ ] Upload each file with a progress bar; retry on network failure
- [ ] Submit button → show accept/reject result with fix instructions

**Done when:** a full session uploads from the phone and shows the result.

### P3-15 · Test the workflow 5 times   `S`
**Depends on:** all above
- [ ] 5 sessions (different lighting/clothes) with consenting adults
- [ ] Record success rate, common failure reasons, average time to capture
- [ ] Tune thresholds; update `docs/capture-guide.md`

**Done when:** results written in `docs/experiments/capture-test-1.md` and success rate is known.
