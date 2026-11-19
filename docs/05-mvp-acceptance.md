# 5. MVP Acceptance Checklist

The MVP is **done** only when every item passes on a real test run with a consenting adult tester.

| # | Criterion | How to verify | Built in |
|---|-----------|---------------|----------|
| A1 | A customer can create an account, consent to capture, and upload one guided multi-angle session | Manual E2E: sign up on phone → consent → capture → upload succeeds | P2, P3 |
| A2 | A model can be generated, reviewed, saved, and reopened after signing out | Sign out → sign in → same model loads | P4, P5 |
| A3 | The model rotates in a browser-based 3D viewer | Drag to rotate 360°, zoom works on desktop and phone | P5 |
| A4 | At least **2 shirts and 2 pants** can be switched independently on a test model | All 4 combinations render without reloading the body | P6 |
| A5 | Customer data is private; the customer can request model deletion | Second user gets 403/404 on first user's model; delete removes all files | P7 |
| A6 | Model fidelity, garment fit and capture limits are clearly disclosed | Disclaimers visible on Consent, My Model and Try-On screens | P1, P7 |

## Quality targets (set in Phase 1, P1-06 — 20 Nov 2026)

| ID | Metric | Target | How measured | Phase |
|----|--------|--------|--------------|-------|
| Q1 | Capture accepted by quality checks | **≥ 60% first try, ≥ 85% by 2nd try** | Session status logs | P3, P8 |
| Q2 | Time to complete capture (first-time user) | **≤ 6 min** | Start→upload timestamps | P3, P8 |
| Q3 | Reconstruction success (accepted capture → `ready` model) | **≥ 80%** | Job status | P4, P8 |
| Q4 | Reconstruction time on the MacBook | **≤ 30 min** per model (measure in Phase 4; revise if needed) | Job timestamps | P4 |
| Q5 | Face likeness rated by the scanned person | **≥ 3.5 / 5** average | Pilot survey | P4, P8 |
| Q6 | Model file size sent to browser | **≤ 15 MB** | GLB size | P4, P5 |
| Q7 | Viewer first load (model + 1 outfit), local network | **≤ 5 s** | Browser timing | P5 |
| Q8 | Garment swap (already cached / first load) | **≤ 0.3 s / ≤ 1.5 s** | Browser timing | P6 |
| Q9 | Viewer frame rate while rotating, mid-range phone | **≥ 30 fps** | Browser perf tools | P5 |
| Q10 | Cross-user data access in tests | **0** | Automated access test | P7 |
| Q11 | Files left after account deletion | **0** | Automated deletion test | P7 |
| Q12 | Testers who understand "visual preview, not size" | **≥ 90%** | Pilot survey | P8 |

These targets are a starting point. Phase 4 may show that Q4 or Q5 needs changing; record any change in an ADR.
