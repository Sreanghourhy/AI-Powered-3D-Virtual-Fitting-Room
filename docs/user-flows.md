# User Flows (v3 — single user, MacBook camera, CR-02)

One user (the owner), one MacBook. No login, accounts or profiles. Screens match [wireframes/](wireframes/README.md).

---

## Flow 1 — Scan and generate my 3D model

```mermaid
flowchart TD
    A[Open app → Fitting room /] --> B[Click Start Scan]
    B --> N{First time?}
    N -- yes --> P[Privacy notice → Start camera]
    N -- no --> C
    P --> C[Camera access: MacBook built-in camera]
    C -- denied --> X[Help: browser + macOS camera settings]
    C --> D[Setup checklist: light, floor X, video effects off]
    D --> E[Calibration on the X: full body, one person, brightness]
    E --> F[8 body views, turning 45° each; auto-capture + voice cues]
    F --> G[5 face close-ups at ~70 cm]
    G --> H[Review → retake any view]
    H --> I[Click Generate 3D Model]
    I --> J[Upload to localhost + camera stops]
    J --> K{Quality + consistency checks}
    K -- fail --> R[Flow 3: retake the listed views]
    K -- pass --> L[Fitting room: progress %]
    L --> M{Reconstruction}
    M -- failed --> F2[Flow 3: failure + reasons, NO avatar]
    M -- ready --> V[My model in the 360° viewer]
```

| # | Step | System does |
|---|------|-------------|
| 1 | Opens `http://localhost:5173` | Shows the fitting room: "No scan yet" + **Start Scan** |
| 2 | Clicks **Start Scan** | First time: privacy notice |
| 3 | Allows camera | `getUserMedia` on the built-in camera |
| 4 | Ticks the setup checklist | — |
| 5 | Stands on the X; calibration turns green | MediaPipe pose + brightness; stores person height |
| 6 | Turns 45° at a time (8 views) | Auto-capture when orientation is right and still ≥ 1 s; voice cues |
| 7 | Comes closer for 5 face close-ups | Face-size guide |
| 8 | Reviews and retakes | Images kept in memory only |
| 9 | Clicks **Generate 3D Model** | Uploads to localhost (encrypted, metadata removed), **camera stops**, checks run |
| 10 | Back in the fitting room, sees progress | Reconstruction job runs (minutes) |
| 11 | Sees the model, rotates 360° | GLB streamed from localhost |

## Flow 2 — Try on shirts and pants

```mermaid
flowchart LR
    A[Fitting room with my model] --> B[Pick shirt] --> C[Only the shirt changes]
    A --> D[Pick pants] --> E[Only the pants change]
    C & E --> F[Rotate 360° / zoom]
    F --> G[Outfit remembered locally]
```

- Choosing a shirt never reloads the body or the pants, and choosing pants never changes the shirt.
- "None" removes that garment.
- Before a model exists, the pickers can be browsed but nothing is rendered on a body. **No sample or avatar body is shown in its place.**

## Flow 3 — Problems: retake or failed reconstruction

```mermaid
flowchart TD
    A{What failed?} -- quality check on some views --> B[List: view + reason + fix]
    B --> C[Retake only those views → Generate again]
    A -- setup problem: framing changed / 2 people / too dark --> D[Fix setup → rescan]
    A -- reconstruction failed --> E[Show failure reason + tips<br/>keep images until Discard]
    E --> F[Try Generate again / Rescan / Discard]
```

Rules:
- Every problem is shown in plain words with a fix (codes in [capture-steps.md](capture-steps.md)).
- A failed reconstruction **never** shows a generic avatar. The viewer stays empty with the reason.
- After 3 failed attempts, show the full capture guide.

## Flow 4 — Discard everything

```mermaid
flowchart LR
    A[Fitting room: Discard scan & model] --> B[Confirm: deletes photos, model and outfit from this MacBook]
    B --> C[DELETE /data] --> D[Fitting room back to 'No scan yet']
```
