"""Build disposable WebP stage and thumbnail assets for the static preview.

Original cover files remain the editable source in content-pool/packs.
Requires Pillow with WebP support (`python -m pip install Pillow`).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps, features


def convert(source: Path, target: Path, max_size: tuple[int, int], quality: int) -> int:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, "WEBP", quality=quality, method=6)
    return target.stat().st_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not features.check("webp"):
        raise RuntimeError("Pillow was built without WebP support")
    count = 0
    original = optimized = 0
    for image in sorted(args.source.glob("*/images/*")):
        if image.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        relative = image.relative_to(args.source)
        destination = args.output / relative.parent
        original += image.stat().st_size
        optimized += convert(image, destination / (image.stem + ".webp"), (940, 1672), 80)
        optimized += convert(image, destination / (image.stem + "-thumb.webp"), (400, 711), 72)
        count += 1
    print(f"Optimized {count} preview covers: {original / 1048576:.1f} MiB source -> "
          f"{optimized / 1048576:.1f} MiB stage + thumbnails")


if __name__ == "__main__":
    main()
