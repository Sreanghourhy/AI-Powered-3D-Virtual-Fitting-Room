# Wireframe — My Model (`/my-model`) · P1-08

## States

```text
 1. No model yet                    2. Processing                     3. Failed
┌───────────────────────────┐     ┌───────────────────────────┐     ┌───────────────────────────┐
│  My 3D model              │     │  My 3D model              │     │  My 3D model              │
│                           │     │                           │     │                           │
│   ┌───────────────────┐   │     │  Building your model…     │     │  ✕ We couldn't build your │
│   │      🧍 (grey)    │   │     │  ███████░░░░░░  48%       │     │    model.                 │
│   └───────────────────┘   │     │  Step: reconstructing     │     │  Reason: not enough back  │
│  You haven't been scanned │     │                           │     │  views were matched.      │
│  yet. It takes about 4    │     │  This can take several    │     │                           │
│  minutes on your MacBook. │     │  minutes. You can leave — │     │  [ Rescan ]               │
│                           │     │  we keep working.         │     │  [ View capture guide ]   │
│  [ Start capture ]        │     │                           │     │                           │
└───────────────────────────┘     └───────────────────────────┘     └───────────────────────────┘
```

## 4. Ready — phone

```text
┌───────────────────────────────┐
│ ☰  Fitting Room         [👤]  │
├───────────────────────────────┤
│  My 3D model                  │
│ ┌───────────────────────────┐ │
│ │                           │ │
│ │          🧍 3D            │ │  ← drag rotate · pinch zoom
│ │                           │ │
│ │   ⟲ reset   ▶ auto-rotate │ │
│ └───────────────────────────┘ │
│  ⓘ This 3D model is an        │
│  approximation of you. Hair,  │
│  loose clothing and hidden    │
│  areas may differ.            │
│                               │
│  Scanned 20 Nov 2026          │
│                               │
│  [   Try on clothes   →    ]  │  ← primary
│  [ Rescan ]  [ Export ]       │
│  Delete my 3D model           │  ← red text link → Flow 3
└───────────────────────────────┘
```

## 4. Ready — desktop

```text
┌──────────────────────────────────────────────────────────────────┐
│ Fitting Room   Catalog  Try-On  [My Model]               [👤 ▾]  │
├──────────────────────────────────────────┬───────────────────────┤
│                                          │  My 3D model          │
│                                          │  Scanned 20 Nov 2026  │
│                 🧍 3D                     │                       │
│                                          │  ⓘ Approximation…     │
│                                          │                       │
│        ⟲ reset    ▶ auto-rotate          │  [ Try on clothes → ] │
│                                          │  [ Rescan ] [ Export ]│
│                                          │  Delete my 3D model   │
└──────────────────────────────────────────┴───────────────────────┘
```

**Not on this screen (FR-08):** no sliders for height, weight, face, or body shape.

## Delete dialog (Flow 3)

```text
┌───────────────────────────────┐
│  Delete your data?            │
│                               │
│  ◉ Delete my 3D model only    │
│  ○ Delete my account and all  │
│    data                       │
│                               │
│  Removed now from our storage │
│  and within 30 days from      │
│  backups. This can't be undone│
│                               │
│  Export my data first →       │
│                               │
│  Type DELETE: [__________]    │
│  [ Cancel ]   [ Delete ]      │  ← red, enabled after typing
└───────────────────────────────┘
```
