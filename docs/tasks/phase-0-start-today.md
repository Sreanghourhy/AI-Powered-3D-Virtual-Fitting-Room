# Phase 0 — Start Today (Day 1)

**Goal:** Turn the plan's "first five actions" into a working base.
**Deliverable:** Git repo, frontend + backend running, a rotating sample GLB, a capture checklist draft, and one reconstruction experiment started.

---

### P0-01 · Initialize Git repository   `XS` ✅
**Depends on:** —
- [x] `git init` in `ai-powered-3d-virtual-fitting-room/`
- [x] Add to `.gitignore`: `data/`, `backend/.venv/`, `__pycache__/`, `*.pyc`, `pipeline/output/`, `*.blend1`
- [x] Confirm `.env` is ignored (it already is)
- [x] Commit Phase 0 work

**Done when:** `git status` is clean and `.env` / `data/` are not tracked.

### P0-02 · Create backend folder and Python env   `XS` ✅
**Depends on:** P0-01
- [x] Create `backend/` with `pyproject.toml` (Python 3.12+)
- [x] Create a venv: `python3 -m venv backend/.venv`
- [x] Install `fastapi`, `uvicorn[standard]`, `pytest`, `httpx`

**Done when:** `backend/.venv/bin/python -c "import fastapi"` works.

### P0-03 · FastAPI health endpoint   `XS` ✅
**Depends on:** P0-02
- [x] `backend/app/main.py` with `GET /health` → `{"status": "ok"}`
- [x] Add a pytest test for `/health`
- [x] Run: `uvicorn app.main:app --reload --port 8000`

**Done when:** `curl localhost:8000/health` returns ok and `pytest` passes.

### P0-04 · Install Three.js and load a sample GLB   `S` ✅
**Depends on:** P0-01
- [x] `npm install three @threlte/core @threlte/extras` and `npm install -D @types/three`
- [x] Download a free, licensed sample human GLB into `static/models/sample.glb` (note the license in `static/models/README.md`)
- [x] Create `src/lib/components/fitting-room/ModelViewer.svelte` with OrbitControls (rotate + zoom), lights, and a ground plane
- [x] Show it on a new route `/viewer-demo`

**Done when:** the sample model rotates 360° with mouse/touch at `/viewer-demo`.

### P0-05 · Connect frontend to backend   `XS` ✅
**Depends on:** P0-03
- [x] Add a Vite dev proxy `/api → http://localhost:8000`
- [x] Show backend health status on the home page

**Done when:** the home page shows "Backend: ok" when FastAPI is running.

### P0-06 · Draft the photo-capture checklist   `S`
**Depends on:** —
- [x] Write `docs/capture-guide.md` covering: lighting (even, no strong backlight), background (plain), clothing (fitted, solid colour, no logos), hair (tied back), pose (A-pose, arms ~30° from body, feet shoulder-width), distance (whole body in frame + margin), angles (every ~15–20° around the person, 2 heights), phone (fixed exposure, 1080p+)
- [ ] ~~Collect authorized sample images with a phone~~ → **moved to P3-05** (MacBook camera sample capture, 20 Nov 2026)

**Done when:** the checklist exists and one full sample capture set is stored **outside Git** in `data/samples/`.

### P0-07 · ⚠️ First reconstruction experiment   `M`
**Depends on:** P0-06
- [ ] ~~Try one quick method on the sample set~~ → **moved to P3-05** (reconstruction smoke test)
- [ ] ~~Record in `docs/experiments/000-first-try.md`~~ → recorded in the feasibility report instead

**Done when:** you have *any* 3D output (even a bad one) plus written notes. Don't pick a final method yet; that happens in Phase 4.
