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

## Quality targets to measure (set exact numbers in Phase 1)

| Metric | Example target |
|--------|----------------|
| Capture success rate (session accepted by quality checks) | ≥ 80% on 2nd attempt |
| Reconstruction time on MacBook | Measured in Phase 4; displayed to user |
| Viewer first load (model + 1 outfit) | < 5 s on local network |
| Garment swap time | < 1 s |
| Testers who understand "visual preview, not size" | ≥ 90% in pilot survey |
