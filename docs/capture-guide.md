# Capture Guide — MacBook Built-in Camera (v1.0)

> **Changed 20 Nov 2026:** capture now uses the **MacBook's built-in camera** in the browser. There is no phone and no helper. Earlier phone instructions (v0.2) are retired.
> Distances and counts are **proposals until the feasibility tests** ([feasibility-macbook-camera.md](feasibility-macbook-camera.md)) confirm them.

> 🔒 Only capture **consenting adults**, and only the account owner. Development sample captures go in `data/samples/` (git-ignored) and are never committed.

## 1. Room setup

| Item | Rule | Why |
|------|------|-----|
| **Laptop position** | On a table (~75 cm high), lid tilted so the person's whole body is centred on screen | The camera is fixed in the lid |
| **Distance** | Person stands on a floor marker about **2.5 m** from the laptop (exact value set by calibration) | Whole body must fit in a landscape frame |
| **Floor marker** | Tape an **X** on the floor | The person turns on the same spot for every view |
| **Background** | Plain wall behind the person, colour different from the clothes, nothing moving | Clean person mask |
| **Lighting** | Bright, even, soft light from the **front** (behind or beside the laptop). **No window behind the person.** | Small webcam sensors get noisy and auto-adjust in poor light |
| **Space** | ~1 m free around the marker | Arms out in A-pose while turning |

## 2. Mac settings (before opening the capture page)

- **Control Center → Video Effects: turn OFF** Center Stage, Portrait, Studio Light, Reactions, and any background effect. These change the framing or your real appearance.
- Close other apps using the camera (FaceTime, Zoom, Photo Booth…).
- Use the latest **Chrome** or **Safari**. Allow camera access when asked, and also in System Settings → Privacy & Security → Camera if needed.
- Plug in power. Keep the laptop still during the whole capture.

## 3. Clothing, hair, accessories

- Fitted clothes in a solid, matte colour. No logos, stripes, shiny or very loose fabric.
- Hair tied back off the neck and shoulders.
- Remove glasses, hats, bags, watches.

## 4. Pose

- **A-pose:** stand straight, arms out about **30°** from the body, palms facing the thighs.
- Feet shoulder-width apart, centred on the **X**.
- Keep the **same arm angle** in every view.
- **Turn on the spot** with small steps. Don't walk off the marker.
- When the screen says **HOLD**, stay completely still for about 1 second.

## 5. Capture sequence

1. **Calibration.** Stand on the X. The app checks that head to feet fit, the distance, and the brightness.
2. **Body views (8).** Face the camera, then turn **45°** to your left after each capture, until you are facing the camera again:
   front → front-right → right → back-right → back → back-left → left → front-left
   The app captures automatically when you are in the right direction and still. You'll hear and see the next instruction.
3. **Face close-ups (5).** Come closer (about **70 cm**, sitting is fine): front, turn slightly left (45°), slightly right (45°), left profile (90°), right profile (90°). Neutral face, mouth closed.
4. **Review.** Check the thumbnails, retake any view, then upload.

**Total:** 8 body views + 5 face close-ups = **13 images** (min 11, max 30 including retakes).

## 6. Quick self-check

- [ ] Video effects are off (no automatic zoom or blur)
- [ ] Head and feet visible in all 8 body views
- [ ] Same spot and same arm angle in every view
- [ ] Face sharp in the close-ups
- [ ] No big brightness change between views

## 7. Development sample naming (experiments only)

```text
data/samples/<subject-code>/<YYYY-MM-DD>-macbook/
  body-front.jpg, body-front-right.jpg, …, face-front.jpg, …, settings.json
```

Use a **subject code** (S01, S02…), never a real name. Keep the consent record separate.
