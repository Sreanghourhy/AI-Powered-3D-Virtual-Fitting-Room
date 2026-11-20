"""Validate and clean uploaded photos before they are stored.

Every photo is re-encoded as JPEG, which removes all metadata (EXIF/GPS/device info)
and anything that isn't real image data.
"""

import io
from dataclasses import dataclass

from PIL import Image, ImageOps, UnidentifiedImageError

MAX_UPLOAD_BYTES = 8 * 1024 * 1024
MAX_SIDE = 4096
JPEG_QUALITY = 92
_SIGNATURES = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n")  # JPEG, PNG


class ImageRejected(ValueError):
    """The upload is not an acceptable image (message is safe to show)."""


@dataclass
class CleanImage:
    data: bytes
    width: int
    height: int


def clean_image(raw: bytes) -> CleanImage:
    if not raw.startswith(_SIGNATURES):
        raise ImageRejected("Only JPEG or PNG images are accepted")
    try:
        with Image.open(io.BytesIO(raw)) as img:
            img.load()
            img = ImageOps.exif_transpose(img)  # apply orientation, then drop EXIF
            img = img.convert("RGB")
            if max(img.size) > MAX_SIDE:
                img.thumbnail((MAX_SIDE, MAX_SIDE))
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=JPEG_QUALITY, optimize=True)  # no exif=
            return CleanImage(out.getvalue(), img.width, img.height)
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ImageRejected("The image could not be read") from exc
