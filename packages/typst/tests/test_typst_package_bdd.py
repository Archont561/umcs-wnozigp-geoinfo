"""BDD scenarios asserting the Typst package against the faculty's rules.

Each step shells out to the pinned `typst` and reads the document's own
metadata with `typst query`, so the assertions are on rendered structure
rather than on a reviewer's impression. See SPEC-TYP (backlog/docs/doc-5)
for the contract and SPEC-SOURCE (doc-3) for the rule each scenario cites.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from rendered import typst_env

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "packages" / "typst"
MAIN = PACKAGE / "main.typ"

pytestmark = pytest.mark.integration
scenarios(str(Path(__file__).parent / "features" / "typst-package.feature"))


def run_typst(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    # The font path matters: the title page sets its heading in a sans face the
    # environment ships, and Typst only finds it when told where to look. Without
    # this the compiler warns and substitutes a serif.
    return subprocess.run(
        ["typst", *args],
        cwd=cwd or PACKAGE,
        capture_output=True,
        text=True,
        check=False,
        env=typst_env(),
    )


def query(label: str, source: Path = MAIN) -> list[dict]:
    """Return the values of a query label, parsed from Typst's JSON output."""
    result = run_typst("query", str(source), f"<{label}>")
    assert result.returncode == 0, result.stderr
    return [entry["value"] for entry in json.loads(result.stdout)]


