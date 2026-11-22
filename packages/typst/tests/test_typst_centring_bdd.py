"""Scenarios asserting that illustrations sit in the middle of the text column.

See ``rendered.py`` for why these measure a PNG instead of querying Typst: the
claim is about the page a reader gets, and no query reports alignment. SPEC-TYP
records that the faculty document does not require any particular alignment for
illustrations, so this file pins down a maintainer decision rather than a
quoted rule.

Each fixture is deliberately minimal so the bands of ink on the page are known
in order: a figure renders as body, caption, source; a table as caption, body,
source; a listing as caption, code, source. The scenarios rely on that order
instead of guessing which band is which.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest
from pytest_bdd import given, scenarios, then, when

from rendered import Band, render_bands

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "packages" / "typst"

pytestmark = pytest.mark.integration
scenarios(str(Path(__file__).parent / "features" / "typst-centring.feature"))

# SRC-003 fixes 2.5 cm margins on A4, so the text column is where the page
# starts plus one margin and ends minus the other. Deriving it from the page
# width keeps the assertion independent of the ppi the helper uses.
PAGE_WIDTH_CM = 21.0
MARGIN_CM = 2.5

# One pixel of slack. Typst places the object exactly, so the only error is the
# rounding of the measured ink box; a looser bound would let a left-aligned
# object pass on a narrow body.
TOLERANCE_PX = 2


class Rendered(NamedTuple):
    """The three bands of one minimal document, already identified by role."""

    object: Band
    caption: Band
    source: Band
    page_width: int


def _document(body: str) -> str:
    return f"""
    #import "lib.typ": *
    #let meta = (programme: "G", specialisation: "S", author: "A", album: "1",
      title: "T", title-en: "T", supervisor: "S", department: "D",
      city: "Lublin", year: "2027")
    #show: umcs-thesis.with(cycle: "magisterska", meta: meta)
    {body}
    """


def _render(tmp_path: Path, body: str, order: tuple[str, str, str]) -> Rendered:
    """Render ``body`` and attach the bands to roles in the order they appear.

    The order is a property of the constructor the body uses and is asserted
    elsewhere: a figure puts its caption below the body (SRC-018), a table and
    a listing put theirs above it (SRC-015). Taking it as a parameter keeps
    this file about horizontal placement only.
    """
    (tmp_path / "lib.typ").write_text(
        (PACKAGE / "lib.typ").read_text(encoding="utf-8"), encoding="utf-8"
    )
    source = tmp_path / "doc.typ"
    source.write_text(_document(body), encoding="utf-8")
    page_width, page_height, bands = render_bands(source, tmp_path)
    # SRC-008 puts the page number at the bottom centre, so anything in the
    # last tenth of the page is the footer rather than content.
    content = [b for b in bands if b.top < page_height * 0.9]
    assert len(content) == 3, (
        f"expected three bands of ink (object, caption, source), got "
        f"{[(b.top, b.left, b.right) for b in content]}"
    )
    by_role = dict(zip(order, content, strict=True))
    return Rendered(by_role["object"], by_role["caption"], by_role["source"], page_width)


def _assert_centred(band: Band, page_width: int, what: str) -> None:
    margin = page_width * (MARGIN_CM / PAGE_WIDTH_CM)
    expected = margin + (page_width - 2 * margin) / 2
    assert abs(band.centre - expected) <= TOLERANCE_PX, (
        f"{what} is not centred: its ink spans x {band.left}-{band.right} px "
        f"(centre {band.centre:.1f}), but the text column's centre is "
        f"{expected:.1f}"
    )


def _assert_left_aligned(band: Band, page_width: int, what: str) -> None:
    margin = page_width * (MARGIN_CM / PAGE_WIDTH_CM)
    assert abs(band.left - margin) <= TOLERANCE_PX, (
        f"{what} should start at the left margin ({margin:.1f} px) but starts "
        f"at {band.left} px"
    )


@given("a document containing only a narrow figure", target_fixture="rendered")
def narrow_figure(tmp_path: Path) -> Rendered:
    # 40 % wide on purpose: a full-width body would sit in the middle of the
    # column whether or not the package centres it.
    return _render(
        tmp_path,
        """
        #figure-with-source(caption: [Podpis ryciny], source: [źródło])[
          #rect(width: 40%, height: 6mm, fill: black)
        ]
        """,
        order=("object", "caption", "source"),
    )


@given("a document containing only a narrow table", target_fixture="rendered")
def narrow_table(tmp_path: Path) -> Rendered:
    return _render(
        tmp_path,
        """
        #table-with-source(caption: [Podpis tabeli], source: [źródło])[
          #table(columns: 2, stroke: 0.5pt, [A], [B], [1], [2])
        ]
        """,
        order=("caption", "object", "source"),
    )


@given("a document containing only a listing", target_fixture="rendered")
def listing_document(tmp_path: Path) -> Rendered:
    return _render(
        tmp_path,
        """
        #listing(caption: [Podpis listingu], source: [źródło])[
          #raw(block: true, "delta = (a2 - a1) / a1 * 100")
        ]
        """,
        order=("caption", "object", "source"),
    )


@when("I render the first page and measure its bands of ink", target_fixture="bands")
def measure_bands(rendered: Rendered) -> Rendered:
    return rendered


@then("the figure body is centred on the text column")
@then("the table body is centred on the text column")
def body_is_centred(bands: Rendered) -> None:
    _assert_centred(bands.object, bands.page_width, "the illustration body")


@then("the figure caption is centred on the text column")
@then("the table caption is centred on the text column")
@then("the listing caption is centred on the text column")
def caption_is_centred(bands: Rendered) -> None:
    _assert_centred(bands.caption, bands.page_width, "the illustration caption")


@then("the listing code starts at the left margin like its source line")
def code_is_left_aligned(bands: Rendered) -> None:
    # Centring a code block would misalign its own indentation, so the code
    # keeps the left margin exactly like the source line beneath it.
    _assert_left_aligned(bands.object, bands.page_width, "the listing's code")
    # The source line is italic, so its first glyph's ink starts a pixel or two
    # inside the margin; the code's does not. Both are left aligned, so the
    # check is that they agree to within that bearing rather than exactly.
    assert abs(bands.object.left - bands.source.left) <= TOLERANCE_PX, (
        f"the code starts at {bands.object.left} px but its source line starts "
        f"at {bands.source.left} px"
    )
