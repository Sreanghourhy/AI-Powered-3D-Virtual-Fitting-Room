# P3-01 — MacBook Camera Capability Probe

> **Status:** tool ready (20 Nov 2026). **Waiting for the owner's real-camera runs** in Chrome and Safari.
> Tool: `/dev/camera-lab` (development only; 404 in production builds). It sends nothing to any server and keeps no images.

## How to run (owner, ~2 minutes per browser)

1. Turn **off** Control Center → Video Effects (Center Stage, Portrait, Studio Light, Reactions, backgrounds).
2. Start the app: `npm run dev:api` and `npm run dev`.
3. Open **http://localhost:5173/dev/camera-lab** in **Chrome**, click **Run camera test**, allow the camera.
4. Wait about 15 s until "Done. The camera is now off." Then click **Download report (.json)**. The file is `camera-report-chrome.json` in Downloads.
5. Repeat in **Safari** (`camera-report-safari.json`).
6. Tell Claude the files are in Downloads (or paste their contents). They contain no images, only numbers and the browser/camera names.

## What the probe measures

| Item | Why it matters | Feasibility check |
|------|----------------|-------------------|
| Resolution delivered for 4K / 1440p / 1080p / 720p requests | Pixels on body and face | **F1** |
| Real frame rate (3 s count) | Smooth live guidance, motion blur | — |
| Canvas still vs `ImageCapture.takePhoto()` (size, sharpness, JPEG size) | Which capture method to use | — |
| `getCapabilities()`: exposure, white balance, focus, zoom… | Can exposure/white balance be locked (P3-03)? | F8 (input) |
| Supported constraints | Browser differences | — |

## Tool self-test (fake camera, NOT the MacBook)

Headless Chrome with its built-in **fake** camera (`--use-fake-device-for-media-stream`), only to check the tool works:

| Check | Result |
|-------|--------|
| Ladder 4K / 1440p / 1080p / 720p | 1920×1080 / 1920×1080 / 1920×1080 / 1280×720 @ 20 fps |
| Measured fps | ~20 |
| Canvas still | 1920×1080, works |
| `takePhoto()` | works in Chrome |
| Camera off at the end | yes |

These numbers describe the fake device and say **nothing** about the MacBook camera.

## Results — MacBook Pro Camera (to be filled from the reports)

| Item | Chrome | Safari |
|------|--------|--------|
| Browser version | | |
| Camera label | | |
| 4K request → delivered | | |
| 1440p request → delivered | | |
| 1080p request → delivered | | |
| 720p request → delivered | | |
| Measured fps | | |
| Canvas still: size / sharpness / JPEG KB | | |
| `takePhoto()`: size / sharpness / JPEG KB or error | | |
| exposureMode options | | |
| whiteBalanceMode options | | |
| focusMode options | | |
| zoom | | |
| **F1 (≥ 1280×720)** | | |

## Conclusions (after the runs)

- _pending_
