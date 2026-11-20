# 4. Risks & Costs

## 4.1 Risk register

| # | Risk | Impact | Likelihood | Mitigation | Owner phase |
|---|------|--------|------------|------------|-------------|
| R1 | **Poor 3D accuracy** from laptop-camera images | High | High | Standardize lighting, distance (floor marker) and clothing. **Feasibility gate (P3-01 to P3-05)** before building the capture flow; evaluate reconstruction **before** building the full catalog. | 3, 4 |
| R2 | **Scan mesh can't take new clothes** (original clothing baked in) | High | High | Research body-template fitting and retopology **early** (Phase 4), not after the UI is finished. | 4 |
| R3 | **Garment fit looks unrealistic** | Medium | High | Start with a small curated set of prepared garments. Label results as visual previews. | 6 |
| R4 | **Long processing times** on a MacBook | Medium | Medium | Async jobs with progress display. Never promise instant results. Benchmark early. | 2, 4 |
| R5 | **Sensitive personal data** (your face/body images) leak | High | Low | Local only, encrypted at rest, camera off outside scanning, Discard. See [03-privacy-security.md](03-privacy-security.md). | All |
| R6 | **Model/tool licenses** block commercial use (e.g. SMPL-X) | High | Medium | Check licenses in Phase 4 before committing. Prefer permissive options. | 4 |
| R7 | **Mac-only hardware**: many research repos need NVIDIA CUDA | Medium | High | Prefer Mac-native tools (Apple Object Capture, CPU/MPS paths). Rent a GPU only after a concrete bottleneck shows up. | 4 |
| R8 | **macOS video effects** (Center Stage auto-framing, Portrait blur, Studio Light) change framing or appearance | High | Medium | Setup checklist; framing-consistency check (`framing_changed`); test detection in P3-02 | 3 |
| R9 | **Fixed camera geometry**: landscape only, ~2.5 m distance, face only ~85 px wide in body views | High | High | Separate face close-ups; template-fitting approach; measure in P3-02 | 3, 4 |
| R10 | **Person moves between views** (turning changes arm pose or position) | High | Medium | Floor marker, A-pose cues, stillness-based auto-capture, consistency checks (`distance_changed`, `pose_changed`) | 3 |
| R12 | **No authentication**: other websites in the same browser, or DNS rebinding, could try to call the local backend | High | Low–Medium | 127.0.0.1 bind, Host allow-list, `X-Fitting-Room` header on writes, no CORS (P2R-02) | 2R |
| R13 | **Reconstruction fails or looks wrong**, tempting a generic-avatar fallback | High | Medium | Explicit failure state with reasons; tests forbid any avatar fallback (TC-23, TC-55); log failed experiments | 4 |
| R11 | **Browser camera controls** (exposure / white-balance lock) may be unsupported in Safari/Chrome on macOS | Medium | Medium | Measure in P3-01; rely on stable front lighting + brightness checks | 3 |

## 4.2 Costs

### Free for the prototype (subject to each project's license)
SvelteKit, FastAPI, MediaPipe, OpenCV, Blender, Three.js, SQLite/PostgreSQL, and the MacBook with its built-in camera.

### Possible paid items (only when needed)
| Item | When it becomes necessary |
|------|---------------------------|
| GPU compute (cloud) | Reconstruction or AI fitting is too slow, or won't run, on the MacBook |
| Garment 3D assets (buy or commission) | After the try-on approach works with 2+2 test garments |
| Soft lights for the capture area | If P3-03 shows room lighting is too uneven (low cost) |
| Better external USB webcam | **Only** if the feasibility gate fails on resolution or face detail. Requires owner approval (requirement change). |
| Commercial model license (e.g. SMPL-X) | If a licensed body model is chosen for a commercial product |
| Cloud storage, hosting, domain, backups | Before a public deployment |
| Security monitoring | Only if the app is ever used by other people online (new change request) |

No reliable fixed budget is possible before benchmarking.

### Spending order
1. **$0** software proof of concept.
2. Benchmark 3D reconstruction on the available MacBook.
3. Pay for GPU or assets **only** after the proof of concept shows a concrete bottleneck.
