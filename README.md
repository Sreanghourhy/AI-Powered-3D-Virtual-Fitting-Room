# AI-Powered 3D Virtual Fitting Room

A SvelteKit + TypeScript + Tailwind CSS starter. Includes a responsive placeholder page and a feature-oriented folder structure. AI inference, avatar generation, uploads, persistence, and 3D rendering are not implemented yet.

## Getting started

Use Node.js 22.12+ (Node.js 24 LTS recommended) and Python 3.12+.

**1. Backend (FastAPI), one-time setup:**

```sh
cd backend
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
cd ..
```

**2. Run (two terminals):**

```sh
npm run dev:api        # FastAPI on http://localhost:8000
npm install            # first time only
npm run dev -- --open  # SvelteKit on http://localhost:5173
```

The frontend proxies `/api/*` to the backend, and the home page shows **Backend: ok** when both are running. The 3D viewer demo is at `/viewer-demo`.

Project plan and task backlog: see [`docs/`](docs/README.md).

## Project structure

```text
src/
  lib/
    assets/                    # Imported images and icons
    components/
      ui/                      # Shared UI components
      fitting-room/            # Avatar viewer and try-on controls
      garments/                # Garment cards, filters, and selectors
    types/
      garment.ts               # Shared garment data model
    utils/                     # Shared utility functions
    server/
      ai/                      # Private AI provider integrations
      garments/                # Server-side garment data access
  routes/
    +layout.svelte             # Root layout and global CSS import
    +page.svelte               # Starter home page
    layout.css                 # Tailwind entry point and global styles
  app.html                     # HTML document template
  app.d.ts                     # Application-level TypeScript declarations
static/
  models/                      # Public GLB/GLTF assets
  images/                      # Public image assets
```

Empty directories contain `.gitkeep` files so Git preserves the structure. Import shared code using `#lib/`, for example `#lib/types/garment`.

## Commands

- `npm run dev` — development server
- `npm run check` — Svelte and TypeScript validation
- `npm run check:watch` — continuous validation
- `npm run build` — production build
- `npm run preview` — preview the production build locally
- `npm run dev:api` — FastAPI backend with auto-reload (port 8000)
- `npm run test:api` — backend tests (pytest)

## Development guidance

Create pages under `src/routes` using `+page.svelte`. Add server endpoints with `+server.ts` when needed. Keep private AI credentials and integrations in `src/lib/server`; copy `.env.example` to `.env` when configuring a provider. Never put user uploads or private data in `static/`, whose contents are publicly served.

Tailwind CSS uses its Vite plugin and `@import 'tailwindcss'` in `src/routes/layout.css`. A separate Tailwind configuration file is not required for this starter.

The 3D viewer uses Three.js + Threlte (`src/lib/components/fitting-room/ModelViewer.svelte`). Only public, licensed sample models go in `static/models/` (see its README). The included adapter-auto supports automatic deployment detection; select a target-specific adapter when choosing hosting.
# AI-Powered-3D-Virtual-Fitting-Room
