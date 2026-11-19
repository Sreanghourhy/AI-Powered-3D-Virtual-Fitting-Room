# 1. Project Overview

## 1.1 Vision

Build a virtual clothing fitting system based on the **customer's own appearance**.

1. Capture the person **once** with phone photos/video from multiple angles.
2. Reconstruct an approximate 3D representation of that person.
3. Save it securely until the customer deletes it.
4. Let the customer try shirts and pants again and again in a **360° viewer**.

The app must **not** offer controls to change the customer's face or body proportions. It is the real person, not an avatar editor.

## 1.2 Users and main flows

| User | Main flow |
|------|-----------|
| Customer | Sign up → give consent → guided capture → wait for processing → review model → try on outfits → come back later → delete profile if wanted |
| Admin / developer | Manage garment catalog → review failed reconstructions → monitor jobs |

### Screens (from Phase 1 wireframes)

| Screen | Purpose |
|--------|---------|
| **Sign in / Sign up** | Account access |
| **Consent** | Explain what is captured, stored, for how long, and how to delete |
| **Capture** | Guided multi-angle photo/video capture on the phone, with live quality hints |
| **My Model** | Processing status, 360° preview of the saved model, delete/export buttons |
| **Catalog** | Browse shirts and pants |
| **Try-On** | 360° viewer with independent shirt and pants selectors |

## 1.3 Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Capture front, side, back and overlapping views of a person with a phone camera; MacBook used for development and processing | Must |
| FR-02 | Create a 3D representation that preserves the person's original appearance as closely as technically possible — no fantasy avatar | Must |
| FR-03 | Display the saved model in an interactive 360° viewer (rotate, zoom) | Must |
| FR-04 | Choose and change shirts and pants **independently** from a catalog; support outfit combinations | Must |
| FR-05 | Reuse a saved 3D profile without rescanning for each clothing change | Must |
| FR-06 | Store the profile until the customer requests deletion, with informed consent and applicable privacy rules | Must |
| FR-07 | Customer can view, export (where feasible) and delete their profile; access restricted to their own data | Must |
| FR-08 | No controls to edit face or body proportions | Must |
| FR-09 | Size recommendations | Later (optional) |

## 1.4 Technical constraints (must be understood before building)

1. **Phone images do not give an accurate body measurement.** Hair, loose clothing, hidden surfaces, lighting and movement all cause errors.
2. **A 360° capture is not a clean, editable body mesh.** A raw photogrammetry mesh includes the clothes the person wore and usually cannot "change clothes."
3. **Editable body + garment fitting are two separate problems.** One is body reconstruction and the other is garment alignment and cloth simulation.
4. **A try-on is a visual preview, not a size or fit guarantee.** It must be labelled that way unless validated.
5. **Face and body data are sensitive.** You need clear consent, encryption, data minimization, and deletion that also covers backups.

## 1.5 Out of scope for the MVP

- Size recommendation / measurement extraction
- Realistic cloth physics simulation (evaluated in Phase 6, not promised)
- Dresses, outerwear, shoes, accessories (the existing `Garment` type allows `dress`/`outerwear`; keep them unused for now)
- Native mobile apps (the phone uses the web app in the browser)
- Public cloud deployment before the pilot

## 1.6 Success criteria

See [05-mvp-acceptance.md](05-mvp-acceptance.md). Short version: a customer can scan once, sign out, come back, rotate their saved model, and switch between at least 2 shirts and 2 pants. Their data stays private and can be deleted.
