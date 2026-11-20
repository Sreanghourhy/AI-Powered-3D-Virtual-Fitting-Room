# AI-Powered 3D Virtual Fitting Room

A **single-user personal prototype**. It scans **you** with your MacBook's built-in camera, builds a 3D model of your **real** appearance (no avatar, no reshaping), and lets you try on shirts and pants and rotate the model 360°. Everything stays on your MacBook. There is no login.

- **Frontend:** SvelteKit 3 + TypeScript + Tailwind CSS 4, Three.js / Threlte viewer
- **Backend:** Python 3.12 + FastAPI (localhost only), SQLAlchemy + Alembic (SQLite), encrypted file storage, background job worker

> **Status:** Phase 2R done (single-user app). Camera capture (Phase 3) and 3D reconstruction (Phase 4) are **not built yet**, so "Start Scan" currently shows the setup checklist only.

Project plan, design docs and task backlog: [`docs/`](docs/README.md).

## Getting started

Requirements: Node.js 22.12+ (24 LTS recommended) and Python 3.12+.

```sh
npm install          # frontend dependencies
npm run setup        # MediaPipe files (self-hosted) + backend venv, dependencies, encryption key, database, seed data
```

Run (separate terminals):

```sh
npm run dev:api        # FastAPI on http://127.0.0.1:8000 (API docs: /docs)
npm run dev:worker     # background job worker
npm run dev -- --open  # the app on http://localhost:5173
```

The app opens directly on the **fitting room**. The browser calls `/api/*`: Vite proxies it to FastAPI in dev, and during server-side rendering the `handleFetch` hook forwards it (see `src/hooks.server.ts`).

> **Encryption key:** `setup:api` creates `backend/.env` with `FR_ENCRYPTION_KEY`, which encrypts your scan images and models. Back it up securely, because losing it makes stored scans unreadable. Never commit `backend/.env`.

> **Dev styles:** `src/routes/layout.css` tells Tailwind to scan all of `src/` (`@source '../'`), which fixed classes missing on new or client-only pages in dev. If styles ever look stale, restart `npm run dev`.

> **Camera lab (dev only):** http://localhost:5173/dev/camera-lab runs the P3-01 camera capability probe. See [docs/experiments/p3-01-camera-capabilities.md](docs/experiments/p3-01-camera-capabilities.md). It returns 404 in production builds.

## Manual test checklist

1. **`/` (Fitting room)** opens directly: "No scan yet", **Start Scan**, Shirt and Pants pickers, "Backend: ok". No login or profile screen.
2. Pick a shirt, then pants: each picker changes only its own item, and the URL keeps the outfit (`?top=…&bottom=…`).
3. **Start Scan** → the privacy notice appears. **Cancel** returns to the fitting room. **Continue** (with or without "Don't show this again") shows the setup checklist.
4. **Discard scan & model** → confirm → green "deleted" message.
5. **Catalog** shows 2 shirts / 2 pants; "Try on" opens the fitting room with that item selected.
6. Old links redirect: `/try-on` → `/`, `/my-model` → `/`, `/capture` → `/scan`; `/login` is gone (404).
7. `/viewer-demo` (dev only) rotates the public sample model. It is never shown as "you".

## Commands

| Command | What it does |
|---------|--------------|
| `npm run dev` | SvelteKit dev server |
| `npm run dev:api` | FastAPI with auto-reload, bound to 127.0.0.1:8000 |
| `npm run dev:worker` | Job worker (`python -m app.worker`) |
| `npm run setup:api` | Backend setup (safe to re-run; keeps an existing key) |
| `npm run db:migrate` | Apply database migrations |
| `npm run db:seed` | Seed the catalog (2 shirts + 2 pants) |
| `npm run check` | Svelte + TypeScript validation |
| `npm test` | Frontend unit tests (Vitest) |
| `npm run lint:api` | Backend lint + format check (ruff) |
| `npm run test:api` | Backend tests (pytest) |
| `npm run test:all` | All of the above checks and tests |
| `npm run build` / `npm run preview` | Production build / preview |

## Project structure

```text
src/                         # SvelteKit frontend
  env.ts                     # Environment variables (SvelteKit 3 defineEnvVars), e.g. API_URL
  hooks.server.ts            # SSR /api proxy to the local backend
  lib/
    api/client.ts            # Typed FastAPI client (sends X-Fitting-Room header)
    components/
      ui/                    # Header, Modal, privacy notice, disclaimers, backend status
      fitting-room/          # 3D viewer + fitting-room stage (no avatar state)
      garments/              # Catalog card, shirt/pants pickers, outfit helpers
    types/                   # api.ts (API responses), garment.ts (catalog)
    utils/                   # local-flag (safe localStorage)
  routes/
    +page.svelte             # Fitting room (main interface)
    scan/                    # Scan (camera capture arrives in Phase 3)
    catalog/                 # Browse shirts and pants
    viewer-demo/             # Dev-only viewer test with the public sample model
    try-on/ my-model/ capture/   # Redirects from old URLs
backend/                     # FastAPI
  app/api/                   # Routers: health, garments, jobs, data (discard)
  app/core/                  # Settings, localhost protection, key generator
  app/db/                    # Models, session, migrations helper, seed
  app/services/              # Encrypted storage, discard, jobs, audit log
  app/worker/                # Background job runner + handlers
  alembic/                   # Database migrations
  tests/
static/models/               # PUBLIC sample models only (never your scan)
static/garments/             # PUBLIC catalog assets
data/                        # PRIVATE, git-ignored: database + encrypted blobs
docs/                        # Plan, design docs, task backlog
```

## Security and privacy rules

- **Local only.** The backend listens on `127.0.0.1`, accepts only `localhost`/`127.0.0.1` Host headers, and requires `X-Fitting-Room: 1` on every change. No CORS, so other websites can't call it.
- Scan images and models are stored **encrypted** (AES-256-GCM) under `data/`, never in `static/` or any public URL.
- **Discard scan & model** (`DELETE /data`) deletes all scan rows and encrypted files.
- If a real model can't be built, the app shows why. **It never substitutes a generic avatar** (guarded by a test).
- Garments: **shirts (`top`) and pants (`bottom`) only**, enforced by the database.

See [docs/03-privacy-security.md](docs/03-privacy-security.md).
