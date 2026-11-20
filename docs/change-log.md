# Change Log — Requirements

## CR-02 · Simplified single-user prototype, no authentication (20 Nov 2026)

**Requested by:** project owner · **Status:** 📝 **docs updated, waiting for owner approval** · **Code:** not changed yet

### New requirements (owner, summarised)
- **Single-user personal prototype** on the owner's MacBook. The app opens **directly** to the fitting-room interface.
- **Workflow:** Start Scan → allow camera → turn and capture angles → review/retake → **Generate 3D Model** → view in 3D → pick shirts/pants independently → rotate 360°.
- **Remove:** login, registration, authentication, user accounts, customer profiles, profile selection, PINs, recovery codes, phone capture, multiple users, cloud profile storage, any shared-profile screen.
- The model must be available during the session. **Optional local persistence** is acceptable; no profile UI.
- MediaPipe for guidance, pose and quality checks. Multiple angles. **Real person only**: no generic avatar, no reshaping, and **never a silent avatar fallback if reconstruction fails**.
- Private camera processing and storage, plus a clear **discard** option for captured images and generated data.
- Feasibility must be **tested** and documented: full body in frame, enough angles, usable reconstruction, **geometry that supports changing shirts and pants**, limitations, failed experiments, alternatives.
- **Priority:** MacBook camera → multi-angle capture → real-person 3D reconstruction → shirt/pants try-on → 360° viewer.
- The Pinterest idea from the previous message is **not** part of this change. The catalog stays with prepared 3D shirts and pants.

### Conflicts found in the current implementation

| Component | Where | Conflict | Proposed action (task) |
|-----------|-------|----------|------------------------|
| Sign up / log in / log out / me API | `backend/app/api/auth.py` | Authentication not wanted | **Remove** router (P2R-01) |
| Sessions, password hashing | `UserSession` model, `app/core/security.py` | Not needed without accounts | **Remove** (P2R-01) |
| Users table, user ownership | `User` model, `CurrentUser` in `deps.py`, `jobs.user_id` | No accounts / multiple users | **Remove**; jobs not tied to a user (P2R-01) |
| Consent API + guard | `app/api/consents.py`, `require_consent`, `consents` table | Was per-account consent | **Replace** with an in-app privacy notice; no stored record (P2R-01, P2R-06) |
| Audit log `user_id` | `AuditLog` | No users | **Keep** the log, drop the user column (P2R-01) |
| — (new) | Backend | Without accounts, other websites open in the browser could try to call `localhost:8000` | **Add** localhost protection (P2R-02) |
| — (new) | Backend | Need "discard everything" | **Add** `DELETE /data` (P2R-03) |
| Login / sign-up pages, AuthForm | `src/routes/(auth)/`, `AuthForm.svelte` | No login | **Remove** (P2R-04) |
| Account menu, Sign in / Get started | `AppHeader.svelte` | No accounts | **Simplify** header (P2R-04) |
| User lookup + SSR route guard | `hooks.server.ts` (`handle`), `(app)/+layout.server.ts`, `locals.user`, `loginUrl` | No auth | **Remove**; keep the `/api` SSR proxy (P2R-04) |
| Consent page, consent text v2 | `(app)/consent/`, `ConsentText.svelte` | Consent flow replaced | **Remove**; add a privacy notice (P2R-04, P2R-06) |
| Separate My Model / Try-On / Capture pages | `(app)/my-model`, `(app)/try-on`, `(app)/capture` | App should open straight to one fitting-room interface | **Merge** into `/` (fitting room) + `/scan` (capture); old URLs redirect (P2R-05) |
| Sample model in Try-On | `(app)/try-on` uses the public CesiumMan model | Could look like a generic avatar stand-in | Main viewer shows **"No scan yet"** instead; sample model only on dev page `/viewer-demo` (P2R-05) |
| Home landing page | `src/routes/+page.svelte` | Should open to the fitting room | **Replace** with the fitting-room interface (P2R-05) |
| Auth / consent tests | `test_auth.py`, `test_consents.py`, parts of `test_jobs.py`, `test_models_users.py`, `redirect.test.ts`, client tests | Test removed features | **Remove or adapt**; add tests for localhost protection + discard (P2R-07) |

**Kept unchanged:** catalog API and seed (2 shirts + 2 pants), encrypted storage, job worker, 3D viewer, garment picker and outfit helpers, typed client (minus auth calls), `/catalog`, `/viewer-demo`, settings, migrations tooling, Vitest/pytest setup.

