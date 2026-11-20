# 2. Architecture

## 2.1 Technology stack

| Layer | Tools | Purpose |
|-------|-------|---------|
| Frontend | SvelteKit + TypeScript + Tailwind CSS | Catalog, dashboard, capture workflow |
| 3D viewer | Three.js / Threlte | Render and rotate the person and garments |
| Backend | Python + FastAPI | REST API and processing jobs |
| Camera | Browser MediaDevices API (`getUserMedia`) with the MacBook built-in camera | Live preview and still capture in the web app |
| Computer vision (browser) | MediaPipe Tasks Vision (WASM, models served from our own server) | Live pose, orientation, stillness → guidance + auto-capture |
| Computer vision (backend) | OpenCV + MediaPipe (Python) | Server-side quality and consistency checks |
| 3D reconstruction | Body-template fitting (primary) / photogrammetry (comparison), chosen in Phase 4 | Build a body-like 3D representation from few fixed-camera views |
| 3D editing | Blender (+ Python scripting) | Clean meshes, align garments, export GLB |
| Database | SQLite (prototype) → PostgreSQL | Accounts, catalog, model metadata, jobs |
| File storage | Local encrypted storage (prototype) | Private scans and 3D assets |
| Dev environment | MacBook + VS Code + Git | Build and test locally |

## 2.2 Processing pipeline

```text
 MacBook (browser + built-in camera)   MacBook backend (localhost)                   Browser
 ───────────────────────────────────   ───────────────────────────                   ───────
 getUserMedia → calibration →
 8 body views (person turns) + 5 face
 close-ups, auto-capture (MediaPipe)
 → review ──── upload to localhost ──▶ Store encrypted raw captures
                                        │
                                        ▼
                                  Quality checks (blur, light, pose coverage)
                                        │ pass
                                        ▼
                                  Reconstruction / body-fitting JOB (async)
                                        │
                                        ▼
                                  Model review (auto checks + optional manual)
                                        │ approved
                                        ▼
                                  Private 3D asset storage (GLB, encrypted)
                                        │
                                        ▼
                                  Authenticated API ─────────────────▶ 3D viewer (Three.js)
                                                                            │
                                                                            ▼
                                                                  Shirt / pants selection
                                                                            │
                                                                            ▼
                                                                  Garment alignment & render
```

## 2.3 Repository layout (target)

The SvelteKit app already exists at the repo root. Add the backend next to it rather than moving the frontend.

```text
ai-powered-3d-virtual-fitting-room/
├── src/                     # SvelteKit frontend (existing)
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── fitting-room/   # Viewer, try-on controls
│   │   │   ├── garments/       # Catalog cards, selectors
│   │   │   └── capture/        # Camera + guidance overlay (new)
│   │   ├── api/                # Typed client for FastAPI (new)
│   │   └── types/
│   └── routes/
│       ├── login/  signup/  consent/
│       ├── capture/  my-model/  catalog/  try-on/
├── static/models/           # PUBLIC sample models only (never customer data)
├── backend/                 # FastAPI (new)
│   ├── app/
│   │   ├── main.py
│   │   ├── api/             # routers: auth, catalog, captures, models, jobs
│   │   ├── core/            # config, security, crypto
│   │   ├── db/              # SQLAlchemy models, session, Alembic
│   │   ├── services/        # quality checks, storage, reconstruction adapters
│   │   └── worker/          # job runner
│   ├── tests/
│   └── pyproject.toml
├── pipeline/                # Reconstruction experiments + Blender scripts (new)
├── data/                    # LOCAL ONLY, git-ignored: encrypted uploads & assets
└── docs/
```

## 2.4 Data model (first version)