def compile_document(text: str) -> subprocess.CompletedProcess[str]:
    """Compile inline Typst source against lib.typ in a temporary directory."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        (work / "lib.typ").write_text(
            (PACKAGE / "lib.typ").read_text(encoding="utf-8"), encoding="utf-8"
        )
        source = work / "doc.typ"
        source.write_text(text, encoding="utf-8")
        return run_typst("compile", str(source), str(work / "doc.pdf"), cwd=work)


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------


@given("the Typst package has a demo main", target_fixture="demo")
def demo_main() -> Path:
    assert MAIN.is_file(), "packages/typst/main.typ is missing"
    assert (PACKAGE / "lib.typ").is_file(), "packages/typst/lib.typ is missing"
    return MAIN


@given("a document setting an unknown meta key", target_fixture="bad_doc")
def unknown_key_document() -> subprocess.CompletedProcess[str]:
    return compile_document(
        """
        #import "lib.typ": *
        #show: umcs-thesis.with(cycle: "magisterska", meta: (
          author: "A", album: "1", title: "T", title-en: "T2",
          supervisor: "S", department: "D",
          promoter: "typo for supervisor",
        ))
        = Wstęp
        Tekst.
        """
    )


@given("a document omitting the cycle", target_fixture="bad_doc")
def missing_cycle_document() -> subprocess.CompletedProcess[str]:
    return compile_document(
        """
        #import "lib.typ": *
        #show: umcs-thesis.with(meta: (
          author: "A", album: "1", title: "T", title-en: "T2",
          supervisor: "S", department: "D",
        ))
        = Wstęp
        Tekst.
        """
    )


@given("a document with an unsourced figure", target_fixture="bad_doc")
def unsourced_figure_document() -> subprocess.CompletedProcess[str]:
    return compile_document(
        """
        #import "lib.typ": *
        #show: umcs-thesis.with(cycle: "magisterska", meta: (
          author: "A", album: "1", title: "T", title-en: "T2",
          supervisor: "S", department: "D",
        ))
        = Wstęp
        #figure-with-source(caption: [Bez źródła])[#rect(width: 1cm, height: 1cm)]
        """
    )


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------


@when("I compile the demo main with Typst", target_fixture="compiled")
def compile_demo(demo: Path) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        return run_typst("compile", str(demo), str(Path(tmp) / "main.pdf"))


@when("I query the document counters", target_fixture="counters")
def query_counters(demo: Path) -> dict:
    values = query("umcs-counters", demo)
    assert len(values) == 1, f"expected one counter record, got {len(values)}"
    return values[0]


@when("I query the registered illustrations", target_fixture="illustrations")
def query_illustrations(demo: Path) -> list[dict]:
    return query("umcs-illustration", demo)


@when("I query the abstract", target_fixture="abstract_record")
def query_abstract(demo: Path) -> dict:
    values = query("umcs-abstract", demo)
    assert len(values) == 1, f"expected one abstract record, got {len(values)}"
    return values[0]


@when("I compile it with Typst", target_fixture="bad_result")
def compile_bad(bad_doc: subprocess.CompletedProcess[str]):
    return bad_doc


@when("I query the chapters", target_fixture="chapters")
def query_chapters(demo: Path) -> list[dict]:
    return query("umcs-chapter", demo)


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------


@then("the compiled PDF has a valid header and trailer")
def pdf_is_well_formed(compiled: subprocess.CompletedProcess[str]) -> None:
    assert compiled.returncode == 0, compiled.stderr
    assert "warning" not in compiled.stderr.lower(), compiled.stderr


@then("the counters report one table, two figures and one listing")
def counters_are_independent(counters: dict) -> None:
    # Each registered class is numbered independently. The photograph on the
    # demo page is deliberately a figure: the owner removed the separate
    # photograph class (recorded in SPEC-TYP as a deviation from SRC-021).
    assert counters["tables"] == 1
    assert counters["figures"] == 2
    assert counters["listings"] == 1


@then("no photograph counter is reported")
def no_photograph_counter(counters: dict) -> None:
    # The owner directed that photographs be folded into figures and that
    # "Spis fotografii" not exist, so the counter must be gone rather than
    # merely unused.
    assert "photographs" not in counters, counters


@then("every illustration reports a source and a caption")
def illustrations_have_sources(illustrations: list[dict]) -> None:
    # SRC-022: every illustration carries a caption and a source.
    assert illustrations, "no illustrations were registered"
    for item in illustrations:
        assert item["has-source"] is True, item
        assert item["caption"] is not None, item


@then("every illustration carries a per-kind sequence number")
def illustrations_are_numbered_per_kind(illustrations: list[dict]) -> None:
    # SRC-021: numbering restarts per class, so the first of each kind is 1.
    firsts = {}
    for item in illustrations:
        firsts.setdefault(item["kind"], []).append(item["n"])
    for kind, numbers in firsts.items():
        assert numbers == list(range(1, len(numbers) + 1)), (kind, numbers)


@then("the abstract reports a character count within the faculty limit")
def abstract_within_limit(abstract_record: dict) -> None:
    # SRC-014: up to 4000 characters.
    assert abstract_record["limit"] == 4000
    assert 0 < abstract_record["chars"] <= abstract_record["limit"]


@then("the compiler fails and names the offending key")
def unknown_key_is_named(bad_result: subprocess.CompletedProcess[str]) -> None:
    assert bad_result.returncode != 0
    assert "promoter" in bad_result.stderr
    assert "unknown meta key" in bad_result.stderr


@then("the compiler fails and says the cycle is required")
def cycle_is_required(bad_result: subprocess.CompletedProcess[str]) -> None:
    assert bad_result.returncode != 0
    assert "cycle" in bad_result.stderr
    assert "required" in bad_result.stderr


@then("the compiler fails and says the source is required")
def source_is_required(bad_result: subprocess.CompletedProcess[str]) -> None:
    assert bad_result.returncode != 0
    assert "source" in bad_result.stderr


@then("the first chapter is numbered one")
def first_chapter_is_one(chapters: list[dict]) -> None:
    # SRC-013: front matter must not consume a chapter number, so the first
    # numbered chapter is 1 and the body chapters run consecutively.
    numbered = [c for c in chapters if c["number"] > 0]
    assert numbered, "no numbered chapters found"
    assert numbered[0]["number"] == 1, numbered[0]
    assert numbered[0]["title"]["text"] == "Wstęp", numbered[0]
    numbers = [c["number"] for c in numbered]
    assert numbers == sorted(numbers), f"chapter numbers are not monotonic: {numbers}"


#: Characters per line, measured, not quoted. SRC-002 asks for ~70 at 12 pt
#: and 1.5 spacing; no face available to Typst reaches that at A4 with 2.5 cm
#: margins, so the value is pinned here and the deviation is documented rather
#: than asserted away. 92 is Termes's; 84 was New Computer Modern's.
CHARS_PER_LINE = 92

#: The 160 mm measure, in points: A4 minus the 2.5 cm margins on both sides.
MEASURE_PT = (210 - 50) / 10 / 2.54 * 72


def measure_text(spec: str, sample: str) -> float:
    """Return the width in points of ``sample`` set with ``spec``.

    ``spec`` is Typst markup for the `text` set rule, so the measurement uses
    the package's own size rather than a number written here twice.
    """
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        source = work / "probe.typ"
        source.write_text(
            '#set page(width: 30cm, height: 6cm, margin: 0pt)\n'
            "#context [\n"
            f"  #metadata(measure(text({spec}, {sample})).width / 1pt) <probe>\n"
            "]\n",
            encoding="utf-8",
        )
        return query("probe", source)[0]


@then("the body face is the vendored Times substitute")
def body_face_is_termes(counters: dict) -> None:
    # The face reaches the test through the document's own metadata, so this
    # fails if the default drifts even when the demo still compiles.
    assert counters["font"] == "TeXGyreTermes", (
        f"the body is set in {counters['font']!r}; SRC-002 asks for Times New "
        "Roman and TeXGyreTermes is the vendored substitute (TYP-006)"
    )


@then("the body face is not the wider Computer Modern")
def body_face_is_not_computer_modern(counters: dict) -> None:
    # New Computer Modern was the previous default. It is about 6 % wider per
    # character, which is the whole reason this scenario exists.
    assert counters["font"] != "New Computer Modern"


#: A 93-character Polish sentence, used as the yardstick for line length.
LINE_SAMPLE = (
    '"W pracy przedstawiono analizę zmian pokrycia terenu w zlewni '
    'Bystrzycy w latach 2000-2020."'
)


@when("I measure a line of body text at the document's own settings", target_fixture="line")
def measure_line(counters: dict) -> dict:
    # The probe uses the face the document reports, not a name written here, so
    # it measures the face actually in use and cannot drift from it.
    width = measure_text(f'size: 12pt, font: "{counters["font"]}"', LINE_SAMPLE)
    return {"chars": 93 * MEASURE_PT / width, "face": counters["font"]}


@then("the measured characters per line is about 92")
def characters_per_line_is_about_92(line: dict) -> None:
    chars = line["chars"]
    assert abs(chars - CHARS_PER_LINE) <= 3, (
        f"the body fits {chars:.1f} characters per line at the document's "
        f"settings, not the pinned {CHARS_PER_LINE}; if the face or the measure "
        "changed, confirm SRC-002's ~70-character target is still as close as "
        "it was and update this number deliberately"
    )
