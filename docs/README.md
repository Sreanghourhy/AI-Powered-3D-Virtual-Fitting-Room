# AI-Powered 3D Virtual Fitting Room — Documentation

> **Core principle:** Scan once, save until the customer deletes it, customize clothing anytime.

This folder turns the planning PDF (`AI_3D_Virtual_Fitting_Room_Step_by_Step_Plan.pdf`, v1.0, 20 Nov 2026) into working project documents and a small-task backlog.

## Documents

| # | Document | What it covers |
|---|----------|----------------|
| 1 | [Project overview](01-project-overview.md) | Vision, functional requirements, constraints, out-of-scope |
| 2 | [Architecture](02-architecture.md) | Tech stack, pipeline, folder layout, data model, API, key decisions |
| 3 | [Privacy & security](03-privacy-security.md) | Consent, encryption, access control, deletion rules |
| 4 | [Risks & costs](04-risks-and-costs.md) | Risk register, cost plan, spending order |
| 5 | [MVP acceptance](05-mvp-acceptance.md) | The checklist that defines "MVP done" |
| 6 | [Task backlog](tasks/README.md) | All phases broken into small tasks (≤ 1 day each) |

## Roadmap at a glance

| Phase | Weeks | Goal | Task file |
|-------|-------|------|-----------|
| 0 | Day 1 | First five actions | [phase-0-start-today.md](tasks/phase-0-start-today.md) |
| 1 | 1 | Requirements & prototype design | [phase-1-requirements.md](tasks/phase-1-requirements.md) |
| 2 | 2–3 | App foundation (frontend, backend, DB, auth, catalog) | [phase-2-foundation.md](tasks/phase-2-foundation.md) |
| 3 | 4–5 | Camera capture & upload with quality checks | [phase-3-capture.md](tasks/phase-3-capture.md) |
| 4 | 6–9 | 3D reconstruction proof of concept | [phase-4-reconstruction.md](tasks/phase-4-reconstruction.md) |
| 5 | 10–11 | Saved profiles & 360° viewer | [phase-5-profiles-viewer.md](tasks/phase-5-profiles-viewer.md) |
| 6 | 12–16+ | Clothing catalog & try-on | [phase-6-try-on.md](tasks/phase-6-try-on.md) |
| 7 | 17–18 | Privacy, reliability & testing | [phase-7-hardening.md](tasks/phase-7-hardening.md) |
| 8 | 19–20+ | Pilot & release decision | [phase-8-pilot.md](tasks/phase-8-pilot.md) |

> The schedule is an illustrative estimate, not a delivery date. The most uncertain part is producing a reusable, realistic body mesh from ordinary phone images, so Phase 4 decides whether the later phases work as planned.

## Current project state (20 Nov 2026)

- ✅ SvelteKit + TypeScript + Tailwind CSS starter at the repo root (`src/`, placeholder fitting-room page, `Garment` type).
- ❌ No Git repository yet.
- ❌ No backend (FastAPI), database, auth, capture, reconstruction or 3D viewer yet.

Start with [Phase 0](tasks/phase-0-start-today.md).
