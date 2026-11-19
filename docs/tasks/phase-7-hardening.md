# Phase 7 — Privacy, Reliability & Testing (Weeks 17–18)

**Goal:** Make the prototype safe to give to pilot users.
**Deliverable:** Test report and a secure pilot build.

> Many privacy controls were already built in earlier phases (🔒 tasks). This phase **verifies** and completes them.
> Checklist source: [03-privacy-security.md](../03-privacy-security.md).

---

## Privacy & security

### P7-01 · 🔒 Access control audit   `S`
**Depends on:** —
- [ ] List every endpoint; confirm auth + owner check
- [ ] Automated test: user B tries every user-A resource URL → 404

**Done when:** test covers 100% of user-data endpoints and passes.

### P7-02 · 🔒 Account & data deletion   `M`
**Depends on:** P2-08
- [ ] `DELETE /me`: delete captures, models, outfits, consents, sessions, blobs; anonymize audit log
- [ ] Confirmation screen ("type DELETE")
- [ ] Test: after deletion, no blob files and no DB rows for that user remain

**Done when:** deletion test passes.

### P7-03 · 🔒 Backup deletion policy   `S`
**Depends on:** P7-02
- [ ] Decide backup method and retention (e.g. 30 days)
- [ ] Deletions list → purge from backups or let them expire; document it
- [ ] Mention the purge time in the consent text

**Done when:** `docs/backup-policy.md` written and consent text updated (v2 if changed).

### P7-04 · 🔒 Data export   `S`
**Depends on:** P5-02
- [ ] `GET /me/export` → ZIP with account info JSON, consent history, model GLB

**Done when:** the export downloads and opens.

### P7-05 · 🔒 Encryption & secrets review   `S`
**Depends on:** —
- [ ] Confirm no plaintext customer files on disk (`grep` image magic bytes in `data/`)
- [ ] Keys not in Git; key rotation procedure written

**Done when:** checklist signed off.

### P7-06 · 🔒 Raw capture minimization   `S`
**Depends on:** P4-13
- [ ] Delete raw photos/videos after model is `ready` (unless the user opted in to keep them)
- [ ] Clean temp dirs after every job (including failed ones)

**Done when:** test shows raw files gone after a successful job.

### P7-07 · 🔒 Rate limits & upload limits   `S`
**Depends on:** P3-03
- [ ] Rate-limit login, signup and uploads
- [ ] Verify size/count/type limits with oversized and fake files

**Done when:** abuse tests return 413/415/429 as expected.

### P7-08 · 🔒 Security headers & cookies   `XS`
**Depends on:** —
- [ ] CSP, `X-Content-Type-Options`, `Referrer-Policy`; cookies `HttpOnly`/`Secure`/`SameSite`

**Done when:** headers verified in browser dev tools.

### P7-09 · 🔒 Dependency & secret scan   `XS`
**Depends on:** —
- [ ] `npm audit`, `pip-audit`; scan Git history for secrets

**Done when:** no high/critical issues open.

## Reliability

### P7-10 · Job robustness   `S`
**Depends on:** P4-14
- [ ] Worker restart resumes/fails stuck jobs; one job at a time to protect the Mac
- [ ] Disk-space check before a job

**Done when:** killing the worker mid-job leaves a clear `failed`/retry state.

### P7-11 · Logging without personal data   `S`
**Depends on:** —
- [ ] Structured logs; no images, emails or tokens in logs

**Done when:** a log review shows no personal data.

### P7-12 · Move to PostgreSQL (if pilot needs it)   `S`
**Depends on:** —
- [ ] Run Alembic migrations on Postgres; run all tests

**Done when:** tests pass on Postgres (or decision to keep SQLite for pilot is recorded).

## Testing

### P7-13 · End-to-end test suite   `M`
**Depends on:** P5-11, P6-16
- [ ] Playwright: signup → consent → (fixture) upload → model ready → try-on 2×2 → export → delete

**Done when:** full flow passes in one command.

### P7-14 · Variation testing   `M`
**Depends on:** —
- [ ] Test across body types, poses, skin tones, hair, lighting and all garments (consenting adults)
- [ ] Record failures honestly. Don't claim perfect accuracy.

**Done when:** results table in the test report.

### P7-15 · Test report + pilot build   `S`
**Depends on:** all above
- [ ] `docs/test-report.md`: what passed, what failed, known limitations, open risks
- [ ] Tag a pilot release in Git

**Done when:** report written and `v0.1-pilot` tag created.
