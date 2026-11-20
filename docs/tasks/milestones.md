# Simplified Plan — 3 Milestones (CR-03, 20 Nov 2026)

> **Approved by owner 20 Nov 2026.** This is the active plan. The detailed phase files (Phase 3–8) remain as a **reference backlog**; items not listed here are postponed.

| Milestone | Owner's words | Result |
|-----------|---------------|--------|
| **1. Scan** | "Scan the body by using the camera" | `/scan` uses the MacBook camera, guides you through 8 body views + 5 face close-ups with MediaPipe auto-capture, lets you retake, and saves the photos privately (encrypted) on this Mac |
| **2. AI 3D body** | "Get that body to real 3D body reconstruction by using an AI model" | Test 2–3 AI body models on the saved photos, pick the best that runs on the M4 Pro, connect it to **Generate 3D Model**, show the result in the 360° viewer. Never a generic avatar. |
| **3. Clothes** | "Customise that body by putting on shirts or pants" | Real 3D shirts and pants fitted to the generated body, chosen independently, rotate 360° |

## Postponed (can come back later)
Voice prompts, server-side MediaPipe quality checks, consistency checks (distance/pose/framing), comparing many 3D methods, local-persistence polish, screenshots, long evaluation reports.

## Milestone 1 tasks

### M1-01 · Plan and docs   `XS` ✅
- [x] This file; change log CR-03

### M1-02 · Backend: save scans   `M`
- [ ] Tables `scans` (status capturing/saved) and `scan_images` (13 named views)
- [ ] `POST /scans`, `POST /scans/{id}/images` (JPEG/PNG, ≤ 8 MB, signature check, re-encoded without metadata, encrypted), `DELETE /scans/{id}/images/{imageId}`, `POST /scans/{id}/complete`, `GET /scans/current`
- [ ] One current scan: completing a new scan deletes the old one and its files
- [ ] Discard deletes scans and images

### M1-03 · Frontend: MediaPipe pose helpers   `M`
- [ ] `@mediapipe/tasks-vision` with WASM + pose model **self-hosted** in `static/mediapipe/` (no third-party requests while the camera is on)
- [ ] Pure helpers with tests: full body in frame, one person, stillness, facing direction estimate (front / side / back)

### M1-04 · Frontend: guided capture   `M`
- [ ] Camera (built-in, mirrored preview, unmirrored capture, always stopped on leave)
- [ ] Steps: setup → stand on your mark (full body check) → 8 body views → 5 face close-ups → review/retake
- [ ] Auto-capture: body fully visible + still ≈ 1 s → 3-2-1 countdown → photo. Click/Space works too. Facing direction is shown as a hint.

### M1-05 · Frontend: save scan   `S`
- [ ] **Save scan** uploads with progress, completes the scan, stops the camera
- [ ] Fitting room shows "Scan saved (N photos)", with Rescan and Discard. No body shown until Milestone 2.

### M1-06 · Tests, docs, owner test   `S`
- [ ] Unit + API tests; end-to-end check with Chrome's fake camera
- [ ] README how-to; **owner scans for real** and reports what happened
