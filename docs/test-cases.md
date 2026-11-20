# Test Cases (v3, CR-02 — single user, MacBook camera)

**Type:** M = manual, A = automated (pytest / Vitest / Playwright).

**Automated so far (Phase 2R):** TC-01, TC-02, TC-55 (`src/routes/routes.test.ts`), TC-44 (`backend/tests/test_discard.py`), TC-57 to TC-59 (`backend/tests/test_local_only.py`). The owner is the only test subject. Automated tests use synthetic images or fixtures, never real scans.

---

## A1 — Opens to the fitting room; scan, review, retake

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-01 | A | Open `/` | Fitting room loads directly; no login, sign-up, profile or consent screen exists |
| TC-02 | A | Request old routes `/login`, `/signup`, `/consent`, `/my-model`, `/try-on`, `/capture` | Removed (404) or redirected to `/` / `/scan` |
| TC-03 | M | First **Start Scan** | Privacy notice appears before the camera starts; "Don't show again" works |
| TC-07 | M | Chrome: calibration → 8 body views (auto-capture) → 5 face close-ups | All steps ≤ 4 min (Q2) |
| TC-08 | M | Same in Safari | Same as TC-07 |
| TC-09 | M | Deny camera (browser), and separately in macOS Privacy settings | Clear help for both; no crash |
| TC-20 | M | Retake one flagged view | Only that image is replaced |
| TC-51 | M | Leave `/scan` mid-way; finish a scan | Camera light turns off in both cases |

## A1/A2 — Quality checks (Flow 3)

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-10 | A | Blurry view | Rejected `blurry` for that view |
| TC-11 | A | Dark set | Rejected `too_dark` |
| TC-12 | A | Backlit set | Rejected `backlit` |
| TC-13 | A | Feet cut off | Rejected `body_cut_off` |
| TC-14 | A | Two people visible | Rejected `multiple_people` |
| TC-15 | A | No back view | Rejected `missing_view` (back) |
| TC-16 | A | 6 body views + 2 face close-ups | Rejected `too_few_photos` |
| TC-17 | A | 20 MB image | 413 |
| TC-18 | A | `.exe` renamed to `.jpg` | 415 (signature check) |
| TC-19 | A | JPEG with metadata | Stored image has no metadata |
| TC-52 | M | Center Stage ON and moving | `framing_changed` (or a warning if not detectable; see P3-02) |
| TC-53 | A | View orientation doesn't match the declared view | `wrong_view` |
| TC-54 | A | Person height differs > 8% from calibration | `distance_changed` |

## A2 — Generate 3D Model (real person, no avatar fallback)

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-21 | A | Generate on an accepted scan (fixture reconstruction) | Job queued → processing → ready; progress visible |
| TC-22 | M | Watch the fitting room during processing | Progress % updates without refresh |
| TC-23 | A | Reconstruction fails | Model `failed` + readable reason; viewer shows **no body**; no avatar/sample model loaded |
| TC-24 | A | Output with impossible height (e.g. 5 m) | Cannot become `ready` |
| TC-26 | A | Rescan and generate again | One current model; old files deleted |
| TC-55 | A | Search the generated-model code paths for any fallback to the sample/avatar GLB | None exists (`static/models/sample.glb` only used by `/viewer-demo`) |

## A3 — 360° viewer

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-27 | M | Drag a full circle, scroll to zoom | Smooth; zoom limited |
| TC-29 | M | Rotate under the floor | Camera stops at the limit |
| TC-30 | M | First load (model + outfit) | ≤ 5 s (Q7) |
| TC-31 | M | FPS while rotating | ≥ 30 (Q9) |
| TC-32 | M | Look for body/face edit controls | None exist (FR-07) |

## A4 — Shirts and pants independently

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-33 | A | Each of the 4 shirt/pants combinations | Correct garments in scene; body not reloaded |
| TC-34 | A | Change shirt only | Pants object unchanged |
| TC-35 | M | Swap a cached garment | ≤ 0.3 s (Q8) |
| TC-36 | M | Shirt = None | Shirt removed, pants stay |
| TC-37 | A | Reload the app | Last outfit restored |
| TC-38 | A | Garment file fails to load | Message shown; previous garment stays |
| TC-56 | A | Request a garment category other than top/bottom | Rejected (422) / not stored (DB check) |

## A5 — Privacy and local-only access

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-41 | A | Inspect `data/` after upload | No plaintext images/GLB (signatures not found) |
| TC-42 | A | Model asset response headers | `Cache-Control: no-store` |
| TC-44 | A | **Discard** (`DELETE /data`) | 0 scan/model/job rows and 0 blob files (Q10) |
| TC-57 | A | Request with `Host: evil.example` | Rejected (400) |
| TC-58 | A | `POST`/`PUT`/`DELETE` without `X-Fitting-Room: 1` | Rejected (403) |
| TC-59 | A | CORS preflight from another origin | No `Access-Control-Allow-*` headers |
| TC-60 | M | Backend start command | Listens on 127.0.0.1 only |
| TC-61 | M | Network panel while the camera is on | No third-party requests (NFR-03) |

## A6 — Disclosure

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-49 | A | Render the fitting room and the scan page | "Visual preview only" and model-approximation notices present |
| TC-62 | M | Review the feasibility report | F1–F11 filled; failed experiments and alternatives listed |

---

## Removed by CR-02 (kept for traceability)

TC-04 to TC-06 (consent per account), TC-25 (sign out/in), TC-28 (phone gestures for capture flow), TC-39, TC-40 (other user / logged out), TC-43, TC-45 to TC-48 (account deletion, login, consent withdrawal, login rate limit), TC-50 (pilot survey with other people). The old TC-01 to TC-03 (sign-up/login) have been **replaced** with new content under the same IDs.

## Traceability

| Acceptance item | Test cases |
|-----------------|-----------|
| A1 | TC-01–03, TC-07–20, TC-51–54 |
| A2 | TC-21–24, TC-26, TC-55 |
| A3 | TC-27, TC-29–32 |
| A4 | TC-33–38, TC-56 |
| A5 | TC-41, TC-42, TC-44, TC-57–61 |
| A6 | TC-49, TC-62 |
