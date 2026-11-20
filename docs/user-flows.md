# User Flows (v2 — MacBook camera, 20 Nov 2026)

Four core flows for the MVP. Screen names match the wireframes in [wireframes/](wireframes/README.md).

---

## Flow 1 — First visit: sign up → scan → see my model

```mermaid
flowchart TD
    A[Home] --> B[Sign up]
    B --> C[Consent screen]
    C -- Decline --> C1[Account kept, capture locked.<br/>Can browse catalog only]
    C -- Accept current version --> D[Capture: setup checklist<br/>incl. video effects off]
    D --> D2[Camera permission<br/>MacBook built-in camera]
    D2 --> E[Calibration on floor X<br/>+ A-pose guide]
    E --> F[8 body views, person turns 45° each<br/>auto-capture + voice cues]
    F --> F2[5 face close-ups at ~70 cm]
    F2 --> G[Review thumbnails / retake any]
    G --> H[Upload with progress]
    H --> I{Quality checks}
    I -- Rejected --> R[Flow 4: retake guidance]
    I -- Accepted --> J[My Model: processing %]
    J --> K{Reconstruction job}
    K -- Failed --> R
    K -- Ready --> L[My Model: 360° preview + limitations notice]
    L --> M[Try-On]
```

| # | Step | Screen | System does |
|---|------|--------|-------------|
| 1 | Taps **Get started** | Home | — |
| 2 | Enters email + password | Sign up | Creates account (password hashed) |
| 3 | Reads and accepts consent | Consent | Stores consent record (current version) with time |
| 4 | Confirms setup checklist (light, clothes, floor X, **video effects off**) | Capture | — |
| 5 | Allows camera access | Capture | Opens the MacBook built-in camera (`getUserMedia`) |
| 6 | Stands on the X; calibration turns green | Capture | Checks full body, single person, brightness; stores person height |
| 7 | Turns 45° at a time for 8 body views | Capture | Live pose/orientation; auto-captures when still; voice cues |
| 8 | Comes closer for 5 face close-ups | Capture | Face-size guide |
| 9 | Reviews thumbnails, retakes bad ones; clicks **Upload** | Capture | Encrypted upload to localhost; metadata removed; **camera stops** |
| 10 | Waits | My Model | Quality + consistency checks, then queues reconstruction job |
| 11 | Sees progress (%) — may leave and come back | My Model | Job runs (may take minutes) |
| 12 | Rotates finished model 360° | My Model | Streams private GLB |
| 13 | Clicks **Try on clothes** | Try-On | — |

## Flow 2 — Return visit: try on outfits

```mermaid
flowchart LR
    A[Sign in] --> B{Has ready model?}
    B -- No --> C[My Model: start capture]
    B -- Yes --> D[Try-On with last outfit]
    D --> E[Pick shirt] --> F[Viewer swaps top only]
    D --> G[Pick pants] --> H[Viewer swaps bottom only]
    F & H --> I[Rotate 360° / zoom]
    I --> J[Outfit auto-saved]
```

| # | Step | System does |
|---|------|-------------|
| 1 | Signs in | Session cookie |
| 2 | Lands on Try-On | Loads saved model + last outfit (no rescan) |
| 3 | Picks a shirt | Loads only the shirt GLB; body and pants stay |
| 4 | Picks pants | Loads only the pants GLB |
| 5 | Rotates / zooms | Client-side only |
| 6 | Leaves | Outfit saved |

## Flow 3 — Delete my profile

```mermaid
flowchart TD
    A[Account / My Model] --> B[Delete my data]
    B --> C[Explain what is deleted<br/>+ backup purge within 30 days]
    C --> D[Type DELETE to confirm]
    D --> E[Delete account, model, captures, outfits]
    E --> F[Signed out + confirmation screen]
```

Options on this screen:
- **Delete my 3D model only.** Keeps the account and lets the user rescan later.
- **Delete my account and all data.** Deletes everything.
- **Export my data first** (a link to the export).

## Flow 4 — Capture rejected → retake

```mermaid
flowchart TD
    A[Quality checks fail] --> B[Result screen: list of problems]
    B --> C{Problem type}
    C -- Blurry / wrong direction / face too small --> D[Retake only those views]
    C -- Too dark / backlit --> E[Show lighting tips → restart]
    C -- Missing view / moved off X / pose changed --> F[Retake those views]
    C -- Framing changed (Center Stage) / 2 people --> G[Fix setup → restart whole capture]
    D & E & F & G --> H[Upload again]
```

Rules:
- Each problem is shown in plain words with a fix, e.g. *"The right view shows the wrong direction. Retake it and follow the turn diagram."* (codes in [capture-steps.md](capture-steps.md))
- If only a few photos are bad, retake just those. If the problem affects the whole set, restart.
- After **3 failed attempts**, show the full capture guide and suggest a better place or time.
