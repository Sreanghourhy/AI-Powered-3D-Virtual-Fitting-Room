# Garment Data Format (v1)

Every garment in the catalog must follow this spec, so it lines up with body models and loads fast in the browser.

## 1. 3D file

| Property | Rule |
|----------|------|
| Format | **GLB** (binary glTF 2.0), one garment per file |
| Units | **Metres** (1 unit = 1 m) |
| Axes | **Y-up**, model faces **+Z** (same as the body model) |
| Origin | `(0, 0, 0)` at floor level, centred between the feet of the reference body |
| Reference body | Modelled/fitted on the project's reference body (chosen in Phase 4, ADR-001) |
| Triangles | ≤ **30,000** per garment (target 10–20k) |
| Textures | ≤ **2048 × 2048**. Base colour + normal (+ optional ORM). JPEG/PNG or KTX2. |
| Materials | glTF PBR metallic-roughness, ≤ 2 materials |
| Compression | Meshopt or Draco allowed (the viewer must have the decoder) |
| File size | ≤ **5 MB** (target ≤ 2 MB) |
| Skinning | Only if Phase 4 picks a template body: skinned to the **same skeleton and bone names** as the reference body |
| Node naming | Root node named `garment`. Mesh named `<garment-id>` |

## 2. Thumbnail

- PNG or WebP, **512 × 512**, transparent or light-grey background, front view.
- Same file name as the GLB: `shirt-basic-tee-white.glb` → `shirt-basic-tee-white.webp`.

## 3. Metadata (database / API)

```jsonc
{
  "id": "shirt-basic-tee-white",          // kebab-case, unique, stable
  "name": "Basic Tee — White",
  "category": "top",                      // MVP: "top" | "bottom"
  "modelUrl": "/garments/shirt-basic-tee-white.glb",
  "thumbnailUrl": "/garments/shirt-basic-tee-white.webp",
  "colors": ["#ffffff"],                  // optional, for filters
  "sizes": ["S", "M", "L"],               // optional, display only, not used for fit in MVP
  "source": {
    "author": "Project team",
    "license": "CC-BY-4.0",               // SPDX id or "proprietary"
    "url": "https://…"                    // optional
  },
  "active": true
}
```

The TypeScript version is [`src/lib/types/garment.ts`](../src/lib/types/garment.ts).

## 4. Folder layout

```text
pipeline/garments/source/      # original .blend / source files (Git LFS if big)
pipeline/garments/LICENSES.md  # source + license of every garment
static/garments/               # exported GLB + thumbnails (public catalog assets)
```

Garments are public catalog assets, so they may be served from `static/`. Scanned body models never are.

## 5. Acceptance check for a new garment

- [ ] Opens in a glTF validator (e.g. Khronos glTF-Validator) with no errors
- [ ] Triangle count, texture size and file size within limits
- [ ] Sits correctly on the reference body in `/viewer-demo` (no floating, no big clipping)
- [ ] License recorded in `LICENSES.md`
- [ ] Thumbnail present
