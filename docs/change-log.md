# Change Log — Requirements

## CR-01 · MacBook built-in camera replaces phone capture (20 Nov 2026)

**Requested by:** project owner · **Status:** 📝 docs updated, **waiting for owner approval** · **Code:** not changed yet

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
