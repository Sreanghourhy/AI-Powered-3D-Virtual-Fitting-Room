# 2. Architecture (v3, CR-02, 20 Nov 2026)

> **Status:** ✅ approved 20 Nov 2026. Single-user, local-only. No accounts or authentication.

## 2.1 Technology stack

| Layer | Tools | Purpose |
|-------|-------|---------|
| Frontend | SvelteKit 3 + TypeScript + Tailwind CSS 4 | Fitting-room interface, scan flow |
| Camera | Browser MediaDevices API (`getUserMedia`), MacBook built-in camera | Live preview and still capture |
| Computer vision (browser) | MediaPipe Tasks Vision (WASM, models **self-hosted**) | Live pose, orientation, stillness, guidance, auto-capture |
| 3D viewer | Three.js + Threlte | 360° viewer, garment layering |
| Backend | Python 3.12 + FastAPI, bound to **127.0.0.1** | Image upload, quality checks, reconstruction jobs, catalog |
| Computer vision (backend) | OpenCV + MediaPipe (Python) | Server-side quality and consistency checks |
| 3D reconstruction | Body-template fitting (primary) / photogrammetry (comparison), chosen after feasibility tests | Real-person 3D model from the captured views |
| 3D editing | Blender (Python scripting, headless) | Mesh cleanup, garment preparation, GLB export |
| Database | SQLite (`data/app.db`) | Scan, model, job and catalog metadata |
| File storage | Local encrypted storage (`data/blobs/`, AES-256-GCM) | Captured images and generated models |
| Dev environment | MacBook (M4 Pro) + VS Code + Git | Build, run and test locally |

## 2.2 Pipeline

```text
 Browser on the MacBook                                  Backend on the same MacBook (127.0.0.1)
 ──────────────────────                                  ─────────────────────────────────────
 /  Fitting room ── Start Scan ──▶ /scan
                                    privacy notice (first time)
                                    getUserMedia (built-in camera)
                                    calibration → 8 body views (turn 45°) → 5 face close-ups
                                    MediaPipe: pose, orientation, stillness → auto-capture
                                    review / retake      (images in memory only)
                                    Generate 3D Model ──────upload──▶ encrypted storage (data/blobs)
                                    camera stops                       quality + consistency checks
                                                                          │ ok          │ fail → reasons to UI
                                                                          ▼
                                                                  reconstruction job (worker)
                                                                          │ ok          │ fail → failure + reasons
                                                                          ▼               (NO avatar fallback)
 /  Fitting room ◀── poll job progress ─────────────────────────  encrypted GLB
    360° viewer + shirt / pants pickers ◀── GLB stream ──────────
    Discard scan & model ─────────────────────────────────────▶  delete images, model, jobs, blobs
```

## 2.3 Repository layout

```text
src/                         # SvelteKit frontend
  routes/
    +page.svelte             # Fitting room (main interface)            [P2R-05]
    scan/                    # Guided capture                            [Phase 3]
    catalog/                 # Optional browse page
    viewer-demo/             # Dev-only viewer test with public sample
    dev/camera-lab/          # Dev-only feasibility tests (blocked in production) [P3-01]
  lib/components/
    fitting-room/  garments/  capture/  ui/
backend/app/
  api/                       # health, garments, scans, models, jobs, data (discard)
  core/  db/  services/  worker/
pipeline/                    # Reconstruction experiments + Blender scripts
data/                        # LOCAL ONLY, git-ignored: app.db + encrypted blobs
docs/
```

## 2.4 Data model (single user)

```text
scans          id, status[capturing|checking|rejected|accepted], calibration_json, created_at
scan_images    id, scan_id, view[front|front_right|right|back_right|back|back_left|left|front_left|
               face_front|face_left_45|face_right_45|face_left_90|face_right_90],
               storage_key, width, height, quality_json, created_at
body_models    id, scan_id, status[queued|processing|ready|failed], method, glb_storage_key,
               metrics_json, failure_reason, created_at
jobs           id, type, ref_id, payload, status, progress, step, error, created_at, started_at, finished_at
garments       id(slug), name, category[top|bottom], model_url, thumbnail_url, colors, sizes,
               source_author, source_license, source_url, active, sort_order        (exists)
outfit         id=1, top_garment_id, bottom_garment_id, updated_at                  (single row)
audit_log      id, action, target, created_at                                       (no user column)
```

- **Only one "current" scan and model.** A new scan replaces the previous one after the new model is ready, or when the user discards.
- Removed in P2R-01: `users`, `sessions`, `consents`, and every `user_id` column.

## 2.5 API (no authentication; localhost only)

| Method & path | Purpose |
|---------------|---------|
| `GET /health` | Health check (exists) |
| `GET /garments?category=top\|bottom`, `GET /garments/{id}` | Catalog (exists) |
| `POST /scans` | Start a scan session |
| `POST /scans/{id}/images` / `DELETE /scans/{id}/images/{imageId}` | Upload one view / remove it (retake) |
| `POST /scans/{id}/generate` | Run checks; if OK, queue reconstruction (the **Generate 3D Model** button) |
| `GET /models/current` | Current model status, metrics, failure reason |
| `GET /models/current/asset` | Stream the decrypted GLB (`Cache-Control: no-store`) |
| `GET /jobs/{id}` | Job progress (exists, owner check removed) |
| `GET/PUT /outfit` | Current shirt + pants |
| `DELETE /data` | **Discard** all scans, images, models, jobs, blobs, outfit |

**Localhost protection** (P2R-02): the server listens on 127.0.0.1 only; the `Host` header must be `localhost` or `127.0.0.1`; state-changing requests need the header `X-Fitting-Room: 1`; no CORS. Other websites open in the same browser can't send that header without a preflight, and the server refuses the preflight.

## 2.6 Decision log

| # | Decision | Status | Notes |
|---|----------|--------|-------|
| D1 | Body representation | Phase 4 | Must be a **real-person** representation that also supports garments (F11) |
| D2 | Reconstruction tool | Phase 4 (smoke test in P3-05) | Template fitting from silhouettes + keypoints primary; photogrammetry comparison only. Check Apple-silicon support and licenses. |
| D3 | Model licenses | Phase 4 | SMPL/SMPL-X are non-commercial research licenses; acceptable for a personal prototype, but recorded |
| D4 | Job runner | ✅ Phase 2 | DB-backed worker, one job at a time |
| D5 | Garment fitting method | Phase 6 | Skinned garments on the template skeleton → cloth simulation only if needed |
| D6 | Auth approach | ❌ **Retired by CR-02** | Session + Argon2 auth removed in P2R-01 |
| D7 | Capture method | ✅ CR-01 | MacBook built-in camera, person turns, 8 body views + 5 face close-ups, auto-capture |
| D8 | In-browser computer vision | ✅ CR-01 | MediaPipe Tasks Vision, self-hosted models |
| D9 | Single-user local mode | ✅ CR-02, approved 20 Nov 2026 | No users, sessions or consents; one current scan/model |
| D10 | Localhost protection | ✅ CR-02, approved 20 Nov 2026 | 127.0.0.1 bind, Host allow-list, custom header on writes, no CORS |
| D11 | Local persistence | ✅ CR-02, approved 20 Nov 2026 | Keep the latest scan/model encrypted in `data/` until Discard |