```text
users            id, email, password_hash, created_at, deleted_at
sessions         id, user_id, token_hash, created_at, expires_at
consents         id, user_id, version, scope, granted_at, withdrawn_at
capture_sessions id, user_id, status[capturing|checking|rejected|accepted], calibration_json
                 (person height px, resolution, browser), created_at
capture_files    id, session_id, view[front|front_right|right|back_right|back|back_left|left|
                 front_left|face_front|face_left_45|face_right_45|face_left_90|face_right_90],
                 storage_key, width, height, quality_json, created_at
body_models      id, user_id, session_id, status[queued|processing|review|ready|failed],
                 method, glb_storage_key, metrics_json, created_at
jobs             id, user_id, type, ref_id, payload, status, progress, step, error,
                 created_at, started_at, finished_at
garments         id(slug), name, category[top|bottom], model_url, thumbnail_url, colors, sizes,
                 source_author, source_license, source_url, active, sort_order
outfits          id, user_id, top_garment_id, bottom_garment_id, created_at
audit_log        id, user_id, action, target, created_at
```

Rules:
- `storage_key` is an opaque random ID. Never put file paths or user names in it.
- Customer files live under `data/`, encrypted. They are **never** served from `static/`.

## 2.5 API sketch (FastAPI)

| Method & path | Purpose |
|---------------|---------|
| `GET /health` | Health check |
| `POST /auth/signup`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me` | Accounts (HTTP-only session cookie) |
| `POST /consents` / `DELETE /consents/{id}` | Grant / withdraw consent |
| `GET /garments?category=top` | Catalog |
| `POST /captures` | Start a capture session |
| `POST /captures/{id}/files` | Upload one image with its `view` (JPEG/PNG, size + count limits) |
| `DELETE /captures/{id}/files/{fileId}` | Remove one image (retake) |
| `POST /captures/{id}/submit` | Run quality checks, then queue reconstruction |
| `GET /models/me` | Current user's model metadata + status |
| `GET /models/{id}/asset` | Stream decrypted GLB (owner only) |
| `GET /jobs/{id}` | Job progress for polling |
| `PUT /outfits/current` | Save selected shirt + pants |
| `GET /me/export` | Export the user's data (where feasible) |
| `DELETE /me` | Delete account, model, captures (and schedule backup purge) |

## 2.6 Key decisions to make (decision log)

Write each decision as a short ADR (`docs/adr/NNN-title.md`) when it is made.

| # | Decision | When | Notes |
|---|----------|------|-------|
| D1 | **Body representation**: raw photogrammetry mesh vs. parametric body template (e.g. SMPL-X fitted to the person + texture) vs. hybrid | End of Phase 4 | **Most important decision.** A shared template with a skeleton lets garments be rigged once and fit everyone. A raw scan keeps likeness but includes the original clothes. |
| D2 | Reconstruction tool | Phase 4 (smoke test in P3-05) | With a **fixed camera and a turning person**, body-template fitting from silhouettes + keypoints is the primary candidate; photogrammetry (Apple Object Capture with masks / COLMAP) is a comparison only. Many research repos need an NVIDIA CUDA GPU, so check Mac support first. |
| D3 | Model licenses | Phase 4 | SMPL/SMPL-X are free for **non-commercial research only**. Commercial use needs a separate license. Check before choosing. |
| D4 | Job runner | ✅ Decided, Phase 2 | DB-backed worker (`python -m app.worker`), one job at a time, interrupted jobs marked failed on restart. Move to a Redis queue (RQ/Celery) only if needed. |
| D5 | Garment fitting method | Phase 6 | Rigid alignment → skinned garments on shared skeleton → cloth simulation (only if needed). |
| D7 | Capture method | ✅ Approved 20 Nov 2026 (final confirmation at the P3-05 gate) | MacBook built-in camera via `getUserMedia`; customer alone; person turns on a floor marker; 8 body views + 5 face close-ups; auto-capture. No phone, helper or LAN transfer. See [feasibility-macbook-camera.md](feasibility-macbook-camera.md). |
| D8 | In-browser computer vision | ✅ Approved 20 Nov 2026 | Add `@mediapipe/tasks-vision` to the frontend for live guidance. Model files self-hosted (no third-party requests while the camera is on). |
| D6 | Auth approach | ✅ Decided, Phase 2 | Server-side sessions (SHA-256 of a random token stored; cookie `HttpOnly`/`Secure`/`SameSite=Lax`, 14 days) + Argon2id password hashing. |
