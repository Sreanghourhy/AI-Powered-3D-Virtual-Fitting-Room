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

### Phase 1 design documents

| Document | What it covers |
|----------|----------------|
| [User flows](user-flows.md) | Sign up → scan, return visit, delete, retake |
| [Consent text v1](consent-v1.md) | Superseded by v2 (phone wording) |
| [Capture guide](capture-guide.md) / [Capture steps](capture-steps.md) | MacBook-camera setup and pose / on-screen steps and error messages |
| [Feasibility: MacBook camera](feasibility-macbook-camera.md) | Can the built-in camera give a usable 3D model? Assessment + go/no-go checks |
| [Consent text v2](consent-v2.md) | Draft for MacBook capture (replaces v1 after approval) |
| [Change log](change-log.md) | Requirement changes and what they affected |
| [Garment format](garment-format.md) | GLB spec + metadata for catalog items |
| [Wireframes](wireframes/README.md) | Consent, Capture, My Model, Catalog, Try-On |
| [Test cases](test-cases.md) | TC-01…TC-50 mapped to MVP items A1–A6 |

## Roadmap at a glance

| Phase | Weeks | Goal | Task file |
|-------|-------|------|-----------|
| 0 | Day 1 | First five actions | [phase-0-start-today.md](tasks/phase-0-start-today.md) |
| 1 | 1 | Requirements & prototype design | [phase-1-requirements.md](tasks/phase-1-requirements.md) |
| 2 | 2–3 | App foundation (frontend, backend, DB, auth, catalog) | [phase-2-foundation.md](tasks/phase-2-foundation.md) |
| 3 | 4–5+ | **MacBook camera** capture: feasibility gate, then capture + quality checks | [phase-3-capture.md](tasks/phase-3-capture.md) |
| 4 | 6–9 | 3D reconstruction proof of concept | [phase-4-reconstruction.md](tasks/phase-4-reconstruction.md) |
| 5 | 10–11 | Saved profiles & 360° viewer | [phase-5-profiles-viewer.md](tasks/phase-5-profiles-viewer.md) |
| 6 | 12–16+ | Clothing catalog & try-on | [phase-6-try-on.md](tasks/phase-6-try-on.md) |
| 7 | 17–18 | Privacy, reliability & testing | [phase-7-hardening.md](tasks/phase-7-hardening.md) |
| 8 | 19–20+ | Pilot & release decision | [phase-8-pilot.md](tasks/phase-8-pilot.md) |

> The schedule is an illustrative estimate, not a delivery date. The most uncertain part is producing a reusable, realistic body mesh from a **fixed laptop camera**, so the Phase 3 feasibility gate and Phase 4 decide whether the later phases work as planned.

## Current project state (20 Nov 2026)

- ✅ SvelteKit + TypeScript + Tailwind CSS starter at the repo root (`src/`, placeholder fitting-room page, `Garment` type).
- ✅ Git repo (GitHub remote), FastAPI backend with `/health`, Three.js viewer demo at `/viewer-demo`, frontend ↔ backend proxy.
- ✅ Phase 1 complete and approved (20 Nov 2026).
- ✅ Phase 2 complete and approved: database, sign-in, consent, catalog, encrypted storage, job worker, Try-On/My Model placeholders.
- ✅ **20 Nov 2026 requirement change approved:** capture uses the **MacBook built-in camera** (no phone). See [change-log.md](change-log.md). P3-00 done (consent-v2 live).
- ❌ No capture or reconstruction yet. Next: [Phase 3](tasks/phase-3-capture.md), starting with the camera feasibility gate.

Start with [Phase 0](tasks/phase-0-start-today.md).
