# AI-Powered 3D Virtual Fitting Room

Scan once, save until the customer deletes it, try on shirts and pants anytime, on a 3D model of the customer's **real** appearance (no avatar editing).

- **Frontend:** SvelteKit 3 + TypeScript + Tailwind CSS 4, Three.js / Threlte viewer
- **Backend:** Python 3.12 + FastAPI, SQLAlchemy + Alembic (SQLite for the prototype), encrypted file storage, background job worker

Project plan, design docs and task backlog: [`docs/`](docs/README.md).

## Getting started

Requirements: Node.js 22.12+ (24 LTS recommended) and Python 3.12+.

```sh
npm install          # frontend dependencies
npm run setup:api    # backend venv, dependencies, backend/.env with a new encryption key, database, seed data
```

Run (separate terminals):

```sh
npm run dev:api      # FastAPI on http://localhost:8000 (API docs: /docs)
npm run dev:worker   # background job worker (needed for processing jobs)
npm run dev -- --open  # SvelteKit on http://localhost:5173
```

The browser calls `/api/*`. Vite proxies it to FastAPI in dev, and during server-side rendering the `handleFetch` hook forwards it (see `src/hooks.server.ts`).

> **Encryption key:** `setup:api` creates `backend/.env` with `FR_ENCRYPTION_KEY`. It encrypts every customer file. Back it up securely, because losing it makes stored scans unreadable. Never commit `backend/.env`.

> **Dev styles look stale** after adding a new file? Restart `npm run dev` (dev-server CSS cache; production builds are unaffected).

## Commands

| Command | What it does |
|---------|--------------|
| `npm run dev` | SvelteKit dev server |
| `npm run dev:api` | FastAPI with auto-reload (port 8000) |
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
  hooks.server.ts            # Resolves signed-in user; SSR /api proxy
  lib/
    api/client.ts            # Typed FastAPI client
    components/
      ui/                    # Header, auth form, shared UI
      consent/               # Consent text v1 + shared disclaimer labels
      fitting-room/          # 3D viewer (Three.js / Threlte)
      garments/              # Catalog card, shirt/pants pickers, outfit helpers
    types/                   # api.ts (API responses), garment.ts (catalog)
    utils/                   # safeRedirect, loginUrl
  routes/
    (auth)/login, signup     # Signed-out only
    (app)/my-model, try-on, consent, capture   # Sign-in required
    catalog/                 # Public catalog
    viewer-demo/             # Public 3D viewer demo
backend/                     # FastAPI
  app/api/                   # Routers: health, auth, consents, garments, jobs
  app/core/                  # Settings, password hashing, session tokens, key generator
  app/db/                    # Models, session, migrations helper, seed
  app/services/              # Encrypted storage, consent rules, jobs, audit log
  app/worker/                # Background job runner + handlers
  alembic/                   # Database migrations
  tests/
static/models/               # PUBLIC sample models only
static/garments/             # PUBLIC catalog assets
data/                        # PRIVATE, git-ignored: database + encrypted blobs
docs/                        # Plan, design docs, task backlog
```

## Security and privacy rules

- Customer scans and models are stored **encrypted** (AES-256-GCM) under `data/`. They are **never** placed in `static/` or any public URL.
- Every user-data endpoint checks ownership and returns 404 for other users' resources.
- Sessions use `HttpOnly`, `Secure`, `SameSite=Lax` cookies. Only a hash of the session token is stored.
- Capture requires the current consent version. See [docs/03-privacy-security.md](docs/03-privacy-security.md).
- Garments: **shirts (`top`) and pants (`bottom`) only**, enforced by the database.
