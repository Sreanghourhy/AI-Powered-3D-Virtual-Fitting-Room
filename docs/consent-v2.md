# Consent Text — v2 (MacBook camera)

> **Version:** `consent-v2` · **Status:** Draft, **waiting for owner approval** · **Date:** 20 Nov 2026
> **Replaces:** [consent-v1](consent-v1.md) (phone + helper wording).
> **What changed from v1:** the camera is the MacBook's built-in camera; the views are front, sides, back and face close-ups; no helper. Everything else is unchanged.
> Engineering draft, not legal advice.

---

## On-screen text (shown before the camera opens)

### Before we scan you

We will use your **MacBook's built-in camera** to take photos of you from the **front, sides and back**, plus a few **close-ups of your face**. Our system turns these photos into a **3D model of you** so you can try on clothes.

**What we collect**
- Photos of your face and whole body, from several angles
- The 3D model we build from them
- The clothes you choose to try on

**Why**
Only to show you a 3D try-on preview. We don't use your photos or model for advertising, sell them, or use them to train AI without asking you separately.

**How we protect it**
- The camera is only on during the capture steps and turns off when you finish or leave the page.
- Nothing is uploaded until you press **Upload**.
- Your photos and model are **encrypted** and stored privately.
- **Only you** can see your model after signing in.
- We remove hidden data (metadata) from your photos.
- We **delete your original photos** once your model is ready. We keep only the 3D model.

**How long we keep it**
Until **you delete it**. You can delete your 3D model, or your whole account, at any time from *My Model* or *Account*. Deleted data is removed right away from our main storage and **within 30 days from backups**.

**Your choices**
- You can view, download (export), or delete your model at any time.
- You can withdraw this consent at any time. We will then delete your scan data.

**Important to know**
- The 3D model is an **approximation**. Hair, loose clothing and hidden areas may not look exactly like you.
- We do **not** change your face or body shape, and we do not replace you with a generic avatar.
- The try-on is a **visual preview only**. It does **not** tell you your exact size or how the clothes will really fit.

**Who can be scanned**
You must be **18 or older**, and you may scan **only yourself**, standing in front of your MacBook camera.

---

☐ **I am 18 or older and I am the person being scanned.**
☐ **I agree to the capture and storage of my photos and 3D model as described above.**

[ Decline ]   [ **Agree and continue** ]

*Declining keeps your account. You can still browse the catalog and scan later.*

---

## Implementation notes (applied in task P3-00 after approval)

| Field | Value |
|-------|-------|
| `consents.version` | `"consent-v2"` |
| Backend setting | `FR_CONSENT_VERSION` default `consent-v2` |
| Existing `consent-v1` users | Must accept v2 before capture (re-consent banner already exists) |
| Short labels (My Model, Try-On, Delete) | **Unchanged** from v1 |
