"""Scenarios asserting that the title page reproduces the faculty's sample.

The sample is a one-page PDF the faculty supplies with its guidelines. Its
geometry was read off that file's content stream, not estimated, and the values
below are copied from it: the logo's ink begins at (52, 70.5) pt measured from
the top-left corner, the vertical rule occupies x = 118 pt between y = 292.9 pt
and y = 709.2 pt, the heading's text starts at x = 119.5 pt, and the fields
start at x = 132.5 pt.

Measuring a render rather than querying the document is deliberate: a title
page is a fixed form, so "does it look like the sample" is a question about
pixels, and no Typst query answers it.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from rendered import Band, decode_png, ink_bands

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "packages" / "typst"
MAIN = PACKAGE / "main.typ"

pytestmark = pytest.mark.integration
scenarios(str(Path(__file__).parent / "features" / "typst-titlepage.feature"))

#: A4 in points, the page the sample and the package both use.
PAGE_WIDTH_PT = 595.28
PAGE_HEIGHT_PT = 841.89

#: The rule's column, in points, as the sample draws it.
RULE_X_PT = 118.0
RULE_LEFT_PT = 292.9
RULE_RIGHT_PT = 709.2
RULE_TOLERANCE_PT = 2.0

#: Where the sample's ink starts.
LOGO_LEFT_PT = 52.0
LOGO_TOP_PT = 70.5

#: The fields are indented 13.5 pt past the rule, so their ink begins at 132.5.
FIELD_LEFT_PT = 132.5
#: Three points, because the measurement is of *ink* and every face puts a
#: different left side bearing in front of its first glyph. The sample itself
#: varies by a point between its own lines for the same reason.
FIELD_TOLERANCE_PT = 3.0

CITY_TOP_PT = 736.7

#: The sample sets the title at 24.79 pt and the fields at 11.96 pt. Its cap
#: height is 16.4 pt for the title, so anything near the body's 8 pt means the
#: size was never applied.
TITLE_SIZE_PT = 24.79
TITLE_MIN_CAP_PT = 12.0
FIELD_MAX_CAP_PT = 12.0


@pytest.fixture(scope="module")
def page_png(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Render page 1 of the demo thesis to a PNG, once per module.

    Rendering from the source rather than from the built PDF keeps the test
    independent of whether `build-typst` ran, and it goes through the same
    font-path environment the build uses, so the measurement cannot be taken
    from a document that silently substituted a face.
    """
    import subprocess

    from rendered import typst_env

    work = tmp_path_factory.mktemp("titlepage")
    target = work / "page1.png"
    result = subprocess.run(
        [
            "typst",
            "compile",
            "--format",
            "png",
            "--ppi",
            "72",
            "--pages",
            "1",
            str(MAIN),
            str(target),
        ],
        cwd=PACKAGE,
        capture_output=True,
        text=True,
        check=False,
        env=typst_env(),
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return target


def _scale(width_px: int) -> float:
    return PAGE_WIDTH_PT / width_px


@given("the demo thesis compiled to a PDF", target_fixture="pdf")
def compiled_pdf() -> Path:
    assert MAIN.is_file(), "packages/typst/main.typ is missing"
    return MAIN


@when("I render the title page and measure its bands of ink", target_fixture="bands")
def measure_bands(page_png: Path) -> tuple[list[Band], float]:
    image = page_png.read_bytes()
    width, _, _, _ = decode_png(image)
    scale = _scale(width)
    # The rule spans the whole field area, so it has to be excluded or it would
    # merge every band it crosses into a single one.
    rule_columns = (
        int((RULE_X_PT - 2) / scale),
        int((RULE_X_PT + 2) / scale),
    )
    # A 3 px gap keeps consecutive 20 pt lines apart: the sample's two heading
    # lines are 24.5 pt apart, which is only 3 px at this resolution.
    return ink_bands(image, gap=2, exclude_columns=rule_columns), scale


@when("I measure the vertical rule on the title page", target_fixture="rule")
def measure_rule(page_png: Path) -> tuple[float, float, float]:
    """Return the rule's column, top and bottom in points."""
    width_px, height_px, channels, pixels = decode_png(page_png.read_bytes())
    scale = _scale(width_px)
    expected = round(RULE_X_PT / scale)
    best: tuple[int, int, int] | None = None
    for x in range(max(0, expected - 3), min(width_px, expected + 4)):
        run = start = 0
        for y in range(height_px):
            index = (y * width_px + x) * channels
            if min(pixels[index], pixels[index + 1], pixels[index + 2]) < 128:
                run += 1
            else:
                if best is None or run > best[2]:
                    best = (x, start, run)
                run, start = 0, y + 1
        if best is None or run > best[2]:
            best = (x, start, run)
    assert best is not None and best[2] > 100, "no vertical rule was found"
    x, start, length = best
    return x * scale, start * scale, (start + length) * scale


@then("the first band of ink occupies the mark's box at the sample's position")
def logo_box_is_in_the_corner(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    logo = rows[0]
    # The package ships no mark, so what is drawn here is the placeholder: a
    # grey outline of exactly the sample's box. The assertions are on the box
    # for that reason, and they are what would catch the placeholder being
    # resized or re-anchored — which would move every rule and field below it.
    assert abs(logo.left * scale - LOGO_LEFT_PT) <= 2, (
        f"the mark's box starts at {logo.left * scale:.1f} pt, the sample has "
        f"{LOGO_LEFT_PT} pt"
    )
    assert abs(logo.top * scale - LOGO_TOP_PT) <= 2, (
        f"the mark's box starts at {logo.top * scale:.1f} pt from the top, the "
        f"sample has {LOGO_TOP_PT} pt"
    )
    # The box is the logotype's aspect: wider than it is tall.
    assert logo.width > logo.bottom - logo.top, (
        "the first band is not the wide logotype-shaped box"
    )
    assert logo.bottom * scale < 160, (
        f"the box runs to {logo.bottom * scale:.1f} pt, so it is not the box "
        "but the heading below it"
    )


@then("the rule spans the sample's range below the heading")
def rule_matches_the_sample(rule: tuple[float, float, float]) -> None:
    x, top, bottom = rule
    assert abs(x - RULE_X_PT) <= 1, f"the rule sits at x = {x:.1f} pt, not 118"
    assert abs(top - RULE_LEFT_PT) <= RULE_TOLERANCE_PT, (
        f"the rule starts at {top:.1f} pt; the sample starts it at "
        f"{RULE_LEFT_PT} pt"
    )
    assert abs(bottom - RULE_RIGHT_PT) <= RULE_TOLERANCE_PT, (
        f"the rule ends at {bottom:.1f} pt; the sample ends it at "
        f"{RULE_RIGHT_PT} pt"
    )


@then("every field starts to the right of the rule")
def fields_are_indented(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    fields = [band for band in rows if band.top * scale > RULE_LEFT_PT]
    assert fields, "no field band was found below the rule"
    for band in fields:
        assert abs(band.left * scale - FIELD_LEFT_PT) <= FIELD_TOLERANCE_PT, (
            f"a field starts at {band.left * scale:.1f} pt, expected "
            f"{FIELD_LEFT_PT} pt (13.5 pt past the rule)"
        )


@then("the title is taller than the fields around it, at the sample's size")
def title_has_its_own_size(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    # The title sits between the album number and the English title, and a
    # 24.79 pt line is visibly taller than the 11.96 pt fields. Measuring ink
    # height rather than querying the source is what caught the original bug:
    # the size argument only positioned the line and never set the type.
    above_body = [b for b in rows if b.top * scale > 400]
    title = max(
        (b for b in above_body if b.top * scale < 460),
        key=lambda b: b.bottom - b.top,
    )
    height_pt = (title.bottom - title.top) * scale
    assert height_pt >= TITLE_MIN_CAP_PT, (
        f"the title's ink is {height_pt:.1f} pt tall; at {TITLE_SIZE_PT} pt it "
        f"should be over {TITLE_MIN_CAP_PT} pt, so it is probably still being "
        "drawn at the body's size"
    )


@then("the university heading occupies exactly two lines")
def university_is_two_lines(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    # The sample breaks the university after "Curie-Skłodowskiej" and sets
    # "w Lublinie" on the second line. Counting bands is not enough to catch a
    # face that is too wide: "w Lublinie" is short, so a wide face pushes the
    # *faculty* line down and the count still reads two. The assertion is
    # therefore on which words are where — line one runs long, line two is the
    # short one, and nothing sits between line two and the faculty.
    heading = [b for b in rows if 150 < b.top * scale < 225]
    assert len(heading) == 2, (
        "the university heading is "
        f"{len(heading)} lines, not the sample's two: "
        f"{[(round(b.top * scale, 1), round(b.right * scale, 1)) for b in heading]}"
    )
    first, second = heading
    assert (first.right - first.left) > 2 * (second.right - second.left), (
        "the university's first line is not the long one: "
        f"widths {(first.right - first.left) * scale:.0f} pt and "
        f"{(second.right - second.left) * scale:.0f} pt"
    )
    # "w Lublinie" is 94 pt wide in the sample's face and the heading starts at
    # 119.5 pt, so the second line must end near 214 pt. A wider face overruns.
    second_right = second.right * scale
    assert abs(second_right - 214) <= 12, (
        f"the university's second line ends at {second_right:.1f} pt; the "
        "sample ends it at 214 pt, so the face in use is too wide"
    )
    # The faculty line is 17 pt and must clear the heading, not overlap it.
    faculty = [b for b in rows if 225 <= b.top * scale < 260]
    assert len(faculty) == 1, f"expected one faculty line, got {len(faculty)}"


@then("every line of the two titles is separated from the next")
def titles_have_a_gap(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    # The demo's title is too long for one line at 24.79 pt, so it wraps and the
    # English title must come below it as a line of its own. The layout that
    # broke this computed the English baseline from the assumption that the
    # title is one line, which drew it *over* the second line: the two fused
    # into a single band 23 pt tall. Counting bands is therefore not enough
    # either, because fusing looks like fewer lines rather than a small gap.
    # The discriminator is the English line's own height: 14.35 pt type puts
    # about 11 pt of ink on the page, while a fused band carries two lines.
    # 545 pt is below the English title and above the diploma block, so the
    # window holds the title and the English title and nothing else.
    region = [b for b in rows if 420 < b.top * scale < 545]
    assert len(region) >= 2, f"expected the two titles, got {len(region)} band(s)"
    english = region[-1]
    english_height = (english.bottom - english.top) * scale
    above = region[-2]
    gap = (english.top - above.bottom) * scale
    assert english_height < 16 and gap > 18, (
        f"the English title's band is {english_height:.1f} pt tall and sits "
        f"{gap:.1f} pt below the line above it; a separate 14.35 pt line is "
        "about 11 pt tall, so a taller band means the English title is being "
        "drawn over the last line of the title"
    )


@then("the last band of ink is the city and year, near the bottom")
def city_and_year_close_the_page(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    last = rows[-1]
    assert abs(last.top * scale - CITY_TOP_PT) <= 3, (
        f"the city and year start at {last.top * scale:.1f} pt; the sample has "
        f"{CITY_TOP_PT} pt"
    )
    assert last.top * scale > PAGE_HEIGHT_PT * 0.85, (
        "the city and year are not in the lower part of the page"
    )


@given("a document supplying its own mark", target_fixture="supplied")
def document_with_mark(tmp_path: Path) -> Path:
    """Compile a copy of the demo that points `logo` at a stand-in image.

    The stand-in is a small dark square, so the band it produces is
    distinguishable from the placeholder's pale box by width and ink.
    """
    import subprocess

    from rendered import decode_png, typst_env

    work = tmp_path / "supplied"
    work.mkdir()
    # A 40 x 40 PNG, black: any image would do, and generating one keeps this
    # test free of a fixture file that could drift.
    import struct

    import zlib

    width = height = 40
    raw = b"".join(b"\x00" + b"\x00\x00\x00" * width for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )
    (work / "mark.png").write_bytes(png)

    # The document is compiled outside the package, so lib.typ has to travel
    # with it; the import in main.typ is relative to the document.
    (work / "lib.typ").write_text(
        (PACKAGE / "lib.typ").read_text(encoding="utf-8"), encoding="utf-8"
    )
    source = (PACKAGE / "main.typ").read_text(encoding="utf-8")
    source = source.replace("logo: none", 'logo: "mark.png"')
    (work / "doc.typ").write_text(source, encoding="utf-8")
    assert "mark.png" in source, "the demo no longer exposes the logo parameter"

    target = work / "page1.png"
    result = subprocess.run(
        ["typst", "compile", "--format", "png", "--ppi", "72", "--pages", "1",
         "doc.typ", str(target)],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env=typst_env(),
    )
    if result.returncode != 0:
        # lib.typ must be reachable from the temporary document.
        raise AssertionError(result.stderr)
    return target


@when("I render its title page and measure the bands of ink", target_fixture="supplied_bands")
def measure_supplied(supplied: Path) -> tuple[list[Band], float]:
    image = supplied.read_bytes()
    width, _, _, _ = decode_png(image)
    return ink_bands(image, gap=2), _scale(width)


@then("the first band is the supplied image, not the placeholder")
def supplied_mark_is_drawn(supplied_bands: tuple[list[Band], float]) -> None:
    rows, scale = supplied_bands
    first = rows[0]
    # The placeholder's fill is pale and its border thin; the supplied image is
    # solid black, so the height of its ink differs and, more usefully, the
    # placeholder's own "logo" label is absent. Assert the geometry the mark is
    # drawn into and that it is dark all the way through.
    assert abs(first.left * scale - LOGO_LEFT_PT) <= 2, (
        f"a supplied mark starts at {first.left * scale:.1f} pt, not the "
        f"sample's {LOGO_LEFT_PT} pt"
    )
    assert abs(first.top * scale - LOGO_TOP_PT) <= 2
    # A supplied mark is drawn at the mark's fixed width and its own aspect, so
    # a square stand-in is 245.4 pt tall — far taller than the 63.6 pt box.
    drawn_height = (first.bottom - first.top) * scale
    assert drawn_height > 200, (
        f"the supplied mark's ink is {drawn_height:.1f} pt tall, which is the "
        "placeholder's height, not the square image's; the parameter looks "
        "ignored"
    )
