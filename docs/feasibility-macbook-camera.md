# Feasibility Assessment — MacBook Built-in Camera for Multi-Angle Body Capture

> **Status:** Desk assessment, **not yet tested** (20 Nov 2026).
> Nothing here assumes the camera can produce an accurate 3D model. The Phase 3 feasibility tasks **P3-01 to P3-05** measure the real camera, and their results are added to §8. Building the full capture flow starts only after the owner approves the go/no-go decision.

## 1. Hardware available

| Item | Value | Source |
|------|-------|--------|
| Computer | MacBook Pro 14" (Mac16,8), Apple M4 Pro, 24 GB RAM | `system_profiler` |
| OS | macOS 26.6.2 | `sw_vers` |
| Camera | "MacBook Pro Camera" (built-in, top of the display lid) | `system_profiler SPCameraDataType` |
| Camera type (expected) | 12 MP Center Stage camera on this model generation | Apple spec, **to confirm in P3-01** |
| Resolution the browser receives | **Unknown.** Expected up to 1920×1080 at 30 fps. | **Measure in P3-01** |
| GPU / ML | Apple GPU (Metal) + Neural Engine; **no NVIDIA CUDA** | Hardware |

## 2. What changes compared with the phone plan

| Topic | Phone plan (old) | MacBook camera (new) |
|-------|------------------|----------------------|
| Who moves | Helper walks **around** a still person | Camera is **fixed** in the lid; the **person turns** in place |
| Views | ~40 photos, 3 heights | ~8 body views at **one height** + face close-ups |
| Helper | Required | **Not needed.** The customer captures alone. |
| Orientation | Portrait possible | **Landscape only.** About 40% of the width is wasted for a standing person. |
| Distance | 1.5–2 m | About **2.2–3 m** (full body in frame) |
| Transfer | Phone → MacBook over LAN, needs HTTPS | Captured in the **same browser** on the MacBook, uploaded to `localhost` |
| HTTPS | Required (mkcert) | **Not required** on `http://localhost` (browsers treat localhost as a secure context) |

## 3. Geometry and resolution estimate (to verify)

**Distance needed for a full body.** Covered height H ≈ 2.1 m (a 1.75 m person plus margins). Required distance d = (H / 2) / tan(vFOV / 2):

| Vertical field of view (vFOV) | Distance needed |
|-------------------|----------------|
| 55° | ≈ 2.0 m |
| 50° | ≈ 2.25 m |
| 45° | ≈ 2.55 m |

The real vFOV is measured in P3-02. Center Stage may crop the image and narrow the field of view.

**Pixels on the person at 1080p** (landscape, 1080 px tall):
- Body: ≈ 1080 × (1.75 / 2.1) ≈ **900 px tall**. This is enough for a silhouette and pose.
- Face (~0.23 m): ≈ **120 px tall / 85 px wide**. This is **too small for good face likeness**.
- So separate **face close-ups at ~0.7 m** are needed (face ≈ 500+ px).

**Camera height.** Laptop on a table (~0.75 m) plus the lid puts the camera at ~0.95 m. That is close to the body's mid-height, which is good because there is little top/bottom distortion.

## 4. Reconstruction approaches with a fixed camera

| # | Approach | Fit for a fixed camera + turning person | Assessment |
|---|----------|----------------------------------------|------------|
| A | **Photogrammetry** (Apple Object Capture, COLMAP) | Needs a **rigid** subject and many overlapping views from **several heights**. A turning person is not rigid: arms, head and clothing move. The static background must also be masked out. With only ~8 views at one height there is too little overlap. | **Unlikely to work well.** Keep as **one** low-cost comparison test only. |
| B | **Body-template fitting** (fit a parametric body to silhouettes + 2D pose keypoints from front/side/back, then project the photos as texture) | Designed for **few views**. Gives a clean, watertight, rigged body, which is needed for shirt/pants fitting. | **Most promising for the MVP.** Risks: the template's shape range may smooth out unique body features; seams in the texture; **license** (e.g. SMPL-X is non-commercial unless licensed). |
| C | **Video-based human reconstruction** (person turns slowly while recording; research methods) | Matches the turning-person setup | **Research option.** Many need CUDA and research-only licenses, and output is often not a clean mesh. Evaluate in Phase 4 only if Mac-compatible. |
| D | **Single-image "image-to-3D" generation** | Invents the back and sides | **Rejected.** It would invent appearance, which conflicts with "preserve the customer's real appearance" and "no generic replacement avatar". |

## 5. Expected outcome (honest summary)

**Likely feasible**
- A customer captures **alone**: guided front / sides / back views with live pose and orientation detection in the browser.
- Clean person masks against a plain background.
- A **360° rotatable** model whose silhouette and colours come from the customer's own photos (approach B).

