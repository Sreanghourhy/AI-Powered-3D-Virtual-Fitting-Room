# Phase 3 — MacBook Camera Capture & Upload (Weeks 4–5+)

> **Re-planned 20 Nov 2026:** capture uses the **MacBook built-in camera** via `getUserMedia`. Phone capture, helper mode, LAN HTTPS (mkcert) and phone-to-MacBook transfer are **removed**.
> **Status:** plan waiting for owner approval. Nothing implemented yet.

**Goal:** One customer, alone, captures guided front / side / back views and face close-ups with the MacBook camera. Images are quality-checked and stored encrypted.
**Deliverable:** (1) feasibility report with go/no-go, then (2) a repeatable capture workflow with quality checks.

```text
P3-00 ─▶ P3-01 … P3-05  (feasibility spike) ─▶ 🛑 OWNER GATE ─▶ P3-06 … P3-20 (build)
```

---

## Part A — Apply the requirement change to the existing app

### P3-00 · 🔒 Update consent text and UI copy for MacBook capture   `S`
**Depends on:** approval of [consent-v2.md](../consent-v2.md)
- [ ] Consent text component → `consent-v2` wording; backend `FR_CONSENT_VERSION` default → `consent-v2` (existing v1 consents must re-consent, which the existing re-consent banner handles)
- [ ] Replace phone/helper copy: home page step 1, My Model empty state, capture placeholder checklist
- [ ] Update tests that reference `consent-v1`

**Done when:** no UI text mentions a phone or helper for capture; all tests pass.

## Part B — Feasibility spike (⚠️ measure before building)

All spike code lives on a **dev-only** route `/dev/camera-lab`. It is blocked in production builds and **saves nothing to the server**, except the sample sets the owner chooses to save in P3-05 (consenting adult, `data/samples/`).

### P3-01 · ⚠️ Camera capability probe   `S`
**Depends on:** P3-00
- [ ] List cameras; open the built-in camera with ideal 1920×1080 at 30 fps
- [ ] Record `getSettings()` (real resolution, fps, aspect) and `getCapabilities()` (exposure / white balance / focus / zoom support)
- [ ] Compare canvas frame grab vs `ImageCapture.takePhoto()` (if available): resolution, sharpness
- [ ] Run in latest Chrome and Safari
- [ ] Camera stops when leaving the page

**Done when:** results are recorded in `docs/experiments/p3-01-camera-capabilities.md`, filling feasibility checks F1 and part of F8/F9.

### P3-02 · ⚠️ Framing, distance and video-effects test   `S`
**Depends on:** P3-01
- [ ] Measure the distance needed for head-to-feet with a 5% margin; vertical FOV; person height in px (F2, F3)
- [ ] Face close-up at ~70 cm: distance between the eyes in px (F4)
- [ ] With **Center Stage ON vs OFF**: does the crop change while the person moves? Can the app detect it (e.g. background reference points shifting)? (F9)
- [ ] Note what Portrait / Studio Light do to the image

**Done when:** numbers are recorded in `docs/experiments/p3-02-framing.md`, and the recommended distance and laptop setup are confirmed.

### P3-03 · ⚠️ Lighting and exposure stability test   `S`
**Depends on:** P3-01
- [ ] Capture the 8 turn views in normal room light and in recommended light
- [ ] Measure body-region brightness and white-balance change between views (F8)
- [ ] Try locking exposure / white balance (if supported); compare

**Done when:** results are recorded, and a lighting recommendation (and whether a lock is possible) is written.

### P3-04 · ⚠️ In-browser pose, orientation and segmentation test   `M`
**Depends on:** P3-01
- [ ] Load MediaPipe Tasks Vision (Pose Landmarker + Image Segmenter) **from our own server** (no third-party CDN while the camera is on)
- [ ] At ~2.5 m: landmark detection rate (F5), orientation classifier for the 8 views (F6), mask quality (F7), frames per second on the M4 Pro
- [ ] Stillness detection (landmark movement over ~1 s)

**Done when:** results are recorded in `docs/experiments/p3-04-pose-segmentation.md` and the auto-capture rule is confirmed workable or changed.

### P3-05 · ⚠️ Sample capture + reconstruction smoke test + go/no-go   `M`
**Depends on:** P3-02, P3-03, P3-04 (absorbs P0-06 sample capture and P0-07 first experiment)
- [ ] Capture 1–2 sample sets (8 body + 5 face) of a consenting adult with the lab page → `data/samples/` (encrypted at rest, git-ignored)
- [ ] Quick test of **approach B** (template fit from silhouettes + keypoints, rough texture) and **approach A** (photogrammetry with masks) as a comparison
- [ ] Owner rates silhouette and face likeness (F10)
- [ ] Fill §8 in [feasibility-macbook-camera.md](../feasibility-macbook-camera.md); write a recommendation: **Go / Go with changes / No-go**

**Done when:** the report is complete and 🛑 **the owner approves the decision**. P3-06+ does not start before that.

## Part C — Build the capture workflow (after the gate)

### Backend

