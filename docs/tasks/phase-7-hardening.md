# Phase 7 — Privacy, Reliability & Testing (CR-02, single user, local)

> **Rewritten 20 Nov 2026 (CR-02):** no accounts, so no access-control audit between users. Focus on localhost protection, discard, local data and reliability.

**Goal:** Make the prototype safe and dependable for daily personal use.
**Deliverable:** Test report and a tagged prototype build.

---

### P7-01 · 🔒 Localhost protection audit   `S`
- [ ] Every endpoint behind the Host check and write-header rule; 127.0.0.1 binding confirmed (TC-57 to TC-60)

**Done when:** an automated test covers every state-changing endpoint.

### P7-02 · 🔒 Discard completeness   `S`
- [ ] Discard removes rows and blobs for scans, images, models, jobs and outfit; temp files from failed jobs too

**Done when:** TC-44 passes after a full scan → generate → try-on cycle.

### P7-03 · 🔒 Raw image lifetime   `XS`
- [ ] Confirm images are kept only until Discard (or a rescan replaces them); document it in the privacy notice

**Done when:** behaviour matches [03-privacy-security.md](../03-privacy-security.md) §3.3.

### P7-04 · 🔒 Encryption and secrets review   `S`
- [ ] No plaintext images/GLB on disk; key not in Git; key-loss consequence documented

**Done when:** checklist signed off.

### P7-05 · 🔒 Camera privacy review   `XS`
- [ ] Camera off outside `/scan`; no third-party requests while the camera is on (TC-51, TC-61)

**Done when:** verified in Chrome and Safari.

### P7-06 · 🔒 Upload limits   `XS`
- [ ] Oversized, fake-type and too-many uploads rejected (413/415/422)

**Done when:** tests pass.

### P7-07 · 🔒 Dependency and secret scan   `XS`
- [ ] `npm audit`, `pip-audit`; scan Git history for secrets

**Done when:** no high/critical issues open.

### P7-08 · Job robustness   `S`
- [ ] Worker restart marks interrupted jobs failed; disk-space check before reconstruction; timeouts

**Done when:** killing the worker mid-job leaves a clear failed state with Try again.

### P7-09 · Logging without personal data   `XS`
- [ ] No images, file contents or paths of personal files in logs

**Done when:** a log review is clean.

### P7-10 · End-to-end test suite   `M`
- [ ] Playwright: open `/` → (fixture) scan → generate → try 2×2 → reload → discard

**Done when:** the full flow passes in one command.

### P7-11 · Variation testing (owner)   `M`
- [ ] Owner scans in different clothes, lighting and times; record failures honestly; no accuracy claims

**Done when:** results table in the test report.

### P7-12 · Test report + tagged build   `S`
- [ ] `docs/test-report.md`: passed, failed, limits, open risks; Git tag `v0.1-prototype`

**Done when:** report written and tag pushed.
