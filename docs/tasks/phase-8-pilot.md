# Phase 8 — Pilot & Improvement (Weeks 19–20+)

**Goal:** Test with real, willing users and decide whether to release.
**Deliverable:** Pilot evaluation and release decision.

---

### P8-01 · Pilot plan   `S`
**Depends on:** P7-15
- [ ] Number of participants (e.g. 5–10 consenting adults), location, lighting setup, duration
- [ ] What to measure (see P8-03) and how

**Done when:** `docs/pilot-plan.md` written.

### P8-02 · 🔒 Recruit and consent participants   `S`
**Depends on:** P8-01
- [ ] Pilot information sheet + app consent; adults only
- [ ] Explain how to delete data after the pilot

**Done when:** participants confirmed with consent records.

### P8-03 · Add measurement events   `S`
**Depends on:** P8-01
- [ ] Count (no personal data): capture attempts, accepted/rejected + reason, job duration, viewer load time, garment swap time

**Done when:** metrics can be exported as a CSV.

### P8-04 · Short user survey   `XS`
**Depends on:** P8-01
- [ ] Likeness rating, ease of capture, would you use it, **"Does the try-on show your exact size?"** (comprehension check, expected answer: no)

**Done when:** survey ready.

### P8-05 · Run pilot sessions   `M`
**Depends on:** P8-02…P8-04
- [ ] Observe without helping (note where people get stuck)

**Done when:** all planned sessions completed.

### P8-06 · Analyze results   `S`
**Depends on:** P8-05
- [ ] Capture success rate, model quality scores, try-on latency, user comprehension vs. Phase 1 targets

**Done when:** results table in `docs/pilot-report.md`.

### P8-07 · Defect triage   `S`
**Depends on:** P8-06
- [ ] List defects; label P0 (blocker), P1, P2
- [ ] Fix all P0 privacy/security and data-loss defects before any public release

**Done when:** prioritized defect list exists; P0s assigned.

### P8-08 · Release decision   `XS`
**Depends on:** P8-07
- [ ] Go / No-go / Another pilot round, with reasons
- [ ] If go: plan hosting, domain, backups, monitoring and their costs ([04-risks-and-costs.md](../04-risks-and-costs.md))

**Done when:** decision recorded in `docs/adr/`.

### P8-09 · 🔒 Pilot data cleanup   `XS`
**Depends on:** P8-06
- [ ] Delete pilot participant data as promised (unless they chose to keep it)

**Done when:** deletion confirmed and logged.
