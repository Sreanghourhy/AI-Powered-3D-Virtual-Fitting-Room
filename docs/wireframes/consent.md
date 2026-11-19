# Wireframe — Consent (`/consent`)

Text source: [consent-v1.md](../consent-v1.md).

```text
┌───────────────────────────────┐
│ ←                             │
│  Before we scan you           │
│  ───────────────────────────  │
│  We take photos of you from   │
│  all sides and turn them into │
│  a 3D model so you can try on │
│  clothes.                     │
│                               │
│  ▸ What we collect        [+] │   ← collapsible sections,
│  ▸ Why                    [+] │     "What we collect" and
│  ▸ How we protect it      [+] │     "How long" open by default
│  ▸ How long we keep it    [+] │
│  ▸ Your choices           [+] │
│                               │
│  ┌─────────────────────────┐  │
│  │ ⚠ Visual preview only — │  │   ← always visible
│  │ not a size guarantee.   │  │
│  └─────────────────────────┘  │
│                               │
│  ☐ I am 18+ and I am the      │
│    person being scanned.      │
│  ☐ I agree to the capture and │
│    storage described above.   │
│                               │
│  [ Decline ] [Agree & continue]│  ← Agree disabled until both ticked
└───────────────────────────────┘
```

**States:** first time · re-consent ("We updated our consent text — please review") · already accepted (redirect to `/capture`).