### Documents changed in CR-02
| Document | Change |
|----------|--------|
| [01-project-overview.md](01-project-overview.md) | **Rewritten** (v3): single-user goal, 10-step workflow, FR/NFR, removed features, sign-off |
| [02-architecture.md](02-architecture.md) | **Rewritten** (v3): local single-user architecture, pipeline, data model without users, API, decisions D9–D11 |
| [03-privacy-security.md](03-privacy-security.md) | **Rewritten**: local data handling, camera, localhost protection, discard |
| [04-risks-and-costs.md](04-risks-and-costs.md) | R5 reworded, R12 (localhost exposure), R13 (reconstruction failure) added |
| [05-mvp-acceptance.md](05-mvp-acceptance.md) | **Rewritten**: A1–A6 for the single-user workflow; targets updated |
| [user-flows.md](user-flows.md) | **Rewritten** (v3): scan → generate → try on; discard; retake / failed reconstruction |
| [capture-guide.md](capture-guide.md), [capture-steps.md](capture-steps.md) | Start Scan entry, privacy notice, Generate 3D Model; no accounts or consent |
| [privacy-notice.md](privacy-notice.md) | **New**: short in-app notice (replaces the consent screen) |
| [consent-v2.md](consent-v2.md), [consent-v1.md](consent-v1.md) | Marked **retired** |
| [feasibility-macbook-camera.md](feasibility-macbook-camera.md) | F11 (garment-ready geometry), no-avatar-fallback rule, failed-experiments log |
| [wireframes/](wireframes/README.md) | **New** [fitting-room.md](wireframes/fitting-room.md) (main screen); capture updated; consent / my-model / catalog-try-on marked superseded |
| [test-cases.md](test-cases.md) | **Rewritten** (v3); removed auth/multi-user cases listed |
| [tasks/phase-2r-single-user.md](tasks/phase-2r-single-user.md) | **New**: 7 refactor tasks P2R-01 to P2R-07 |
| [tasks/phase-3-capture.md](tasks/phase-3-capture.md), [phase-4](tasks/phase-4-reconstruction.md), [phase-5](tasks/phase-5-profiles-viewer.md), [phase-6](tasks/phase-6-try-on.md), [phase-7](tasks/phase-7-hardening.md), [phase-8](tasks/phase-8-pilot.md) | Updated for single user / no auth; Phase 5, 7 and 8 rewritten |
| [tasks/README.md](tasks/README.md), [README.md](README.md), [phase-2-foundation.md](tasks/phase-2-foundation.md) | Counts, sequence, superseded notes |

### Proposed development sequence
1. **Phase 2R** (P2R-01 to P2R-07): remove auth/profiles, add localhost protection + discard, one fitting-room interface. About 2–3 days.
2. **Phase 3 Part B** (P3-01 to P3-05): **real-camera feasibility tests** → 🛑 owner go/no-go.
3. **Phase 3 Part C**: capture build (Start Scan → guided angles → review/retake).
4. **Phase 4**: real-person reconstruction ("Generate 3D Model"), including the garment-ready geometry check.
5. **Phase 6** shirt/pants try-on, **Phase 5** viewer polish + local persistence, then **Phase 7** privacy/reliability and **Phase 8** personal evaluation.

Option: P3-01 (camera probe) doesn't depend on Phase 2R, so it can run in parallel if the owner wants camera results sooner.

### Decisions needed from the owner
1. Approve the CR-02 docs and the sequence above.
2. Approve **removing** (not just hiding) the auth/consent code and dropping the `users`, `sessions` and `consents` tables (P2R-01).
3. Approve **local persistence**: keep the latest scan and model on this MacBook (encrypted, under `data/`) until **Discard**, so a restart doesn't lose a slow-to-generate model.
4. Approve replacing the consent screen with a short **privacy notice** (no stored record).

---

## CR-01 · MacBook built-in camera replaces phone capture (20 Nov 2026)

> Partly superseded by CR-02: consent-v2, per-user ownership and accounts are retired. The MacBook-camera parts remain valid.

**Requested by:** project owner · **Status:** ✅ **approved by owner 20 Nov 2026** (docs, Phase 3 plan, consent-v2, D8, dev camera lab) · **Code:** applied in P3-00

### New requirements (owner)
1. Capture with the **MacBook's built-in camera**.
2. Access it from the web app with the browser **MediaDevices API (`getUserMedia`)**.
3. **Remove** phone camera workflows, helper-held capture, and phone-to-MacBook transfer from the MVP.
4. Guided capture for **front, side and back** views with the MacBook camera.
5. Preserve the customer's original face, body proportions and appearance as accurately as technically possible.
6. Generate a reusable 3D model, **subject to technical feasibility**.
7. Rotate the saved model 360°.
8. Shirts and pants only, independently.
9. Save the 3D profile until the customer requests deletion.

Also: no body reshaping or generic replacement avatars; don't assume the camera works without testing; do a feasibility assessment; no phone HTTPS setup; keep Phase 2 unless a change is necessary.

