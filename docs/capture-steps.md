# Capture Steps — On-Screen Flow (MVP)

These are the steps the **Capture** screen shows. They come from the detailed [capture-guide.md](capture-guide.md).

## MVP decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Photos or video? | **Photos** for the MVP. Video is a later option. | Each photo can be checked and retaken one at a time, and photos are sharper than video frames. |
| Who holds the phone? | **A helper** walks around. The scanned person stands still. | If the person turns themselves, their body moves, which breaks reconstruction. |
| Positions per ring | **12** (every 30°) | Simple clock-face guidance ("move to 1 o'clock") with enough overlap |
| Rings | **3**: chest height, above head (tilted down), knee height (tilted up) | Covers the top of the shoulders/head and the lower legs |
| Face close-ups | **4**: front, left, right, slightly below | Improves face likeness |
| Photo count | **Min 36 / target 40 / max 80** | 36 = 3 rings × 12. Extra photos allowed for problem areas. |
| Required views (quality check) | front, left, back, right must each have ≥ 3 sharp photos | Coverage check in P3-09 |
| Max file size | 15 MB per photo, 600 MB per session | Fits 4K JPEG/HEIC |
| Time target | ≤ 6 minutes for a first-time user | Measured in P3-15 |

> A "self mode" (phone on a tripod, person turns) may be added later **only if** Phase 4 picks a body-template method that needs fewer views.

## Screens and text

### Step 0 — Setup checklist
> **Get ready (1 minute)**
> ☐ Bright room, no window behind you
> ☐ Fitted, plain clothes. Hair tied back. No glasses or hat.
> ☐ About 2.5 m of free space around you
> ☐ A helper to hold the phone
>
> [ Start ]

### Step 1 — Pose
> **Stand like this and stay still**
> *(A-pose illustration)*
> Arms slightly away from your body, feet shoulder-width apart, look straight ahead.
> **Helper:** stand 1.5–2 m away so the whole body fits inside the outline.

The silhouette overlay must fit head-to-feet. The **Next** button turns on only when MediaPipe sees the full body (Phase 3).

### Step 2 — Ring 1: chest height (12 photos)
> **Ring 1 of 3 — Hold the phone at chest height**
> *(clock diagram, current position highlighted)*
> **Photo 1 of 12 — Front (12 o'clock).** Tap to capture.
> → then: *"Take one step to the right, to 1 o'clock."*

### Step 3 — Ring 2: above head (12 photos)
> **Ring 2 of 3 — Raise the phone above head height and tilt it down slightly**

### Step 4 — Ring 3: knee height (12 photos)
> **Ring 3 of 3 — Hold the phone at knee height and tilt it up slightly**

### Step 5 — Face (4 photos)
> **Face close-ups — come closer (about 60 cm)**
> Front · left side · right side · slightly from below

### Step 6 — Review
> **Check your photos**
> Grid of thumbnails, with a warning icon on any photo the phone thinks is dark or blurry.
> Tap a photo to retake it. [ **Upload** ]

### Step 7 — Upload
> **Uploading 23 of 40…** (progress bar)
> *Keep this page open.*

### Step 8 — Result
- Accepted: *"Great, your photos look good. Building your 3D model now. This can take several minutes. You can leave this page; we'll keep working."* → My Model
- Rejected: list of problems + fixes → [Flow 4](user-flows.md#flow-4--capture-rejected--retake)

## Problem messages (shared with backend reasons)

| Code | Message |
|------|---------|
| `blurry` | "Photo {n} is blurry. Hold the phone still and tap the person to focus." |
| `too_dark` | "Photos are too dark. Move to a brighter place or turn on more lights." |
| `backlit` | "There is strong light behind you. Turn so the window is behind the helper." |
| `body_cut_off` | "Photo {n} doesn't show the whole body. Step back until head and feet fit in the outline." |
| `multiple_people` | "More than one person is visible. Make sure only the scanned person is in the photo." |
| `missing_view` | "We need more photos of your {side}. Retake ring positions {list}." |
| `person_moved` | "The pose changed during the capture. Please restart and stay still." |
| `too_few_photos` | "We need at least 36 photos. You have {n}." |
