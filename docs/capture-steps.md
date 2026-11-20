# Capture Steps — On-Screen Flow (MVP, MacBook camera)

> **Changed 20 Nov 2026:** replaces the phone + helper flow. Numbers are proposals until the feasibility gate (P3-05) confirms them.

These are the steps the **Capture** screen (`/capture`) shows on the MacBook. The detailed rules are in [capture-guide.md](capture-guide.md).

## MVP decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Camera | **MacBook built-in camera** via `getUserMedia` in the browser | Owner requirement (20 Nov 2026) |
| Who operates | **The customer alone.** No helper. | Fixed camera; hands-free auto-capture |
| Photos or video | **Still frames** grabbed from the live video at full resolution | Each view can be checked and retaken one at a time |
| Body views | **8**, one every 45° (front, front-right, right, back-right, back, back-left, left, front-left) | Covers front, sides and back with overlap between neighbours |
| Face close-ups | **5** at ~70 cm (front, ±45°, ±90°) | Body views are too far away for face detail |
| Capture trigger | **Auto-capture** when the orientation is right and the person is still ≥ 1 s. Keyboard **Space** / click as a fallback. | The customer is ~2.5 m from the keyboard |
| Cues | Large on-screen text readable at 3 m + **voice** prompts (browser speech) + a beep on capture | Customer can't read small text from the marker |
| Preview | Mirrored on screen; saved images **not** mirrored | Natural for the user; correct for reconstruction |
| Image count | **Min 11** (8 body + 3 face) / **target 13** / **max 30** | Retakes allowed |
| Formats | JPEG (quality ~0.92) or PNG, from the browser | No HEIC or video needed |
| Max size | 8 MB per image, 150 MB per session | 1080p JPEGs are ~0.5–1.5 MB |
| Required views (quality check) | All 8 body views + face front | Coverage check |
| Time target | ≤ **4 minutes** for a first-time user | Measured in P3-20 |
| Browsers | Latest Chrome and Safari on macOS | Verified in P3-01 |

## Screens and text

### Step 0 — Setup checklist
> **Get ready (1 minute)**
> ☐ Laptop on a table, nothing moving behind you
> ☐ Bright, even light in front of you. No window behind you.
> ☐ Fitted, plain clothes. Hair tied back. No glasses or hat.
> ☐ **Video effects off:** Control Center → Video Effects → Center Stage, Portrait, Studio Light **off**
> ☐ A marked spot (X) about 2.5 m from the laptop
>
> [ Start camera ]

### Step 1 — Camera access
Browser permission prompt. If denied: *"Allow camera access for this site in your browser, and in System Settings → Privacy & Security → Camera."*
If several cameras exist, the built-in camera is selected by default and the user can change it.

### Step 2 — Calibration
> **Stand on your X and face the screen**
> The live preview shows a body outline. It turns green when:
> - head and feet are inside the frame with a margin
> - you are the only person visible
> - the brightness is OK
>
> Hints: *"Step back a little"* · *"Step closer"* · *"Move left"* · *"Too dark"*

The app stores the person's pixel height here, to check that the distance stays the same in every view.

### Step 3 — Pose
> **A-pose: arms slightly away from your body, feet apart, look ahead.** (illustration)

### Step 4 — Body views (8, auto-capture)
> **View 1 of 8 — Face the screen**
> HOLD STILL … ● *beep* ✓
> **View 2 of 8 — Turn a quarter-left… a little more (45°)** *(top-down turn diagram)*

Auto-capture rule: correct orientation for this view + still ≥ 1 s + full body visible → 1 s countdown → capture.

### Step 5 — Face close-ups (5)
> **Come closer (about 70 cm). Sitting is fine.**
> Front · turn a little left · a little right · left side · right side

### Step 6 — Review
> **Check your photos** — 8 body + 5 face thumbnails. Warning icon on any the app flags (blurry, dark, wrong direction). Click to retake that one.
> [ **Upload** ]

### Step 7 — Upload
> **Uploading 9 of 13…** (progress bar). *Keep this page open.*

### Step 8 — Result
- Accepted: *"Great, your photos look good. We're building your 3D model now. This can take several minutes, and you can leave this page."* → My Model
- Rejected: list of problems + fixes → [Flow 4](user-flows.md#flow-4--capture-rejected--retake)

**Leaving the page or finishing always stops the camera** (the camera light turns off).

## Problem messages (shared with backend reasons)

| Code | Message |
|------|---------|
| `blurry` | "The {view} photo is blurry. Hold still until you hear the beep." |
| `too_dark` | "Photos are too dark. Add light in front of you." |
| `backlit` | "There is strong light behind you. Turn off or cover the light behind you." |
| `body_cut_off` | "Your head or feet are outside the frame in the {view} photo. Step back to your X." |
| `multiple_people` | "More than one person is visible. Only the person being scanned should be in view." |
| `wrong_view` | "The {view} photo shows the wrong direction. Retake it and follow the turn diagram." |
| `missing_view` | "We still need your {view} view." |
| `distance_changed` | "You moved closer or further away in the {view} photo. Stand on your X and retake it." |
| `pose_changed` | "Your arm position changed in the {view} photo. Keep the same A-pose and retake it." |
| `framing_changed` | "The camera framing changed between photos. Turn off Center Stage and start again." |
| `face_too_small` | "Your face is too small in the close-up. Come closer to the screen." |
| `too_few_photos` | "We need at least 8 body views and 3 face close-ups." |