### Documents changed

| Document | Change |
|----------|--------|
| [feasibility-macbook-camera.md](feasibility-macbook-camera.md) | **New.** Hardware, geometry and resolution estimate, approach comparison, likely / uncertain / not possible, macOS/browser specifics, go/no-go checks F1–F10 |
| [01-project-overview.md](01-project-overview.md) | Vision, Capture screen, FR-01 (MacBook camera + `getUserMedia`), FR-08 (no reshaping / no generic avatar), FR-11 (customer alone), **new FR-16** (3D model subject to feasibility), NFR-01 / NFR-02, new constraint 6 (fixed camera), out-of-scope (phone, helper, transfer), sign-off row |
| [02-architecture.md](02-architecture.md) | Stack (camera API, in-browser MediaPipe), pipeline diagram, `capture_sessions` / `capture_files` (13 named views), retake endpoint, D2 updated, **new D7** (capture method), **new D8** (in-browser computer vision, needs approval) |
| [03-privacy-security.md](03-privacy-security.md) | New camera section (camera only on the capture page, stopped on leave, video effects off, no third-party requests); localhost vs HTTPS; images stay in memory until upload |
| [04-risks-and-costs.md](04-risks-and-costs.md) | R1 reworded; R8 (phone HTTPS) replaced; **new R9–R11**; costs: no phone; optional lights; external webcam only with owner approval |
| [05-mvp-acceptance.md](05-mvp-acceptance.md) | A1 on MacBook; Q2 ≤ 4 min (alone); link to F1–F10 |
| [user-flows.md](user-flows.md) | Flow 1 and Flow 4 rewritten for MacBook capture |
| [capture-guide.md](capture-guide.md) | **Rewritten** (v1.0): room setup, Mac video-effects settings, floor marker, 8 views + 5 face close-ups |
| [capture-steps.md](capture-steps.md) | **Rewritten**: MVP decisions, steps 0–8, auto-capture, new problem codes |
| [wireframes/capture.md](wireframes/capture.md) | **Rewritten** for a landscape laptop screen readable from ~3 m |
| [wireframes/README.md](wireframes/README.md), [wireframes/my-model.md](wireframes/my-model.md) | Capture on MacBook only; phone layouts are for viewing only |
| [consent-v2.md](consent-v2.md) | **New draft** (MacBook camera wording, no helper, "no generic avatar"); [consent-v1](consent-v1.md) marked superseded |
| [test-cases.md](test-cases.md) | TC-07 to TC-09 for MacBook Chrome / Safari; TC-15 to TC-17, TC-19 updated; **new TC-51 to TC-54** |
| [tasks/phase-3-capture.md](tasks/phase-3-capture.md) | **Re-planned**: P3-00 copy/consent update, **P3-01 to P3-05 feasibility spike + owner gate**, P3-06 to P3-20 build. 15 → 21 tasks. LAN HTTPS removed |
| [tasks/phase-4-reconstruction.md](tasks/phase-4-reconstruction.md) | Approach B primary; A comparison only; dataset from MacBook workflow |
| [tasks/phase-0-start-today.md](tasks/phase-0-start-today.md) | Phone sample capture and first experiment moved to P3-05 |
| [tasks/README.md](tasks/README.md), [README.md](README.md) | Task count, roadmap row, new document links |

### Not changed
- **Phase 2 code** stays as it is.
- Viewing pages (catalog, My Model, Try-On) still work on phones. Only **capture** is MacBook-only.
- Garment format, backup policy, short disclaimer labels.

### Code changes needed after approval (task P3-00)
| File | Current text | Change |
|------|--------------|--------|
| `src/lib/components/consent/ConsentText.svelte` | v1: "phone camera…", "A helper can hold the phone…" | v2 wording |
| `backend/app/core/config.py` | `consent_version = "consent-v1"` | `"consent-v2"` |
| `src/routes/+page.svelte` | "A helper takes about 40 photos of you with a phone." | "Stand in front of your MacBook camera and turn slowly. About 4 minutes." |
| `src/routes/(app)/my-model/+page.svelte` | "about 6 minutes with a helper holding the phone" | "about 4 minutes in front of your MacBook camera" |
| `src/routes/(app)/capture/+page.svelte` | Checklist item "A helper to hold the phone" | MacBook checklist (video effects off, floor X) |
| Backend / frontend tests | Use `consent-v1` | Use the setting / `consent-v2` |

### Decisions needed from the owner
1. Approve the updated documents and the **re-planned Phase 3**.
2. Approve **consent-v2** wording.
3. Approve **D8**: adding `@mediapipe/tasks-vision` (self-hosted models) for live guidance and auto-capture.
4. Approve a **dev-only `/dev/camera-lab` page** for the feasibility tests. It is never available in production builds.