### P3-06 · Capture tables + consent-withdrawal deletion   `S`
**Depends on:** gate
- [ ] `capture_sessions` (status: capturing / checking / rejected / accepted; calibration: person height px, resolution, browser)
- [ ] `capture_files` (view: `front`, `front_right`, `right`, `back_right`, `back`, `back_left`, `left`, `front_left`, `face_front`, `face_left_45`, `face_right_45`, `face_left_90`, `face_right_90`; storage key; quality JSON)
- [ ] Withdrawing consent / deleting the account deletes captures and their blobs (completes P2-05 note)

**Done when:** the migration applies; a deletion test proves no blobs remain.

### P3-07 · 🔒 Capture session + upload API   `M`
**Depends on:** P3-06
- [ ] `POST /captures` (needs consent), `POST /captures/{id}/files` (multipart + `view`), `DELETE /captures/{id}/files/{fileId}` (retake)
- [ ] Limits: JPEG/PNG only (checked by file signature), ≤ 8 MB per image, ≤ 30 images, ≤ 150 MB per session
- [ ] Stored through encrypted `StorageService`; owner-only (404 for others)

**Done when:** tests cover the happy path, too large, wrong type, too many, another user's session.

### P3-08 · 🔒 Image normalisation   `S`
**Depends on:** P3-07
- [ ] Re-encode with Pillow; remove all metadata; cap resolution; reject unreadable images

**Done when:** a test confirms stored images have no metadata.

### P3-09 · Quality check: blur   `S`
- [ ] Variance of Laplacian on the person region; threshold from P3-05 samples

**Done when:** blurry samples fail with `blurry` and sharp ones pass.

### P3-10 · Quality check: exposure / backlight   `S`
- [ ] Brightness of the person region vs background; clipped pixels

**Done when:** dark and backlit samples fail with the right code.

### P3-11 · Quality check: person, pose and view (server)   `M`
- [ ] MediaPipe Pose (Python): one person, full body, A-pose arm angle
- [ ] Orientation matches the declared `view` → else `wrong_view`
- [ ] Face close-ups: face size check → `face_too_small`

**Done when:** sample cases for each code pass or fail correctly.

### P3-12 · Session consistency checks   `S`
- [ ] Person height within ±8% of calibration → `distance_changed`
- [ ] Arm angle within tolerance across views → `pose_changed`
- [ ] Background reference stable (framing) → `framing_changed`
- [ ] All required views present → `missing_view` / `too_few_photos`

**Done when:** each rule has a passing and a failing test.

### P3-13 · Submit endpoint   `S`
- [ ] `POST /captures/{id}/submit` runs P3-09 to P3-12 → `accepted` / `rejected` with per-view reasons
- [ ] On accept: create a `body_models` row + queue the reconstruction job (dummy handler until Phase 4)

**Done when:** an accepted session creates a queued job; a rejected one returns a fix list.

### Frontend

### P3-14 · Camera component   `M`
**Depends on:** gate
- [ ] `components/capture/Camera.svelte`: open the built-in camera (choose device), mirrored preview, unmirrored full-resolution capture
- [ ] Handle: permission denied (browser + macOS help), no camera, camera busy, unsupported browser
- [ ] Always stop all tracks when leaving or finishing (camera light off)

**Done when:** works in Chrome and Safari on the MacBook; the camera light turns off when leaving the page.

### P3-15 · Setup checklist + calibration screen   `M`
**Depends on:** P3-14, P3-04
- [ ] Step 0 checklist incl. video-effects instructions
- [ ] Live calibration: full body in frame, single person, brightness; hints "step back / closer / left / right"; store person height px

**Done when:** a tester can get a green calibration without reading the docs.

### P3-16 · Guided body views with auto-capture   `M`
**Depends on:** P3-15
- [ ] 8-view sequence with turn diagram, very large text, voice prompts (mutable), beep
- [ ] Auto-capture: right orientation + still ≥ 1 s + body in frame → countdown → capture; **Space**/click fallback
- [ ] Live per-view hints (wrong direction, moved off the X)

**Done when:** a tester completes all 8 views hands-free.

### P3-17 · Face close-up step   `S`
**Depends on:** P3-14
- [ ] Oval face guide, 5 directions, face-size hint

**Done when:** 5 usable close-ups are captured in one go.

### P3-18 · Review and retake   `S`
**Depends on:** P3-16, P3-17
- [ ] Thumbnail grid with client-side flags; retake a single view
- [ ] Images kept **only in memory**. No localStorage or IndexedDB.

**Done when:** retaking one view replaces only that image.

### P3-19 · Upload with progress, retry and result   `S`
**Depends on:** P3-07, P3-13, P3-18
- [ ] Upload each image with progress; retry on failure; submit; show the accept or reject result with fixes

**Done when:** a full session uploads and shows the result.

### P3-20 · Test the workflow 5 times   `S`
**Depends on:** all above
- [ ] 5 sessions (different clothes and lighting) with consenting adults
- [ ] Measure success rate (Q1), time (Q2), common failures; tune thresholds; update the capture guide

**Done when:** results are written in `docs/experiments/capture-test-1.md`.
