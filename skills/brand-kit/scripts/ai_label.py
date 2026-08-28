#!/usr/bin/env python3
"""Create a visibly labelled, web-sized copy of an image.

This helper does not determine whether disclosure is legally required and does
not prove compliance. Use the brand-kit compliance decision record first.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - environment-dependent
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


DIGITAL_SOURCE_TYPE = "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
FONT_CANDIDATES = (
    Path("C:/Windows/Fonts/consolab.ttf"),
    Path("/System/Library/Fonts/Menlo.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"),
)


def color(value: str) -> tuple[int, int, int]:
    text = value.removeprefix("#")
    if len(text) != 6:
        raise argparse.ArgumentTypeError("Color must use #RRGGBB.")
    try:
        return tuple(int(text[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Color must use #RRGGBB.") from exc


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than zero.")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than zero.")
    return parsed


def aspect(value: str) -> float:
    try:
        width, height = value.replace(":", "/").split("/", 1)
        ratio = float(width) / float(height)
    except (ValueError, ZeroDivisionError) as exc:
        raise argparse.ArgumentTypeError("Aspect must look like 16:9.") from exc
    if ratio <= 0:
        raise argparse.ArgumentTypeError("Aspect must be positive.")
    return ratio


def find_font(explicit: Path | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if explicit:
        if not explicit.is_file():
            raise SystemExit(f"Font file not found: {explicit}")
        return ImageFont.truetype(str(explicit), size)
    for candidate in FONT_CANDIDATES:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def fit(im: Image.Image, ratio: float, anchor: str) -> Image.Image:
    width, height = im.size
    target = (max(1, round(height * ratio)), height) if width / height >= ratio else (width, max(1, round(width / ratio)))
    centering = {"top": (0.5, 0.0), "center": (0.5, 0.5), "bottom": (0.5, 1.0)}[anchor]
    return ImageOps.fit(im, target, method=Image.Resampling.LANCZOS, centering=centering)


def stamp(im: Image.Image, label: str, bg: tuple[int, int, int], fg: tuple[int, int, int], accent: tuple[int, int, int], font_path: Path | None, scale: float) -> None:
    draw = ImageDraw.Draw(im, "RGBA")
    unit = scale * (im.width / 1120)
    pad, height, gap = max(8, round(24 * unit)), max(28, round(52 * unit)), max(6, round(12 * unit))
    font = find_font(font_path, max(10, round(22 * unit)))
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    width = max(height, text_width + gap * 3 + max(3, round(4 * unit)))
    x1, y1 = im.width - pad, im.height - pad
    x0, y0 = x1 - width, y1 - height
    if x0 < 0 or y0 < 0:
        raise SystemExit("Image is too small for the selected label scale.")
    radius = max(2, round(5 * unit))
    draw.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=bg + (235,), outline=fg + (100,), width=1)
    bar = max(3, round(4 * unit))
    draw.rectangle((x0 + gap, y0 + gap, x0 + gap + bar, y1 - gap), fill=accent + (255,))
    draw.text((x0 + gap * 2 + bar, (y0 + y1) / 2), label, font=font, fill=fg + (255,), anchor="lm")


def save_jpeg_under_limit(im: Image.Image, output: Path, quality: int, max_kb: float | None) -> tuple[float, int]:
    last_quality = quality
    for current in range(quality, 29, -5):
        last_quality = current
        im.save(output, "JPEG", quality=current, optimize=True, progressive=True)
        size = output.stat().st_size / 1024
        if max_kb is None or size <= max_kb:
            return size, current
    return output.stat().st_size / 1024, last_quality


def write_metadata(output: Path) -> tuple[bool, str]:
    tool = shutil.which("exiftool")
    if not tool:
        return False, "ExifTool is not installed."
    result = subprocess.run(
        [tool, "-overwrite_original", f"-XMP-iptcExt:DigitalSourceType={DIGITAL_SOURCE_TYPE}", str(output)],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stderr.strip() or result.stdout.strip()


def transform(args: argparse.Namespace) -> dict[str, object]:
    source, output = args.input.resolve(), args.output.resolve()
    if not source.is_file():
        raise SystemExit(f"Input file not found: {source}")
    if source == output:
        raise SystemExit("Input and output must be different files.")
    if output.exists() and not args.force:
        raise SystemExit(f"Output exists; use --force to replace it: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        im = ImageOps.exif_transpose(opened).convert("RGB")
    original = im.size
    if args.aspect:
        im = fit(im, args.aspect, args.anchor)
    if args.width and im.width != args.width:
        im = im.resize((args.width, max(1, round(im.height * args.width / im.width))), Image.Resampling.LANCZOS)
    if args.label:
        stamp(im, args.label, args.bg, args.fg, args.accent, args.font, args.scale)
    extension = output.suffix.lower()
    if extension in {".jpg", ".jpeg"}:
        size_kb, quality = save_jpeg_under_limit(im, output, args.quality, args.max_kb)
    elif extension == ".png":
        im.save(output, "PNG", optimize=True)
        size_kb, quality = output.stat().st_size / 1024, None
    else:
        raise SystemExit("Output extension must be .jpg, .jpeg, or .png.")
    metadata = {"requested": args.metadata, "written": False, "detail": "not requested"}
    if args.metadata:
        ok, detail = write_metadata(output)
        metadata = {"requested": True, "written": ok, "detail": detail}
    return {"status": "PASS", "input_size": list(original), "output_size": list(im.size), "output": str(output), "size_kb": round(size_kb, 2), "quality": quality, "visible_label": bool(args.label), "metadata": metadata}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("-o", "--output", type=Path, required=True)
    p.add_argument("--width", type=positive_int)
    p.add_argument("--aspect", type=aspect)
    p.add_argument("--anchor", choices=("top", "center", "bottom"), default="center")
    p.add_argument("--label", default="AI-generated", help="Visible label; use an empty value to disable.")
    p.add_argument("--bg", type=color, default="#0B0D10")
    p.add_argument("--fg", type=color, default="#F4F1E8")
    p.add_argument("--accent", type=color, default="#C4A45F")
    p.add_argument("--font", type=Path)
    p.add_argument("--scale", type=positive_float, default=1.0)
    p.add_argument("--max-kb", type=positive_float, default=250.0)
    p.add_argument("--quality", type=int, choices=range(30, 96), default=82, metavar="30..95")
    p.add_argument("--metadata", action="store_true", help="Ask ExifTool to write DigitalSourceType metadata.")
    p.add_argument("--force", action="store_true")
    return p


def main() -> int:
    import json

    result = transform(parser().parse_args())
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
