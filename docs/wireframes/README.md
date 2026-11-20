# Wireframes (v1)

Low-fidelity text wireframes. They fix **layout and content**, not colours or fonts. The UI follows the existing Tailwind style: slate text, indigo accent, rounded cards.

| Screen | File | Route | Flow |
|--------|------|-------|------|
| Consent | [consent.md](consent.md) | `/consent` | 1 |
| Capture | [capture.md](capture.md) | `/capture` | 1, 4 |
| My Model | [my-model.md](my-model.md) | `/my-model` | 1, 3 |
| Catalog | [catalog-try-on.md](catalog-try-on.md#catalog) | `/catalog` | 2 |
| Try-On | [catalog-try-on.md](catalog-try-on.md#try-on) | `/try-on` | 2 |

## Shared layout

```text
Phone (≤ 640 px)                      Desktop (≥ 1024 px)
┌───────────────────────────┐         ┌──────────────────────────────────────────────────────┐
│ ☰  Fitting Room     [👤]  │         │ Fitting Room   Catalog  Try-On  My Model     [👤 ▾]   │
├───────────────────────────┤         ├──────────────────────────────────────────────────────┤
│                           │         │                                                      │
│        page content       │         │                    page content                      │
│                           │         │                                                      │
└───────────────────────────┘         └──────────────────────────────────────────────────────┘
```

- The account menu (👤) has: Account, Export my data, Delete my data, Sign out.
- The Capture screen runs **on the MacBook**, full-screen (no nav bar), with text large enough to read from ~3 m. Capture is not offered on phones.
- Phone layouts below are for **viewing only** (catalog, My Model, Try-On).

## Rules for all screens

- No controls to change the face or body (FR-08).
- Disclaimers use the exact short labels from [consent-v1.md](../consent-v1.md#short-labels-used-elsewhere-must-stay-consistent-with-this-text).
- Every async state has three versions: **loading**, **error** (with retry), and **empty**.
