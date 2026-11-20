# Consent Text — v1

> ⚠️ **Superseded** by [consent-v2](consent-v2.md) (MacBook camera) (approved 20 Nov 2026). Kept for the record because some accounts may have accepted v1.
>
> **Version:** `consent-v1` · **Status:** Approved 20 Nov 2026, superseded · **Date:** 20 Nov 2026
> Engineering draft only, not legal advice. Have it reviewed for the countries where you launch before real customers use it.
> If any wording changes, create `consent-v2` and ask existing users to accept again.

---

## On-screen text (shown before the camera opens)

### Before we scan you

We will use your phone camera to take photos of you from all sides. Our system turns these photos into a **3D model of you** so you can try on clothes.

**What we collect**
- Photos of your face and whole body, from many angles
- The 3D model we build from them
- The clothes you choose to try on

**Why**
Only to show you a 3D try-on preview. We don't use your photos or model for advertising, sell them, or use them to train AI without asking you separately.

**How we protect it**
- Your photos and model are **encrypted** and stored privately.
- **Only you** can see your model after signing in.
- We remove location and device data from your photos.
- We **delete your original photos** once your model is ready. We keep only the 3D model.

**How long we keep it**
Until **you delete it**. You can delete your 3D model, or your whole account, at any time from *My Model* or *Account*. Deleted data is removed right away from our main storage and **within 30 days from backups**.

**Your choices**
- You can view, download (export), or delete your model at any time.
- You can withdraw this consent at any time. We will then delete your scan data.

**Important to know**
- The 3D model is an **approximation**. Hair, loose clothing and hidden areas may not look exactly like you.
- The try-on is a **visual preview only**. It does **not** tell you your exact size or how the clothes will really fit.

**Who can be scanned**
You must be **18 or older**, and you may scan **only yourself**. A helper can hold the phone, but the person scanned must be the account owner.

---

☐ **I am 18 or older and I am the person being scanned.**
☐ **I agree to the capture and storage of my photos and 3D model as described above.**

[ Decline ]   [ **Agree and continue** ]

*Declining keeps your account. You can still browse the catalog and scan later.*

---

## Implementation notes

| Field | Value |
|-------|-------|
| `consents.version` | `"consent-v1"` |
| `consents.scope` | `"capture_and_store_body_model"` |
| Both checkboxes required | Yes. The "Agree" button stays disabled until both are ticked |
| Store | user id, version, scope, `granted_at` (UTC) |
| Withdraw | sets `withdrawn_at` and triggers deletion of captures and models |
| Re-consent | if the latest version > the user's accepted version, show the screen again before capture |

### Short labels used elsewhere (must stay consistent with this text)

- My Model: *"This 3D model is an approximation of you. Hair, loose clothing and hidden areas may differ."*
- Try-On: *"Visual preview only — not a size or fit guarantee."*
- Delete dialog: *"Removed now from our storage and within 30 days from backups."*
