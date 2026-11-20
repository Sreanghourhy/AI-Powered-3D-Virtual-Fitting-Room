# AI-Powered 3D Virtual Fitting Room — Documentation

> **Core principle:** Scan yourself with the MacBook camera, generate a real-person 3D model, try on shirts and pants. Discard anytime. (Single-user prototype, CR-02.)

This folder turns the planning PDF (`AI_3D_Virtual_Fitting_Room_Step_by_Step_Plan.pdf`, v1.0, 20 Nov 2026) into working project documents and a small-task backlog.

## Documents

| # | Document | What it covers |
|---|----------|----------------|
| 1 | [Project overview](01-project-overview.md) | Vision, functional requirements, constraints, out-of-scope |
| 2 | [Architecture](02-architecture.md) | Tech stack, pipeline, folder layout, data model, API, key decisions |
| 3 | [Privacy & security](03-privacy-security.md) | Local data handling, camera, encryption, localhost protection, discard |
| 4 | [Risks & costs](04-risks-and-costs.md) | Risk register, cost plan, spending order |
| 5 | [MVP acceptance](05-mvp-acceptance.md) | The checklist that defines "MVP done" |
| 6 | [Task backlog](tasks/README.md) | All phases broken into small tasks (≤ 1 day each) |

### Phase 1 design documents

| Document | What it covers |
|----------|----------------|
| [User flows](user-flows.md) | Scan → Generate → view; try on; retake / failure; discard (single user) |
| [Privacy notice](privacy-notice.md) | Short in-app notice before the camera starts (replaces consent, CR-02) |
| [Consent text v1](consent-v1.md) / [v2](consent-v2.md) | Retired (CR-02) |
| [Capture guide](capture-guide.md) / [Capture steps](capture-steps.md) | MacBook-camera setup and pose / on-screen steps and error messages |
| [Feasibility: MacBook camera](feasibility-macbook-camera.md) | Can the built-in camera give a usable 3D model? Assessment + go/no-go checks |
| [Change log](change-log.md) | Requirement changes and what they affected |
| [Garment format](garment-format.md) | GLB spec + metadata for catalog items |
| [Wireframes](wireframes/README.md) | Fitting room (main), Scan; older screens marked superseded |
| [Test cases](test-cases.md) | v3 test cases mapped to A1–A6 (removed auth cases listed) |

## Roadmap at a glance

| Phase | Weeks | Goal | Task file |
|-------|-------|------|-----------|
| 0 | Day 1 | First five actions | [phase-0-start-today.md](tasks/phase-0-start-today.md) |
| 1 | 1 | Requirements & prototype design | [phase-1-requirements.md](tasks/phase-1-requirements.md) |
| 2 | 2–3 | App foundation (done; auth parts superseded) | [phase-2-foundation.md](tasks/phase-2-foundation.md) |
| **2R** | ~3 days | **Single-user refactor: remove auth, one fitting-room screen, localhost protection, discard** | [phase-2r-single-user.md](tasks/phase-2r-single-user.md) |
| 3 | 4–5+ | **MacBook camera** capture: feasibility gate, then capture + quality checks | [phase-3-capture.md](tasks/phase-3-capture.md) |
| 4 | 6–9 | 3D reconstruction proof of concept | [phase-4-reconstruction.md](tasks/phase-4-reconstruction.md) |
| 5 | 10–11 | 360° viewer & local persistence | [phase-5-profiles-viewer.md](tasks/phase-5-profiles-viewer.md) |
| 6 | 12–16+ | Clothing catalog & try-on | [phase-6-try-on.md](tasks/phase-6-try-on.md) |
| 7 | 17–18 | Privacy, reliability & testing | [phase-7-hardening.md](tasks/phase-7-hardening.md) |
| 8 | 19–20+ | Personal evaluation & next steps | [phase-8-pilot.md](tasks/phase-8-pilot.md) |

> The schedule is an illustrative estimate, not a delivery date. The most uncertain part is producing a reusable, realistic body mesh from a **fixed laptop camera**, so the Phase 3 feasibility gate and Phase 4 decide whether the later phases work as planned.

## Current project state (20 Nov 2026)

- ✅ Phases 0, 1, 2 done. P3-00 done.
- ✅ **CR-02 (approved 20 Nov 2026):** single-user personal prototype. No login, accounts or profiles; the app opens straight into the fitting room. See [change-log.md](change-log.md).
- ✅ [Phase 2R](tasks/phase-2r-single-user.md) done (waiting for approval): no login, app opens on the fitting room, localhost protection, Discard.
- Next: camera feasibility tests in [Phase 3](tasks/phase-3-capture.md) (P3-01 to P3-05).
