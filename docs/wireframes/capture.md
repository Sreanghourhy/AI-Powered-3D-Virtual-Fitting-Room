# Wireframe — Capture (`/capture`) · MacBook camera

> **Changed 20 Nov 2026:** replaces the phone wireframe. Landscape laptop screen, full-screen mode, text readable from ~3 m. Step text from [capture-steps.md](../capture-steps.md).

## A. Setup checklist (Step 0)

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ✕ Exit                                                    Step 0 / 6 │
│                                                                      │
│   Get ready (1 minute)                    ┌────────────────────────┐ │
│                                           │   laptop    ·····  X   │ │
│   ☐ Laptop on a table, still              │   [▭]  ← ~2.5 m →  🧍  │ │
│   ☐ Bright light in front of you,         │  (setup diagram, top   │ │
│     no window behind you                  │   and side view)       │ │
│   ☐ Fitted plain clothes, hair tied back  └────────────────────────┘ │
│   ☐ Video effects OFF                                                │
│     (Control Center → Video Effects →                                │
│      Center Stage, Portrait, Studio Light)                           │
│   ☐ Tape an X on the floor ~2.5 m away                               │
│                                                                      │
│                                          [ View full guide ]         │
│                                          [     Start camera      ]   │  ← enabled when all ticked
└──────────────────────────────────────────────────────────────────────┘
```

## B. Calibration (Step 2) and body views (Step 4)

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ✕   BODY VIEW 3 of 8          ●●◉○○○○○                  🔊 on   ⌨ Space │  ← progress dots; voice toggle
├──────────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────┐  ┌──────────────┐ │
│ │            live camera preview (mirrored)      │  │   TURN       │ │
│ │                                                │  │    ↑ screen  │ │
│ │                     ╭─╮                        │  │  ◜     ◝     │ │  ← top-down turn
│ │                    ╱│ │╲                       │  │ ◉   🧍   ○   │ │    diagram: done ●,
│ │                   ╱ │ │ ╲    body outline      │  │  ◟     ◞     │ │    current ◉, todo ○
│ │                     │ │      (green = OK)      │  │      ○       │ │
│ │                    ╱   ╲                       │  └──────────────┘ │
│ │                                                │                   │
│ │  ⚠ Step back a little                          │                   │  ← live hint
│ └────────────────────────────────────────────────┘                   │
│                                                                      │
│        TURN TO YOUR RIGHT SIDE  →   HOLD STILL   ● 1                 │  ← very large text (≥ 48 px)
└──────────────────────────────────────────────────────────────────────┘
```

- Auto-capture: orientation OK + still ≥ 1 s → "HOLD STILL" → 1 s countdown → beep → ✓
- Fallback: **Space** key or click **Capture**.
- Voice reads each instruction (can be muted).

## C. Face close-ups (Step 5)

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ✕   FACE 2 of 5               ●◉○○○                                  │
│ ┌────────────────────────────────────────────────┐                   │
│ │                 ╭───────╮                      │   Come closer     │
│ │                 │  face │  oval guide          │   (about 70 cm).  │
│ │                 │ outline│                     │   Turn your head  │
│ │                 ╰───────╯                      │   a little LEFT.  │
│ └────────────────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────┘
```

## D. Review → Upload → Result (Steps 6–8)

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ←  Check your photos                                         13 / 13 │
│                                                                      │
│  Body   [▣ front][▣ fr-right][⚠ right][▣ bk-right][▣ back]           │  ← ⚠ = flagged
│         [▣ bk-left][▣ left][▣ fr-left]                               │
│  Face   [▣ front][▣ left 45][▣ right 45][▣ left 90][▣ right 90]      │
│                                                                      │
│  Click a photo to retake it.                       [   Upload   ]    │
└──────────────────────────────────────────────────────────────────────┘

 Uploading 9 of 13 ████████████░░░░ 69%        ✕ A few retakes needed
 Keep this page open.                           • Right view: wrong direction [Retake]
                                                • Face too small in close-up 1 [Retake]
                                                [ Retake these ]  [ Start over ]
```

**Other states:**
- Camera permission denied (browser and macOS settings help)
- No camera found
- Camera in use by another app
- Unsupported browser
- Upload failed, with "Retry"

**Privacy:** the camera stops when you leave the page or finish. Nothing is uploaded until you press **Upload**.
