# Wireframe — Fitting Room (`/`, main interface) · CR-02

The app opens here. No login, account menu or profile selection.

## States

```text
 1. No scan yet                                   2. Generating
┌───────────────────────────────────┬──────────────┐ ┌───────────────────────────────────┬──────────────┐
│ Fitting Room                       Catalog        │ │ Fitting Room                       Catalog        │
├───────────────────────────────────┼──────────────┤ ├───────────────────────────────────┼──────────────┤
│                                   │ Shirt        │ │                                   │ Shirt        │
│         (empty stage,             │ [∅][👕][👕]  │ │   Building your 3D model…         │ [∅][👕][👕]  │
│          no body shown)           │              │ │   ███████░░░░░░  48%              │              │
│                                   │ Pants        │ │   Step: fitting body shape        │ Pants        │
│   No scan yet.                    │ [∅][👖][👖]  │ │                                   │ [∅][👖][👖]  │
│   [  Start Scan  ]                │              │ │   This can take several minutes.  │              │
│   ~4 min · MacBook camera         │ (pickers can │ │                                   │              │
│                                   │  be browsed) │ │                                   │ [Discard…]   │
└───────────────────────────────────┴──────────────┘ └───────────────────────────────────┴──────────────┘
```

```text
 3. Ready (main state)
┌──────────────────────────────────────────────────┬───────────────────────┐
│ Fitting Room                          Catalog     │                       │
├──────────────────────────────────────────────────┼───────────────────────┤
│ ⓘ Visual preview only — not a size or fit        │  Shirt                │
│   guarantee.                                     │  ┌────┐┌────┐┌────┐   │
│                                                  │  │ ∅  ││ 👕 ││ 👕 │   │
│              🧍 (my model) + 👕 + 👖               │  └────┘└────┘└────┘   │
│                                                  │  Basic Tee — White    │
│                                                  │                       │
│                                                  │  Pants                │
│   ⟲ reset   ▶ auto-rotate   📷                    │  ┌────┐┌────┐┌────┐   │
│                                                  │  │ ∅  ││ 👖 ││ 👖 │   │
│ ⓘ This 3D model is an approximation of you…      │  └────┘└────┘└────┘   │
│                                                  │                       │
│                                                  │  [ Rescan ]           │
│                                                  │  Discard scan & model │  ← red link → confirm
└──────────────────────────────────────────────────┴───────────────────────┘
```

```text
 4. Reconstruction failed (NO avatar shown)
┌───────────────────────────────────┬──────────────┐
│   ✕ We couldn't build a reliable  │ Shirt / Pants│
│     3D model from this scan.      │ (disabled)   │
│   Reason: back views didn't match │              │
│   the front (you moved off the X).│              │
│   [ Try again ]  [ Rescan ]       │              │
│   [ View capture guide ]          │ [Discard…]   │
└───────────────────────────────────┴──────────────┘
```

**Discard confirm dialog:** "Delete your scan photos, 3D model and outfit from this MacBook? This can't be undone." [Cancel] [Delete]

**Header:** app name + "Catalog" link only. No account or profile menu.