**Uncertain — must be tested**
- **Face likeness.** Depends on the close-ups and how well texture projection works.
- **Consistency across views.** The person must keep the same pose and the same spot while turning.
- **Auto-exposure / white-balance shifts** as the person turns. Can the browser lock them on this camera?
- **macOS video effects** (Center Stage, Portrait, Studio Light, backgrounds) change framing and appearance. Can we detect them, or only instruct the user?
- **Processing time** on the M4 Pro.

**Not possible / never claimed**
- Accurate body measurements or size recommendations.
- Fine detail: hair volume, fingers, loose clothing.
- A model that is perfect from every angle. The try-on stays a **visual preview**.

## 6. macOS and browser specifics

| Topic | Detail | Impact |
|-------|--------|--------|
| Camera API | `navigator.mediaDevices.getUserMedia({ video: { width: {ideal: 1920}, height: {ideal: 1080}, frameRate: {ideal: 30} } })` | Read the real values with `track.getSettings()` |
| Secure context | `http://localhost` is allowed; any other host needs HTTPS | No certificates for the MVP. HTTPS returns when deployed. |
| Permissions | Browser prompt **and** macOS System Settings → Privacy & Security → Camera (per browser) | Show both fixes when access is denied |
| Camera controls | `track.getCapabilities()` may expose `exposureMode`, `whiteBalanceMode`, `focusMode`, `zoom`. Support differs by browser. | **Measure in P3-01**. If not lockable, rely on stable lighting + checks |
| **Center Stage** | Auto-pans and zooms to follow the person, so the crop changes between shots | **Must be OFF** (Control Center → Video Effects) |
| Portrait / Studio Light / Backgrounds / Reactions | Blur, relight or replace parts of the image | **Must be OFF**, because they alter real appearance |
| Mirroring | The preview is shown mirrored (natural for users) | Save frames **unmirrored** |
| Still capture | Grab a full-resolution frame from the video (canvas), or `ImageCapture.takePhoto()` if supported | Measure which gives better quality |
| Browsers | Target: latest **Chrome** and **Safari** on macOS; Firefox best-effort | Verify in P3-01 |

## 7. Proposed capture design (MVP, subject to §8 results)

1. **Setup.** Laptop on a table, plain wall behind the person, soft even light from the front. A floor marker (tape **X**) at the calibrated distance (≈ 2.5 m).
2. **Mac settings check.** Turn video effects off, close other camera apps, plug in power.
3. **Calibration.** The app checks that the whole body fits, the distance, and the brightness.
4. **8 body views** in A-pose, turning **45°** each time: front, front-right, right, back-right, back, back-left, left, front-left. The app **auto-captures** when the orientation is right and the person has been still for ~1 s. It gives big on-screen and **voice** cues, because the customer is ~2.5 m from the keyboard.
5. **Face close-ups (5)** at ~0.7 m: front, ±45°, ±90°.
6. **Review**, retake individual views, then upload to the local backend.

## 8. Go / no-go criteria (measured in P3-01 to P3-05)

| # | Check | Pass threshold | Result |
|---|-------|----------------|--------|
| F1 | Resolution delivered to the browser | ≥ 1280×720 (target 1920×1080) | _pending_ |
| F2 | Full body fits with ≥ 5% margin | at ≤ 3.0 m | _pending_ |
| F3 | Person height in frame | ≥ 700 px | _pending_ |
| F4 | Face close-up detail | distance between the eyes ≥ 100 px | _pending_ |
| F5 | Pose landmarks detected (8 views) | ≥ 95% of frames | _pending_ |
| F6 | Body orientation classified correctly | ≥ 7 of 8 views | _pending_ |
| F7 | Person mask quality (plain background) | Clean edges, judged visually | _pending_ |
| F8 | Brightness stability on the body across 8 views | varies ≤ 15% | _pending_ |
| F9 | Video effects can be turned off; framing stays fixed | Crop constant across views | _pending_ |
| F10 | Reconstruction smoke test (approach B, + A as comparison) | Owner rates silhouette and face as recognisable ≥ 3 / 5 | _pending_ |

**Decision options after P3-05**
- **Go:** build the capture flow (P3-06+).
- **Go with changes:** for example, add lighting, adjust distance or views, or use a better external USB webcam (**this needs owner approval; it is a cost and a requirement change**).
- **No-go:** stop and rethink the capture approach with the owner.

## 9. Impact on the plan

- **Phase 3** is restructured: a feasibility spike comes first (P3-01 to P3-05) and is gated by owner approval. Phone, helper and LAN-HTTPS tasks are removed.
- **Phase 4:** approach **B (template fitting) is the primary candidate**. Photogrammetry stays as one comparison test.
- **Removed from the MVP:** phone capture, helper-held capture, phone-to-MacBook transfer, local HTTPS certificates, HEIC/video uploads.
