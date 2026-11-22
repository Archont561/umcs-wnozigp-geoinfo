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
FIELD_TOLERANCE_PT = 2.0

CITY_TOP_PT = 736.7


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
    return ink_bands(image, exclude_columns=rule_columns), scale


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


@then("the first band of ink is the logo, at the sample's position")
def logo_is_in_the_corner(bands: tuple[list[Band], float]) -> None:
    rows, scale = bands
    logo = rows[0]
    assert abs(logo.left * scale - LOGO_LEFT_PT) <= 2, (
        f"the logo starts at {logo.left * scale:.1f} pt, the sample has "
        f"{LOGO_LEFT_PT} pt"
    )
    assert abs(logo.top * scale - LOGO_TOP_PT) <= 2, (
        f"the logo starts at {logo.top * scale:.1f} pt from the top, the "
        f"sample has {LOGO_TOP_PT} pt"
    )
    # The eagle and the wordmark share the band, so it is wider than it is tall
    # and it sits above every line of text.
    assert logo.width > logo.bottom - logo.top, (
        "the first band is not the wide logo-and-wordmark image"
    )
    assert logo.bottom * scale < 160, (
        f"the logo band runs to {logo.bottom * scale:.1f} pt, so it is not the "
        "image but the heading below it"
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
