# 1. Project Overview

## 1.1 Vision

Build a virtual clothing fitting system based on the **customer's own appearance**.

1. Capture the person **once** with the **MacBook's built-in camera** (in the browser) from the front, sides and back, plus face close-ups.
2. Reconstruct an approximate 3D representation of that person.
3. Save it securely until the customer deletes it.
4. Let the customer try shirts and pants again and again in a **360° viewer**.

The app must **not** offer controls to change the customer's face or body proportions. It is the real person, not an avatar editor.

## 1.2 Users and main flows

| User | Main flow |
|------|-----------|
| Customer | Sign up → give consent → guided capture **alone in front of the MacBook camera** → wait for processing → review model → try on outfits → come back later → delete profile if wanted |
| Admin / developer | Manage garment catalog → review failed reconstructions → monitor jobs |

### Screens (from Phase 1 wireframes)

| Screen | Purpose |
|--------|---------|
| **Sign in / Sign up** | Account access |
| **Consent** | Explain what is captured, stored, for how long, and how to delete |
| **Capture** | Guided front / side / back capture with the MacBook built-in camera: auto-capture, voice + large on-screen cues, face close-ups |
| **My Model** | Processing status, 360° preview of the saved model, delete/export buttons |
| **Catalog** | Browse shirts and pants |
| **Try-On** | 360° viewer with independent shirt and pants selectors |

## 1.3 Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Capture front, side and back views (8 body views every 45°) plus face close-ups with the **MacBook's built-in camera**, accessed in the web app via the browser MediaDevices API (`getUserMedia`). The MacBook also runs processing. | Must |
| FR-02 | Create a 3D representation that preserves the person's original appearance as closely as technically possible — no fantasy avatar | Must |
| FR-03 | Display the saved model in an interactive 360° viewer (rotate, zoom) | Must |
| FR-04 | Choose and change shirts and pants **independently** from a catalog; support outfit combinations | Must |
| FR-05 | Reuse a saved 3D profile without rescanning for each clothing change | Must |
| FR-06 | Store the profile until the customer requests deletion, with informed consent and applicable privacy rules | Must |
| FR-07 | Customer can view, export (where feasible) and delete their profile; access restricted to their own data | Must |
| FR-08 | No body reshaping, no face/body editing controls, and no generic replacement avatar | Must |
| FR-09 | Size recommendations | Later (optional) |
| FR-10 | Show processing progress while the model is being built (async job) | Must |
| FR-11 | Guided capture: the customer captures **alone** (no helper); reject poor captures with clear, specific retake instructions | Must |
| FR-12 | Rescan to replace the saved model (old one deleted when new one is ready) | Should |
| FR-13 | Remember the last selected outfit between visits | Should |
| FR-14 | Save a screenshot of the current outfit to the device | Could |
| FR-15 | Admin screen to manage the garment catalog | Could (seed script is enough for MVP) |
| FR-16 | Generate a reusable 3D model from the captured images, **subject to technical feasibility** (see [feasibility-macbook-camera.md](feasibility-macbook-camera.md)) | Must (feasibility-gated) |

### Non-functional requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | **Capture:** latest Chrome and Safari on macOS with the built-in camera. **Viewing** (catalog, model, try-on): desktop and mobile browsers. | — |
| NFR-02 | Customer files encrypted at rest; HTTPS in transit whenever not on `localhost` | 100% of files |
| NFR-03 | Owner-only access to models and captures | 0 cross-user leaks in tests |
| NFR-04 | Viewer usable on a mid-range phone | ≥ 30 fps while rotating |
| NFR-05 | Accessibility: readable contrast, keyboard-usable forms, text alternatives for instructions | WCAG 2.2 AA for non-3D UI |

> **Priority key (MoSCoW):** Must = MVP fails without it · Should = expected in MVP if time allows · Could = nice to have · Later = after MVP.

### Sign-off

| Item | Status |
|------|--------|
| Requirements FR-01…FR-15, NFR-01…NFR-05 | ✅ **Approved by project owner, 20 Nov 2026** |
| Out-of-scope list (§1.5) | ✅ **Approved, 20 Nov 2026** |
| Phase 1 design docs (flows, consent v1, capture steps, garment format, targets, wireframes, test cases) | ✅ **Approved with no changes, 20 Nov 2026** |
| **Requirement change: MacBook built-in camera replaces phone capture** (FR-01, FR-08, FR-11, FR-16, NFR-01, NFR-02, out-of-scope) | ✅ **Approved 20 Nov 2026.** See [change-log.md](change-log.md) |

## 1.4 Technical constraints (must be understood before building)

1. **Laptop-camera images do not give an accurate body measurement.** Hair, loose clothing, hidden surfaces, lighting and movement all cause errors.
6. **The MacBook camera is fixed.** It can't move around the person, so the person turns in place. The camera is landscape-only, and the face is small in full-body views, so separate close-ups are needed. Whether this gives a usable 3D model **must be tested** (Phase 3 feasibility gate).
2. **A 360° capture is not a clean, editable body mesh.** A raw photogrammetry mesh includes the clothes the person wore and usually cannot "change clothes."
3. **Editable body + garment fitting are two separate problems.** One is body reconstruction and the other is garment alignment and cloth simulation.
4. **A try-on is a visual preview, not a size or fit guarantee.** It must be labelled that way unless validated.
5. **Face and body data are sensitive.** You need clear consent, encryption, data minimization, and deletion that also covers backups.

## 1.5 Out of scope for the MVP

- Size recommendation / measurement extraction
- Realistic cloth physics simulation (evaluated in Phase 6, not promised)
- Dresses, outerwear, shoes, accessories (the existing `Garment` type allows `dress`/`outerwear`; keep them unused for now)
- Native mobile apps
- **Phone-camera capture, helper-held capture, and phone-to-MacBook transfer** (removed 20 Nov 2026)
- External cameras or 3D scanners (only if the feasibility gate requires it, with owner approval)
- Public cloud deployment before the pilot

## 1.6 Success criteria

See [05-mvp-acceptance.md](05-mvp-acceptance.md). Short version: a customer can scan once, sign out, come back, rotate their saved model, and switch between at least 2 shirts and 2 pants. Their data stays private and can be deleted.
