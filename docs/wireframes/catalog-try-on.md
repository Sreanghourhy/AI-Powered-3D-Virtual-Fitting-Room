# Wireframes — Catalog & Try-On · P1-09

## Catalog

### Phone (`/catalog`)

```text
┌───────────────────────────────┐
│ ☰  Fitting Room         [👤]  │
├───────────────────────────────┤
│  Catalog                      │
│  [ Shirts ]  Pants            │  ← tabs (category top / bottom)
│                               │
│  ┌───────────┐ ┌───────────┐  │
│  │  thumb    │ │  thumb    │  │
│  │           │ │           │  │
│  ├───────────┤ ├───────────┤  │
│  │Basic Tee  │ │Oxford     │  │
│  │White      │ │Blue       │  │
│  │[Try on →] │ │[Try on →] │  │
│  └───────────┘ └───────────┘  │
│  ┌───────────┐ ┌───────────┐  │
│  │  …        │ │  …        │  │
└───────────────────────────────┘
```

### Desktop

```text
┌──────────────────────────────────────────────────────────────────┐
│ Fitting Room   [Catalog]  Try-On  My Model                [👤 ▾] │
├──────────────────────────────────────────────────────────────────┤
│  Catalog        [ Shirts ]  Pants                                │
│                                                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                  │
│  │ thumb  │  │ thumb  │  │ thumb  │  │ thumb  │                  │
│  │ name   │  │ name   │  │ name   │  │ name   │                  │
│  │[Try on]│  │[Try on]│  │[Try on]│  │[Try on]│                  │
│  └────────┘  └────────┘  └────────┘  └────────┘                  │
└──────────────────────────────────────────────────────────────────┘
```

- **Try on →** opens `/try-on?top=<id>` or `/try-on?bottom=<id>`.
- Logged-out users can browse. "Try on" asks them to sign in.
- Users without a ready model see "Scan yourself first → Start capture".

---

## Try-On

### Phone (`/try-on`)

```text
┌───────────────────────────────┐
│ ☰  Fitting Room         [👤]  │
├───────────────────────────────┤
│ ┌───────────────────────────┐ │
│ │ ⓘ Visual preview only —   │ │  ← always visible
│ │   not a size guarantee.   │ │
│ │                           │ │
│ │        🧍 + 👕 + 👖        │ │  ← 3D viewer (≈ 60% height)
│ │                           │ │
│ │  ⟲ reset   ▶ rotate  📷   │ │  ← 📷 = save screenshot (Could)
│ └───────────────────────────┘ │
│                               │
│  Shirt                    ⌄   │
│  ◀ [∅][👕][👕][👕][👕] ▶      │  ← horizontal scroller; ∅ = none
│                               │
│  Pants                    ⌄   │
│  ◀ [∅][👖][👖][👖] ▶          │  ← independent from shirt row
└───────────────────────────────┘
```

### Desktop

```text
┌──────────────────────────────────────────────────────────────────┐
│ Fitting Room   Catalog  [Try-On]  My Model                [👤 ▾] │
├──────────────────────────────────────────┬───────────────────────┤
│ ⓘ Visual preview only — not a size       │  Shirt                │
│   guarantee.                             │  ┌────┐┌────┐┌────┐   │
│                                          │  │ ∅  ││ 👕 ││ 👕 │   │
│               🧍 + 👕 + 👖                │  └────┘└────┘└────┘   │
│                                          │  selected: Basic Tee  │
│                                          │                       │
│                                          │  Pants                │
│                                          │  ┌────┐┌────┐┌────┐   │
│                                          │  │ ∅  ││ 👖 ││ 👖 │   │
│   ⟲ reset    ▶ auto-rotate    📷         │  └────┘└────┘└────┘   │
│                                          │  selected: Chinos     │
└──────────────────────────────────────────┴───────────────────────┘
```

### Behaviour

| Action | Result |
|--------|--------|
| Select shirt | Only the top slot changes; body + pants untouched (FR-04) |
| Select pants | Only the bottom slot changes |
| Select ∅ | Removes that garment |
| Garment loading | Small spinner on that thumbnail; old garment stays until new one is ready |
| Garment load error | Toast "Couldn't load this item. Try again."; previous garment stays |
| Leave page | Outfit saved (FR-13) |
| No ready model | Redirect to My Model with "Scan yourself first" |
