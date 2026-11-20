# 3. Privacy & Data Handling (v3, CR-02 — single user, local only)

Face and body images are sensitive, even in a personal prototype. Everything stays **on this MacBook**.

## 3.1 Privacy notice (replaces consent records)

- [ ] Show the short [privacy notice](privacy-notice.md) the first time **Start Scan** is clicked, before the camera starts. "Don't show again" is stored in the browser only.
- [ ] Scan **only yourself**.

## 3.2 Camera

- [ ] Request the camera only on `/scan`, after the privacy notice.
- [ ] Stop all camera tracks when the scan finishes, is cancelled, or the page is left. The camera light must turn off.
- [ ] Turn **off** macOS video effects (Center Stage, Portrait, Studio Light, backgrounds). They change framing and real appearance.
- [ ] No third-party network requests while the camera is on. MediaPipe models and WASM are served from this app.

## 3.3 Data minimisation and lifetime

- [ ] Captured images stay **in browser memory** until **Generate 3D Model** is clicked (no localStorage / IndexedDB for images).
- [ ] Uploaded images are re-encoded server-side with **all metadata removed**.
- [ ] One current scan and model only. A new scan replaces the old one once the new model is ready, and old files are deleted.
- [ ] Images and model are kept locally until **Discard scan & model** (local persistence, D11).
- [ ] Logs never contain images, file contents or file paths of personal data.

## 3.4 Storage and encryption

- [ ] Every image and model is encrypted at rest (AES-256-GCM) under `data/`, which is git-ignored.
- [ ] The encryption key lives in `backend/.env` (git-ignored). Losing it makes stored files unreadable.
- [ ] Scan images and models are never placed in `static/` or any public URL.
- [ ] No cloud storage. If the Mac is backed up (e.g. Time Machine), `data/` is backed up **encrypted**. Discard + a new backup removes it over time.

## 3.5 Localhost protection (no authentication, so the server itself must be locked down)

- [ ] The backend listens on **127.0.0.1 only** (never `0.0.0.0`).
- [ ] Requests with a `Host` other than `localhost` / `127.0.0.1` (with port) are rejected. This blocks DNS-rebinding attacks.
- [ ] State-changing requests (`POST`/`PUT`/`DELETE`) need the header `X-Fitting-Room: 1`. **No CORS**, so other websites can't send it.
- [ ] The Vite dev server keeps its default host checks; don't expose it with `--host` on a network.
- [ ] Any future non-localhost deployment needs HTTPS **and** authentication again. That is out of scope (CR-02).

## 3.6 Upload safety

- [ ] JPEG/PNG only, checked by file signature, ≤ 8 MB per image, ≤ 30 images, ≤ 150 MB per scan.
- [ ] Images are re-encoded before processing.

## 3.7 Discard

- [ ] **Discard scan & model** (`DELETE /data`) removes scans, images, models, jobs, outfit and **all their encrypted files** in one step, with a confirmation.
- [ ] A test proves no blobs and no rows remain afterwards.

## 3.8 Honest disclosure

- [ ] Label the try-on as a **visual preview**, not size or fit.
- [ ] Show the model's known limits (hair, hands, loose clothing, hidden areas).
- [ ] If reconstruction fails, say so with the reasons. **Never** show a generic avatar in place of the person.
