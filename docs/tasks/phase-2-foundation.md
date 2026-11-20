# Phase 2 — Application Foundation (Weeks 2–3)

**Goal:** A working app skeleton: frontend, backend, database, storage, auth, catalog.
**Deliverable:** Working app with sign-in, catalog, and a placeholder 3D viewer.

**Status (20 Nov 2026):** all 18 tasks done, ✅ **approved by owner 20 Nov 2026**. Tests: backend 71 passed (pytest + ruff clean), frontend 22 passed (Vitest), `svelte-check` 0 errors, production build OK.

> **CR-02 note:** auth, sessions, consent and per-user tasks (P2-03 user parts, P2-04, P2-05, P2-12, P2-13, P2-14) are **superseded** by the single-user refactor in [phase-2r-single-user.md](phase-2r-single-user.md). Their code stays until P2R removes it.

**Implementation notes**
- Auth = server-side sessions (token hash stored) + Argon2id → decision D6.
- Job runner = DB-backed worker, one job at a time → decision D4.
- Route protection uses SvelteKit route groups `(app)` / `(auth)` so it also applies to client-side navigation.
- The project uses **SvelteKit 3**: env vars via `src/env.ts` (`$app/env/private`), hook types from `@sveltejs/kit/hooks`, `goto(..., { reset: false })`.
- Consent withdrawal will also delete captures/models once those tables exist (P3-02).

---

## Backend

### P2-01 · Backend project structure   `S` ✅
**Depends on:** P0-03
- [x] Create `app/api`, `app/core`, `app/db`, `app/services`, `app/worker`, `tests/`
- [x] Settings via `pydantic-settings` reading `.env` (DB URL, data dir, secret key, encryption key)
- [x] Add `ruff` for lint/format

**Done when:** app starts with settings loaded and `ruff check` passes.

### P2-02 · Database setup (SQLite + SQLAlchemy + Alembic)   `S` ✅
**Depends on:** P2-01
- [x] SQLAlchemy 2.x engine/session; SQLite file under `data/`
- [x] Initialize Alembic; first empty migration
- [x] Use UUID primary keys

**Done when:** `alembic upgrade head` creates the DB.

### P2-03 · Tables: users, consents, audit_log   `S` ✅
**Depends on:** P2-02
- [x] Models + migration per [02-architecture.md §2.4](../02-architecture.md)

**Done when:** migration applies cleanly and a test inserts/reads a user.

### P2-04 · 🔒 Auth: sign up / login / logout / me   `M` ✅
**Depends on:** P2-03
- [x] Password hashing with Argon2id (`argon2-cffi`)
- [x] Server-side sessions with an `HttpOnly`, `Secure`, `SameSite=Lax` cookie
- [x] Endpoints: `POST /auth/signup`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`
- [x] `get_current_user` dependency
- [x] Tests: success, wrong password, duplicate email, unauthenticated `/auth/me`

**Done when:** all auth tests pass.

### P2-05 · 🔒 Consent endpoints   `S` ✅
**Depends on:** P2-04, P1-03
- [x] `POST /consents` (stores version), `GET /consents/me`, `DELETE /consents/{id}`
- [x] `require_consent` dependency for capture endpoints later

**Done when:** a user without consent gets 403 from a protected test route.

### P2-06 · Garments table + seed data   `S` ✅
**Depends on:** P2-02, P1-05
- [x] `garments` model + migration
- [x] Seed script with 2 shirts + 2 pants (placeholder SVG thumbnails; GLBs in Phase 6)

**Done when:** seed runs and inserts 4 garments.

### P2-07 · Catalog API   `XS` ✅
**Depends on:** P2-06
- [x] `GET /garments?category=top|bottom`, `GET /garments/{id}`
- [x] Tests

**Done when:** API returns seeded garments filtered by category.

### P2-08 · 🔒 Encrypted file storage service   `M` ✅
**Depends on:** P2-01
- [x] `StorageService.put(bytes) -> storage_key`, `get(key) -> bytes`, `delete(key)`
- [x] AES-GCM encryption with `cryptography`; key from settings
- [x] Random opaque keys; files under `data/blobs/`
- [x] Tests: round-trip, file on disk is not plaintext, delete removes file

**Done when:** all storage tests pass.

### P2-09 · Jobs table + simple worker   `M` ✅
**Depends on:** P2-02
- [x] `jobs` table (type, ref_id, status, progress, error, timestamps)
- [x] `python -m app.worker` loop: pick queued job, run handler, update progress/status
- [x] A dummy `sleep` job type for testing
- [x] `GET /jobs/{id}` (owner only)

**Done when:** a dummy job goes queued → processing → done and progress is visible via API.

## Frontend

### P2-10 · Typed API client   `S` ✅
**Depends on:** P0-05
- [x] `src/lib/api/client.ts` with `fetch` wrapper (credentials included, error handling)
- [x] Types for User, Garment, Job

**Done when:** health + garments calls work from a test page.

### P2-11 · App layout and navigation   `S` ✅
**Depends on:** P1-09
- [x] Responsive header/nav: Catalog, Try-On, My Model, Account
- [x] Mobile menu

**Done when:** navigation works on phone width and desktop.

### P2-12 · Sign up / login pages   `S` ✅
**Depends on:** P2-04, P2-10
- [x] `/signup`, `/login` forms with validation and error messages
- [x] Logout button

**Done when:** a user can sign up, log out and log in from the browser.

### P2-13 · Route protection   `XS` ✅
**Depends on:** P2-12
- [x] `+layout.server.ts` / hooks: redirect to `/login` for protected routes

**Done when:** visiting `/my-model` logged out redirects to login.

### P2-14 · 🔒 Consent page   `S` ✅
**Depends on:** P2-05, P2-12
- [x] `/consent` shows consent v1 text; accept/decline
- [x] Capture route requires consent

**Done when:** a new user is sent to `/consent` before `/capture`.

### P2-15 · Catalog page   `S` ✅
**Depends on:** P2-07, P2-11
- [x] `/catalog` with Shirts / Pants tabs, cards with thumbnails
- [x] Use existing `components/garments/` folder

**Done when:** the 4 seeded garments display, filtered by tab.

### P2-16 · Placeholder Try-On page   `S` ✅
**Depends on:** P0-04, P2-15
- [x] `/try-on` with `ModelViewer` showing the public sample model
- [x] Shirt and pants selectors (UI only, no garment loading yet)
- [x] "Visual preview — not a size guarantee" label

**Done when:** page renders with viewer + selectors on phone and desktop.

### P2-17 · My Model page skeleton   `XS` ✅
**Depends on:** P2-11
- [x] `/my-model` with "No model yet → Start capture" state

**Done when:** empty state renders for a new user.

### P2-18 · Dev scripts & README update   `XS` ✅
**Depends on:** all above
- [x] `npm run setup:api`, `dev:api`, `dev:worker`, `db:migrate`, `db:seed`, `test:all`
- [x] Update root `README.md` with backend setup

**Done when:** a fresh clone can be run by following the README.
