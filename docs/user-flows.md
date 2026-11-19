# User Flows (v1)

Four core flows for the MVP. Screen names match the wireframes in [wireframes/](wireframes/README.md).

---

## Flow 1 — First visit: sign up → scan → see my model

```mermaid
flowchart TD
    A[Home] --> B[Sign up]
    B --> C[Consent screen]
    C -- Decline --> C1[Account kept, capture locked.<br/>Can browse catalog only]
    C -- Accept v1 --> D[Capture: setup checklist]
    D --> E[Capture: pose guide]
    E --> F[Capture: guided photos<br/>3 rings × 12 positions + face]
    F --> G[Review thumbnails / retake any]
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
| 3 | Reads and accepts consent | Consent | Stores consent record `v1` with time |
| 4 | Confirms setup checklist (light, clothes, helper present) | Capture | — |
| 5 | Person stands in A-pose; helper follows on-screen positions | Capture | Live brightness hint |
| 6 | Reviews thumbnails, retakes bad ones | Capture | — |
| 7 | Taps **Upload** | Capture | Encrypted upload, strips EXIF |
| 8 | Waits | My Model | Quality checks, then queues reconstruction job |
| 9 | Sees progress (%) — may leave and come back | My Model | Job runs (may take minutes) |
| 10 | Rotates finished model | My Model | Streams private GLB |
| 11 | Taps **Try on clothes** | Try-On | — |

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
    C -- Blurry photos 7, 12 --> D[Retake only those positions]
    C -- Too dark / backlit --> E[Show lighting tips → restart]
    C -- Missing back view --> F[Retake back positions]
    C -- Person moved / 2 people --> G[Restart whole capture]
    D & E & F & G --> H[Upload again]
```

Rules:
- Each problem is shown in plain words with a fix, e.g. *"Photo 7 is blurry. Hold the phone still and tap to focus."*
- If only a few photos are bad, retake just those. If the problem affects the whole set, restart.
- After **3 failed attempts**, show the full capture guide and suggest a better place or time.
