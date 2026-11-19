# 4. Risks & Costs

## 4.1 Risk register

| # | Risk | Impact | Likelihood | Mitigation | Owner phase |
|---|------|--------|------------|------------|-------------|
| R1 | **Poor 3D accuracy** from phone images | High | High | Standardize lighting, angles, distance and clothing (fitted clothes, hair tied). Evaluate reconstruction **before** building the full catalog. | 3, 4 |
| R2 | **Scan mesh can't take new clothes** (original clothing baked in) | High | High | Research body-template fitting and retopology **early** (Phase 4), not after the UI is finished. | 4 |
| R3 | **Garment fit looks unrealistic** | Medium | High | Start with a small curated set of prepared garments. Label results as visual previews. | 6 |
| R4 | **Long processing times** on a MacBook | Medium | Medium | Async jobs with progress display. Never promise instant results. Benchmark early. | 2, 4 |
| R5 | **Sensitive personal data** leak or misuse | Very high | Low–Medium | Consent, access control, encryption, minimization, deletion from day 1. See [03-privacy-security.md](03-privacy-security.md). | All |
| R6 | **Model/tool licenses** block commercial use (e.g. SMPL-X) | High | Medium | Check licenses in Phase 4 before committing. Prefer permissive options. | 4 |
| R7 | **Mac-only hardware**: many research repos need NVIDIA CUDA | Medium | High | Prefer Mac-native tools (Apple Object Capture, CPU/MPS paths). Rent a GPU only after a concrete bottleneck shows up. | 4 |
| R8 | **Phone camera in browser** needs HTTPS (no camera access over plain `http://` LAN IP) | Low | High | Run the dev server with a local HTTPS certificate (e.g. mkcert). | 3 |

## 4.2 Costs

### Free for the prototype (subject to each project's license)
SvelteKit, FastAPI, MediaPipe, OpenCV, Blender, Three.js, SQLite/PostgreSQL, a MacBook, and an existing phone.

### Possible paid items (only when needed)
| Item | When it becomes necessary |
|------|---------------------------|
| GPU compute (cloud) | Reconstruction or AI fitting is too slow, or won't run, on the MacBook |
| Garment 3D assets (buy or commission) | After the try-on approach works with 2+2 test garments |
| Commercial model license (e.g. SMPL-X) | If a licensed body model is chosen for a commercial product |
| Cloud storage, hosting, domain, backups | Before a public deployment |
| Security monitoring | Before handling real customers at scale |

No reliable fixed budget is possible before benchmarking.

### Spending order
1. **$0** software proof of concept.
2. Benchmark 3D reconstruction on the available MacBook.
3. Pay for GPU or assets **only** after the proof of concept shows a concrete bottleneck.
