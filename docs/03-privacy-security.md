# 3. Privacy & Security

Face and body scans are **sensitive personal data**. In many jurisdictions, face data used to identify someone can count as biometric data. The plan requires these controls **from the first prototype**, not only in Phase 7.

> Check which privacy laws apply where you launch (for example GDPR in the EU or local data-protection law) before the pilot. This document is an engineering checklist, not legal advice.

## 3.1 Consent

- [ ] Show a consent screen **before** the camera opens.
- [ ] Explain in plain language: what is captured, why, where it is stored, how long (until the customer deletes it), and how to delete it.
- [ ] Store a consent record with a **version number**. If the text changes, ask again.
- [ ] Withdrawing consent means the user's data gets deleted.
- [ ] Capture only **adults**, and only with their own consent. Test data must come from consenting adults or properly licensed sample data.

## 3.2 Data minimization

- [ ] Keep raw photos/videos only as long as reconstruction needs them. Delete them after the model is approved, unless the user opts in to keep them.
- [ ] Strip EXIF metadata (GPS location, device info) on upload.
- [ ] Don't log images, file contents, or personal details.

## 3.3 Encryption & storage

- [ ] Encrypt every customer file at rest (e.g. AES-GCM via Python `cryptography`) under `data/`, which is git-ignored.
- [ ] Keep encryption keys out of Git (in `.env`/keychain; later a secrets manager).
- [ ] Never place customer files in `static/` or any public URL.
- [ ] Use HTTPS for every upload, including phone → MacBook on the local network.

## 3.4 Access control

- [ ] Every model/capture endpoint checks `resource.user_id == current_user.id`.
- [ ] Use opaque random IDs (UUIDv4), never sequential IDs, in URLs.
- [ ] Session cookies must be `HttpOnly`, `Secure`, `SameSite=Lax`.
- [ ] Rate-limit login and uploads.
- [ ] Write an audit log for model access, export and deletion.

## 3.5 Upload safety

- [ ] Enforce a max file size and file count per session.
- [ ] Allow only these types: `image/jpeg`, `image/png`, `image/heic`, `video/mp4`, `video/quicktime`. Check the real file signature too, not just the extension.
- [ ] Re-encode images server-side before processing.

## 3.6 Deletion

- [ ] `DELETE /me` removes the account, consents, captures, models and outfits from primary storage at once.
- [ ] Backups: write down how long backups are kept (e.g. 30 days) and how deleted users get purged from them, and tell users this.
- [ ] Deleting a user also deletes their encryption key, if you use per-user keys (crypto-shredding).
- [ ] Add a test that proves no files remain after deletion.

## 3.7 Honest disclosure (product requirement)

- [ ] Label the try-on as a **visual preview**, not an accurate size or fit.
- [ ] Explain model fidelity limits (hair, loose clothing, hidden areas).
- [ ] Don't show any size claim until a validated size feature exists.
