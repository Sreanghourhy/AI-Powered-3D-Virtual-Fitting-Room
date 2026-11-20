# 5. MVP Acceptance Checklist (v3, CR-02)

The MVP is **done** only when every item passes on the owner's MacBook, with the owner as the scanned person.

| # | Criterion | How to verify | Built in |
|---|-----------|---------------|----------|
| A1 | The app opens **directly** to the fitting room. **Start Scan** → allow camera → guided multi-angle capture (8 body views + face close-ups) → review and retake work. | Manual run in Chrome and Safari; no login or profile screen appears | P2R, P3 |
| A2 | **Generate 3D Model** produces a model of the **actual captured person**. If it can't, a clear failure with reasons is shown and **no generic avatar** appears. | Successful run + a deliberately bad scan | P3, P4 |
| A3 | The model rotates 360° and zooms in the browser viewer | Drag to rotate a full circle, scroll to zoom | P5 |
| A4 | At least **2 shirts and 2 pants** can be switched **independently** on the generated model | All 4 combinations render without reloading the body | P6 |
| A5 | Privacy: camera off outside scanning; images and model stored **only on this MacBook**, encrypted; backend reachable only from localhost; **Discard** removes everything | Camera light check; file inspection; host/header tests; discard test | P2R, P3, P7 |
| A6 | Limits are disclosed: visual preview only, model approximation, failed experiments documented | Notices visible; feasibility report complete | P3, P4, P7 |

## Quality targets

| ID | Metric | Target | How measured | Phase |
|----|--------|--------|--------------|-------|
| Q1 | Scan accepted by quality checks | **≥ 60% first try, ≥ 85% by 2nd try** | Scan status log | P3, P8 |
| Q2 | Time to complete a scan (alone) | **≤ 4 min** | Start → Generate timestamps | P3 |
| Q3 | Reconstruction success (accepted scan → `ready`) | **≥ 80%** of good scans | Job status | P4 |
| Q4 | Reconstruction time on the M4 Pro | **≤ 30 min** (revise after Phase 4 benchmarks) | Job timestamps | P4 |
| Q5 | Likeness (owner's own rating) | silhouette ≥ 3.5 / 5, face ≥ 3 / 5 | Self-rating per scan | P4, P8 |
| Q6 | Model file size | **≤ 15 MB** | GLB size | P4 |
| Q7 | Viewer first load (model + outfit) | **≤ 5 s** | Browser timing | P5 |
| Q8 | Garment swap (cached / first load) | **≤ 0.3 s / ≤ 1.5 s** | Browser timing | P6 |
| Q9 | Viewer frame rate while rotating | **≥ 30 fps** | Browser perf tools | P5 |
| Q10 | Files left after Discard | **0** | Automated test | P2R, P7 |
| Q11 | Requests accepted from a non-localhost Host / without the write header | **0** | Automated test | P2R |

Camera feasibility checks F1–F11 are in [feasibility-macbook-camera.md §8](feasibility-macbook-camera.md#8-go--no-go-criteria-measured-in-p3-01-to-p3-05). Targets can be revised after measurement; record the change in [change-log.md](change-log.md).
