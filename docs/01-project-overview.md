# 1. Project Overview (v3, CR-02, 20 Nov 2026)

> **Status:** v3 ✅ approved 20 Nov 2026. Replaces the multi-user, account-based version (history in [change-log.md](change-log.md)).

## 1.1 Goal

A web application that uses the **MacBook's built-in camera** to capture **my real body** from multiple angles, reconstructs a **3D representation of my appearance**, and lets me **virtually try on shirts and pants**.

- **Single-user personal prototype** for development and testing on my MacBook.
- The app opens **directly** to the fitting-room interface. There is no login, account or profile screen.

**Priority:** MacBook camera → multi-angle body capture → real-person 3D reconstruction → shirt/pants try-on → 360° viewer.

## 1.2 Workflow

| # | Step | Screen |
|---|------|--------|
| 1 | Open the web app on the MacBook | Fitting room (`/`) |
| 2 | Click **Start Scan** | Fitting room → Scan (`/scan`) |
| 3 | Allow camera access (short privacy notice the first time) | Scan |
| 4 | Follow on-screen instructions: turn and capture the body angles, plus face close-ups | Scan |
| 5 | Review the images and retake poor views | Scan |
| 6 | Click **Generate 3D Model** | Scan → Fitting room |
| 7 | The app processes the images and reconstructs the body as accurately as technically possible (with progress shown) | Fitting room |
| 8 | The generated model appears in the interactive 3D viewer | Fitting room |
| 9 | Select shirts and pants from the catalog | Fitting room |
| 10 | Change shirt and pants independently and rotate the model 360° | Fitting room |

At any time: **Discard scan & model** deletes the captured images and generated data.

## 1.3 Screens

| Screen | Route | Purpose |
|--------|-------|---------|
| **Fitting room** (main) | `/` | 3D viewer, Start Scan, Generate status, shirt and pants pickers, Discard |
| **Scan** | `/scan` | Full-screen guided MacBook-camera capture, review/retake, Generate 3D Model |
| Catalog (optional browse) | `/catalog` | Larger view of the shirts and pants |
| Viewer demo (dev only) | `/viewer-demo` | Tests the 3D viewer with a public sample model. Never shown as "you". |

## 1.4 Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Capture with the **MacBook built-in camera** via the browser MediaDevices API (`getUserMedia`) | Must |
| FR-02 | Guided capture of **multiple angles** (front, sides, back; 8 body views every 45°) plus face close-ups. Not a single photo. | Must |
| FR-03 | **MediaPipe** for camera guidance, pose detection and capture-quality checks | Must |
| FR-04 | Review captured images and **retake** individual poor-quality views | Must |
| FR-05 | **Generate 3D Model** button starts reconstruction; progress shown | Must |
| FR-06 | Reconstruct a 3D model of the **actual captured person**, preserving real appearance and body proportions as accurately as technically possible. **Subject to feasibility testing.** | Must (feasibility-gated) |
| FR-07 | **No generic avatar, no body reshaping, no face/body editing controls.** If reconstruction fails, show the failure and reasons, and **never silently substitute an avatar**. | Must |
| FR-08 | Interactive **360° viewer** (rotate, zoom) | Must |
| FR-09 | Catalog of **shirts and pants only**; choose and change them **independently** | Must |
| FR-10 | The generated model stays available during the session; **local persistence** on the MacBook until discarded | Must (session) / Should (persistence) |
| FR-11 | Clear **Discard scan & model** option that deletes captured images and generated data | Must |
| FR-12 | Plain-language **privacy notice** before the camera starts the first time | Must |
| FR-13 | Remember the last selected shirt and pants | Should |
| FR-14 | Save a screenshot of the current view to the Mac | Could |
| FR-15 | Size recommendations | Later (not in MVP) |

### Non-functional requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Runs on the owner's MacBook in the latest **Chrome** and **Safari** | — |
| NFR-02 | Camera images and models stay **on this MacBook**. Encrypted at rest. Backend reachable **only from localhost**. | 100% |
| NFR-03 | No third-party network requests while the camera is on | 0 requests |
| NFR-04 | Viewer smooth while rotating | ≥ 30 fps |
| NFR-05 | Readable from the scan position (~2.5 m) during capture | Instruction text ≥ 48 px |

## 1.5 Removed from scope (CR-02)

- Login, registration, authentication, user accounts
- Customer profiles, profile selection, shared-profile screen, PINs, recovery codes
- Multiple users; cloud-based profile storage
- Phone camera capture, helper-assisted scanning, phone-to-MacBook transfer
- Consent records per account (replaced by the privacy notice)
- Dresses, outerwear, shoes, accessories; realistic cloth physics (evaluated later, not promised); size recommendation

## 1.6 Technical constraints

1. **Laptop-camera images do not give accurate body measurements.** Hair, loose clothing, hidden surfaces, lighting and movement cause errors.
2. **The camera is fixed in the lid.** The person turns in place. Images are landscape and the face is small in full-body views, so close-ups are needed.
3. **An editable, garment-ready body and a raw scan are different things.** A raw scan includes the clothes worn during capture and may not support changing shirts and pants.
4. **Do not assume feasibility.** The real camera is tested first (Phase 3 Part B). Results, failed experiments and alternatives are documented in [feasibility-macbook-camera.md](feasibility-macbook-camera.md).
5. **The try-on is a visual preview**, not a size or fit measurement.

## 1.7 Success criteria

See [05-mvp-acceptance.md](05-mvp-acceptance.md).

## 1.8 Sign-off

| Item | Status |
|------|--------|
| Original requirements v1 (multi-user, phone) | Approved 20 Nov 2026, **superseded** |
| CR-01 MacBook camera | Approved 20 Nov 2026 |
| **CR-02 single-user, no authentication (this version)** | ✅ **Approved 20 Nov 2026** |
