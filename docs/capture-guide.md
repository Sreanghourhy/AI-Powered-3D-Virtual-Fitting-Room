# Photo Capture Guide (draft v0.1)

How to capture a person with a phone so the 3D reconstruction has the best chance of working. These steps become the on-screen instructions in Phase 1 (P1-04) and Phase 3.

> 🔒 Only capture **consenting adults**. Record written consent before capturing. Store captures in `data/samples/` (git-ignored) and never commit them.

## 1. Before you start

| Item | Rule | Why |
|------|------|-----|
| **Lighting** | Bright, even, indirect light (e.g. cloudy daylight, or 2+ soft lamps from the front-left and front-right). No strong window behind the person. | Shadows and backlight break texture and shape. |
| **Background** | Plain wall or uncluttered room, colour different from the clothes. | Makes it easier to separate the person from the background. |
| **Clothing** | Fitted clothes in a solid, matte colour. No logos, stripes, shiny or very loose fabric. No black-on-black. | Loose clothing hides the body shape. Patterns and shine confuse matching. |
| **Hair & accessories** | Hair tied back off the neck and shoulders. Remove glasses, hats, bags, watches. | Hair and reflective objects reconstruct badly. |
| **Space** | About 2.5 m clear around the person. | The photographer needs room to walk around. |

## 2. Pose (the person being scanned)

- **A-pose:** stand straight, arms out about **30°** from the body, palms facing the thighs, fingers together.
- Feet about **shoulder-width** apart, toes forward.
- Neutral face, mouth closed, eyes looking straight ahead at a fixed point.
- **Do not move** during the capture: no breathing deeply, no turning the head. Movement is the most common cause of failure.

## 3. Phone settings

- Rear camera, **1080p or higher** (4K video if possible). No portrait/beauty mode, no filters.
- **Lock focus and exposure** (iPhone: long-press on the person → AE/AF Lock).
- Turn off HDR/Live Photo if possible, and turn off flash.
- Clean the lens.

## 4. Capture method A — photos (recommended for first tests)

1. Stand **about 1.5–2 m** away, so the **whole body fits in the frame with a small margin** above the head and below the feet.
2. **Ring 1 (chest height):** walk in a full circle around the person and take a photo **every ~15–20°**, about **20–24 photos**.
3. **Ring 2 (higher, phone above head, tilted down):** another full circle, about **12–16 photos**.
4. **Ring 3 (knee height, tilted up):** another full circle, about **12–16 photos**.
5. **Face close-ups:** about 6 photos from front, front-left, left, front-right, right, and slightly below.
6. Each photo must **overlap ~60–70%** with the previous one. Move the phone, never ask the person to turn.

**Total:** about 50–60 photos.

## 5. Capture method B — video

- One slow orbit at chest height, a second at head height, and a third at knee height. Each orbit takes about **30–40 s**.
- Keep a steady speed, without fast turns or shaking.
- Frames are extracted later (Phase 3, P3-07).

## 6. Quick self-check before ending the session

- [ ] Front, left, back and right of the person are all covered
- [ ] Top of the head and the feet are visible in every photo
- [ ] Photos are sharp when you zoom in on the face
- [ ] No large shadows on one side of the body
- [ ] Person didn't move between the first and last photo

## 7. File naming

```text
data/samples/<subject-code>/<YYYY-MM-DD>-<method>/IMG_0001.jpg
e.g. data/samples/S01/2026-11-21-photos/
```

Use a **subject code** (S01, S02…), never a real name. Keep the consent record separate from the images.

## 8. Notes to record per session

Lighting setup, phone model, number of photos, time taken, anything that went wrong. Record these in `docs/experiments/`.
