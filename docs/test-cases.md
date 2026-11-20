# Test Cases (v1)

Each MVP acceptance item (A1–A6 in [05-mvp-acceptance.md](05-mvp-acceptance.md)) has at least one test case. **Type:** M = manual, A = automated (pytest / Playwright).

Test data: consenting adult testers, or the CC BY sample model. Never use real customer data in automated tests.

---

## A1 — Account, consent, guided capture & upload

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-01 | A | Sign up with new email + valid password | 201; session cookie set (`HttpOnly`, `Secure`, `SameSite=Lax`) |
| TC-02 | A | Sign up with an existing email | 409; no second account |
| TC-03 | A | Log in with wrong password | 401; generic message ("Email or password is wrong") |
| TC-04 | A | Open `/capture` without consent | Redirect to `/consent`; API capture endpoints return 403 |
| TC-05 | M | Consent screen: tick only one box | "Agree" stays disabled |
| TC-06 | A | Accept consent | Record stored with `consent-v1` + timestamp |
| TC-07 | M | MacBook, **Chrome**: customer alone completes calibration, 8 body views (auto-capture) and 5 face close-ups | All steps ≤ 4 min (Q2); upload progress shown; result screen appears |
| TC-08 | M | Same on MacBook **Safari** | Same as TC-07 |
| TC-09 | M | Deny camera permission (browser), and separately in macOS Privacy settings | Clear message with both fixes; no crash |
| TC-51 | M | Leave the capture page mid-way, and finish a capture | Camera light turns off in both cases |
| TC-52 | M | Capture with **Center Stage ON** and move during views | Rejected with `framing_changed` (or warning if not detectable; see P3-02) |
| TC-53 | A | Upload a view whose body orientation doesn't match the declared view | Rejected with `wrong_view` |
| TC-54 | A | Upload a set where the person height differs > 8% from calibration in one view | Rejected with `distance_changed` for that view |

## A1 — Negative capture cases (Flow 4)

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-10 | A | Submit session with a deliberately blurry photo | Rejected with `blurry` for that photo number |
| TC-11 | A | Submit a dark set (low brightness) | Rejected with `too_dark` |
| TC-12 | A | Submit a backlit set | Rejected with `backlit` |
| TC-13 | A | Submit a set with feet cut off | Rejected with `body_cut_off` |
| TC-14 | A | Submit a set with two people visible | Rejected with `multiple_people` |
| TC-15 | A | Submit a set with no back view | Rejected with `missing_view` (back) |
| TC-16 | A | Submit 6 body views and 2 face close-ups | Rejected with `too_few_photos` |
| TC-17 | A | Upload a 20 MB image | 413 |
| TC-18 | A | Upload a `.exe` renamed to `.jpg` | 415 (magic-byte check) |
| TC-19 | A | Upload a JPEG containing metadata (e.g. EXIF/GPS) | Stored file has no metadata |
| TC-20 | M | Retake only the flagged photos and resubmit | Accepted; only retaken photos were re-uploaded |

## A2 — Model generated, reviewed, saved, reopened

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-21 | A | Accepted session → job runs (fixture reconstruction) | Status goes queued → processing → review → ready |
| TC-22 | M | Watch My Model during processing | Progress % updates without refresh |
| TC-23 | A | Reconstruction fails (broken input) | Status `failed` with readable reason; "Rescan" shown |
| TC-24 | A | Model with impossible height (e.g. 5 m) | Cannot reach `ready` |
| TC-25 | A | Sign out → sign in → open My Model | Same model id loads; no rescan needed |
| TC-26 | A | Rescan, then new model becomes ready | Only one model exists; old files deleted |

## A3 — 360° viewer

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-27 | M | Desktop: drag to rotate a full circle, scroll to zoom | Smooth rotation; zoom limited (can't go inside model or too far) |
| TC-28 | M | Phone: one-finger rotate, pinch zoom | Same as TC-27; page doesn't scroll while rotating |
| TC-29 | M | Rotate under the floor | Camera stops at the limit |
| TC-30 | M | Measure first load (model + 1 outfit) on local network | ≤ 5 s (Q7) |
| TC-31 | M | FPS while rotating on a mid-range phone | ≥ 30 fps (Q9) |
| TC-32 | M | Check UI for body/face edit controls | None exist (FR-08) |

## A4 — 2 shirts × 2 pants, independently

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-33 | A | Select each of the 4 shirt/pants combinations | Correct garment ids in scene; body not reloaded |
| TC-34 | A | Change shirt only | Pants object unchanged (same instance) |
| TC-35 | M | Swap a cached garment | ≤ 0.3 s (Q8) |
| TC-36 | M | Select ∅ for shirt | Shirt removed, pants stay |
| TC-37 | A | Leave and return | Last outfit restored |
| TC-38 | A | Garment GLB fails to load | Toast shown; previous garment stays |

## A5 — Privacy and deletion

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-39 | A | User B requests user A's model metadata, asset, capture, job | 404 for every endpoint (no existence leak) |
| TC-40 | A | Request model asset while logged out | 401 |
| TC-41 | A | Inspect `data/` after upload | No plaintext images/GLB (magic bytes not found) |
| TC-42 | A | Asset response headers | `Cache-Control: private, no-store` |
| TC-43 | A | Delete 3D model only | Model + captures gone; account remains; can rescan |
| TC-44 | A | Delete account | 0 DB rows and 0 files for that user (Q11); session invalid |
| TC-45 | A | Log in with deleted account | 401 |
| TC-46 | A | Withdraw consent | Captures and models deleted; capture locked |
| TC-47 | A | Export my data | ZIP contains account JSON, consent history, model GLB |
| TC-48 | A | 20 rapid failed logins | 429 after the limit |

## A6 — Disclosure

| ID | Type | Steps | Expected result |
|----|------|-------|-----------------|
| TC-49 | A | Render Consent, My Model, Try-On | Each shows its disclaimer text exactly as in consent-v1 |
| TC-50 | M | Pilot survey: "Does the try-on show your exact size?" | ≥ 90% answer "No" (Q12) |

---

## Traceability

| Acceptance item | Test cases |
|-----------------|-----------|
| A1 | TC-01 … TC-20, TC-51 … TC-54 |
| A2 | TC-21 … TC-26 |
| A3 | TC-27 … TC-32 |
| A4 | TC-33 … TC-38 |
| A5 | TC-39 … TC-48 |
| A6 | TC-49, TC-50 |
