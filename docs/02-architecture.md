# 2. Architecture

## 2.1 Technology stack

| Layer | Tools | Purpose |
|-------|-------|---------|
| Frontend | SvelteKit + TypeScript + Tailwind CSS | Catalog, dashboard, capture workflow |
| 3D viewer | Three.js / Threlte | Render and rotate the person and garments |
| Backend | Python + FastAPI | REST API and processing jobs |
| Computer vision | OpenCV + MediaPipe | Capture quality checks, pose landmarks |
| 3D reconstruction | Photogrammetry / body-template fitting (chosen in Phase 4) | Build a body-like 3D representation |
| 3D editing | Blender (+ Python scripting) | Clean meshes, align garments, export GLB |
| Database | SQLite (prototype) → PostgreSQL | Accounts, catalog, model metadata, jobs |
| File storage | Local encrypted storage (prototype) | Private scans and 3D assets |
| Dev environment | MacBook + VS Code + Git | Build and test locally |

## 2.2 Processing pipeline

```text
 Phone (browser)                      MacBook backend                                Browser
 ───────────────                      ───────────────                                ───────
 Guided capture ──HTTPS upload──▶ Store encrypted raw captures
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
consents         id, user_id, version, scope, granted_at, withdrawn_at
capture_sessions id, user_id, status[uploading|checking|rejected|accepted], created_at
capture_files    id, session_id, kind[photo|video], view[front|left|back|right|other],
                 storage_key, quality_json, created_at
body_models      id, user_id, session_id, status[queued|processing|review|ready|failed],
                 method, glb_storage_key, metrics_json, created_at
jobs             id, type, ref_id, status, progress, error, started_at, finished_at
garments         id, name, category[top|bottom], glb_url, thumbnail_url, sizes_json, active
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
| `POST /captures/{id}/files` | Upload one photo/video (size + type limits) |
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
| D2 | Reconstruction tool | Phase 4 | Candidates: Apple Object Capture (RealityKit, runs on macOS), COLMAP + OpenMVS, SMPL-X fitting from MediaPipe/2D keypoints. Many research repos need an NVIDIA CUDA GPU, so check Mac support first. |
| D3 | Model licenses | Phase 4 | SMPL/SMPL-X are free for **non-commercial research only**. Commercial use needs a separate license. Check before choosing. |
| D4 | Job runner | Phase 2 | Start with a simple DB-backed worker process. Move to a Redis queue (RQ/Celery) only if needed. |
| D5 | Garment fitting method | Phase 6 | Rigid alignment → skinned garments on shared skeleton → cloth simulation (only if needed). |
| D6 | Auth approach | Phase 2 | Session cookies + Argon2 password hashing, or an auth library. |
