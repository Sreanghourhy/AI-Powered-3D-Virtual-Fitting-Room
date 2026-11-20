# Phase 2R — Simplify to a Single-User Local Prototype (CR-02)

> **Status:** ✅ plan approved 20 Nov 2026 (full removal of auth/consent code and tables approved). In progress.
> Refactors Phase 2. Working code is **kept** where it doesn't conflict: catalog, encrypted storage, job worker, viewer, pickers, typed client, SSR `/api` proxy.

**Goal:** The app opens straight into one fitting-room interface. No login, accounts, profiles or consent records. The backend is locked to localhost, and everything can be discarded.
**Deliverable:** `/` fitting room + `/scan` placeholder; auth/consent code removed; localhost protection; `DELETE /data`; all tests green.

---

### P2R-01 · Backend: remove accounts, sessions and consent   `M` ✅
**Depends on:** owner approval
- [x] Remove routers `auth.py`, `consents.py`; remove `CurrentUser` / `ConsentedUser` deps, `security.py` (passwords/sessions), `services/consent.py`
- [x] Models: drop `User`, `UserSession`, `Consent`; remove `jobs.user_id`; `audit_log` without `user_id`
- [x] Alembic migration that drops these tables/columns (SQLite batch mode); `downgrade` documented as not restoring data
- [x] `GET /jobs/{id}` without owner check; settings: remove session/cookie/consent fields
- [x] Remove `argon2-cffi` and `email-validator` dependencies

**Done when:** the backend starts, migrations apply to the existing dev DB, and no auth code remains (`grep` check).

### P2R-02 · 🔒 Backend: localhost protection   `S`
**Depends on:** P2R-01
- [ ] `dev:api` binds explicitly to `127.0.0.1`
- [ ] Trusted-host check: only `localhost` / `127.0.0.1` (any port) → else 400
- [ ] Middleware: `POST`/`PUT`/`PATCH`/`DELETE` require `X-Fitting-Room: 1` → else 403
- [ ] No CORS middleware (cross-origin preflights get no allow headers)
- [ ] Frontend client always sends the header; SSR proxy forwards it

**Done when:** tests TC-57, TC-58 and TC-59 pass.

### P2R-03 · 🔒 Backend: Discard all data   `S`
**Depends on:** P2R-01
- [ ] `DELETE /data`: delete jobs, audit entries for scans, (scans, images, models, outfit once they exist) **and their blobs**; then remove any orphan blobs under `data/blobs/`
- [ ] Idempotent (204 even when empty)

**Done when:** a test proves 0 rows and 0 blob files remain (TC-44, Q10).

### P2R-04 · Frontend: remove sign-in and consent UI   `S`
**Depends on:** P2R-01
- [ ] Delete `(auth)/` routes, `AuthForm.svelte`, `(app)/consent/`, `ConsentText.svelte`, `(app)/+layout.server.ts` guard
- [ ] `hooks.server.ts`: remove user lookup (`handle`), keep `handleFetch` `/api` proxy; remove `App.Locals.user`
- [ ] Header: app name + Catalog link only (no account menu)
- [ ] Client/types: remove auth and consent calls/types; remove `loginUrl` (keep `safeRedirect` only if still used)

**Done when:** `svelte-check` is clean and no route or component refers to login, sign-up, user or consent.

### P2R-05 · Frontend: one fitting-room interface at `/`   `M`
**Depends on:** P2R-04
- [ ] `/` = viewer area + shirt/pants pickers (reuse `GarmentPicker`, outfit helpers) + **Start Scan** + **Discard** (states: no scan / generating / ready / failed per [wireframes/fitting-room.md](../wireframes/fitting-room.md))
- [ ] **No sample/avatar body in the main viewer.** The empty state says "No scan yet". `static/models/sample.glb` is used only on `/viewer-demo`.
- [ ] `/scan` placeholder with setup checklist (real capture in Phase 3)
- [ ] Old URLs redirect: `/my-model`, `/try-on` → `/`; `/capture` → `/scan`
- [ ] Keep `/catalog` (browse) with "Try on" linking to `/?top=…` / `/?bottom=…`

**Done when:** the app opens directly to the fitting room on desktop; the old routes redirect.

### P2R-06 · Privacy notice and discard confirmation   `S`
**Depends on:** P2R-05
- [ ] Dialog from [privacy-notice.md](../privacy-notice.md) on first **Start Scan** ("Don't show again" in localStorage, wrapped in try/catch)
- [ ] Discard confirmation dialog → `DELETE /data` → back to the "No scan yet" state
- [ ] Disclaimer labels kept (visual preview, approximation)

**Done when:** TC-03 and TC-49 pass manually; discard works from the UI.

### P2R-07 · Tests, README and docs   `S`
**Depends on:** P2R-01 … P2R-06
- [ ] Remove `test_auth.py`, `test_consents.py`, `test_models_users.py` (or adapt); update `test_jobs.py`, `helpers.py`, client and redirect tests
- [ ] New tests: TC-01, TC-02, TC-44, TC-57, TC-58, TC-59
- [ ] README: remove sign-up from the manual test steps; add Discard; note localhost-only
- [ ] `npm run test:all` green

**Done when:** all tests pass and the docs match the code.
