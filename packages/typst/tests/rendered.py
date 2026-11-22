"""Measure where ink lands on a rendered page.

The package's centring is a layout property, and Typst exposes no query for
"is this line centred". So the tests render a page to PNG and measure the
bounding box of each band of ink instead. That keeps the assertion on what a
reader would actually see, which is what SPEC-TYP claims, rather than on the
source that is supposed to produce it.

Only the PNG subset Typst emits is handled: 8-bit, non-interlaced, colour type
0/2/4/6. The standard library's `zlib` is enough for the inflate, and decoding
here avoids adding Pillow to the environment for one assertion.
"""

from __future__ import annotations

import os
import struct
import subprocess
import zlib
from dataclasses import dataclass
from pathlib import Path

# Typst's `--format png` writes RGBA (colour type 6) at the moment; the other
# truecolour/greyscale variants cost three lines and make the helper robust to
# a change of default.
_CHANNELS = {0: 1, 2: 3, 4: 2, 6: 4}

#: The root Pixi environment ships DejaVu Sans and Ubuntu under its own
#: ``fonts/`` directory. Typst only looks there when told to, and a render
#: without them silently substitutes a serif — which changes the title page's
#: metrics, so every measurement below would be taken from the wrong document.
FONT_DIR = Path(__file__).resolve().parents[3] / ".pixi" / "envs" / "default" / "fonts"


def typst_env() -> dict[str, str]:
    """Return an environment that lets Typst find the fonts this repo ships."""
    env = dict(os.environ)
    if FONT_DIR.is_dir():
        env["TYPST_FONT_PATHS"] = str(FONT_DIR)
    return env


def decode_png(data: bytes) -> tuple[int, int, int, bytes]:
    """Return ``(width, height, channels, pixels)`` for a PNG file's bytes."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    pos, idat, header = 8, [], None
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        ctype = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        if ctype == b"IHDR":
            header = struct.unpack(">IIBBBBB", chunk)
        elif ctype == b"IDAT":
            idat.append(chunk)
        elif ctype == b"IEND":
            break
        pos += 12 + length
    if header is None:
        raise ValueError("PNG has no IHDR chunk")
    width, height, depth, colour, _, _, interlace = header
    if depth != 8 or interlace != 0:
        raise ValueError(f"unsupported PNG (depth {depth}, interlace {interlace})")
    channels = _CHANNELS[colour]

    raw = zlib.decompress(b"".join(idat))
    stride = width * channels
    pixels = bytearray()
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        line = bytearray(raw[offset : offset + stride])
        offset += stride
        _unfilter(filter_type, line, previous, channels)
        pixels += line
        previous = line
    return width, height, channels, bytes(pixels)


def _unfilter(filter_type: int, line: bytearray, previous: bytearray, bpp: int) -> None:
    """Reverse one scanline filter in place (PNG spec, section 9.2)."""
    if filter_type == 0:
        return
    if filter_type == 1:
        for i in range(bpp, len(line)):
            line[i] = (line[i] + line[i - bpp]) & 0xFF
    elif filter_type == 2:
        for i in range(len(line)):
            line[i] = (line[i] + previous[i]) & 0xFF
    elif filter_type == 3:
        for i in range(len(line)):
            left = line[i - bpp] if i >= bpp else 0
            line[i] = (line[i] + ((left + previous[i]) >> 1)) & 0xFF
    elif filter_type == 4:
        for i in range(len(line)):
            left = line[i - bpp] if i >= bpp else 0
            up = previous[i]
            up_left = previous[i - bpp] if i >= bpp else 0
            estimate = left + up - up_left
            distances = (
                abs(estimate - left),
                abs(estimate - up),
                abs(estimate - up_left),
            )
            if distances[0] <= distances[1] and distances[0] <= distances[2]:
                predicted = left
            elif distances[1] <= distances[2]:
                predicted = up
            else:
                predicted = up_left
            line[i] = (line[i] + predicted) & 0xFF
    else:
        raise ValueError(f"unknown PNG filter type {filter_type}")


@dataclass(frozen=True)
class Band:
    """A horizontal run of rows that contain ink, with its ink bounding box."""

    top: int
    bottom: int
    left: int
    right: int

    @property
    def centre(self) -> float:
        return (self.left + self.right) / 2

    @property
    def width(self) -> int:
        return self.right - self.left


def ink_bands(
    data: bytes,
    threshold: int = 128,
    gap: int = 6,
    exclude_columns: tuple[int, int] | None = None,
) -> list[Band]:
    """Group the page's inked rows into vertical bands.

    ``exclude_columns`` drops an inclusive pixel range before grouping, which
    is what makes a page with a full-height rule measurable: the rule would
    otherwise join every band it crosses into one.

    A band is a run of rows with at least one dark pixel, merged across gaps of
    up to ``gap`` blank rows. At 72 ppi a 12 pt line is about 12 rows and the
    leading between lines leaves a gap of two or three rows, so a ``gap`` of 6
    keeps one line of text as one band while still merging a table's rows and a
    box's two strokes into a single band.
    """
    width, height, channels, pixels = decode_png(data)
    found: list[Band] = []
    current: list[int] | None = None
    for y in range(height):
        base = y * width * channels
        left = right = None
        for x in range(width):
            if exclude_columns is not None and exclude_columns[0] <= x <= exclude_columns[1]:
                continue
            index = base + x * channels
            if min(pixels[index], pixels[index + 1], pixels[index + 2]) < threshold:
                if left is None:
                    left = x
                right = x
        if left is None:
            if current is not None and y - current[1] > gap:
                found.append(Band(*current))
                current = None
            continue
        if current is None:
            current = [y, y, left, right]
        else:
            current[1] = y
            current[2] = min(current[2], left)
            current[3] = max(current[3], right)
    if current is not None:
        found.append(Band(*current))
    return found


def render_bands(
    source: Path, work: Path, page: int = 1, ppi: int = 72
) -> tuple[int, int, list[Band]]:
    """Compile ``source`` and return ``(width_px, height_px, bands)``."""
    target = work / "page.png"
    result = subprocess.run(
        [
            "typst",
            "compile",
            "--format",
            "png",
            "--ppi",
            str(ppi),
            "--pages",
            str(page),
            str(source),
            str(target),
        ],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env=typst_env(),
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    image = target.read_bytes()
    width, height, _, _ = decode_png(image)
    return width, height, ink_bands(image)
