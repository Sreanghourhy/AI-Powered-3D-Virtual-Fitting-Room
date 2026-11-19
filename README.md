# AI-Powered 3D Virtual Fitting Room

A SvelteKit + TypeScript + Tailwind CSS starter. Includes a responsive placeholder page and a feature-oriented folder structure. AI inference, avatar generation, uploads, persistence, and 3D rendering are not implemented yet.

## Getting started

Use Node.js 22.12+ (Node.js 24 LTS recommended).

```sh
npm install
npm run dev -- --open
```

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

## Development guidance

Create pages under `src/routes` using `+page.svelte`. Add server endpoints with `+server.ts` when needed. Keep private AI credentials and integrations in `src/lib/server`; copy `.env.example` to `.env` when configuring a provider. Never put user uploads or private data in `static/`, whose contents are publicly served.

Tailwind CSS uses its Vite plugin and `@import 'tailwindcss'` in `src/routes/layout.css`. A separate Tailwind configuration file is not required for this starter.

For the 3D viewer, add a rendering library when you begin that feature and initialize browser-only APIs on the client. The included adapter-auto supports automatic deployment detection; select a target-specific adapter when choosing hosting.
# AI-Powered-3D-Virtual-Fitting-Room
