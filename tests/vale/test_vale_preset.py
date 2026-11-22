"""Pin the PLTechnical preset's measured behaviour against its own fixture.

SPEC-EDIT records, rule by rule, what the preset matches and what it
deliberately does not. That record is only worth something if a change to the
rules fails a test rather than quietly invalidating the document, so this module
runs Vale against ``examples/vale/rule-cases.md`` and compares the finding
counts to the numbers the fixture states in its headings.

It exists because a rule was found matching grammatical nonsense and nothing
caught it: ``VerbPhrases`` had a pattern that could only match "Przeprowadzono
została analiza" and never the real passive it was meant for.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "vale" / "rule-cases.md"

#: Findings the fixture is written to produce, by rule. Read from the fixture's
#: own headings where possible; kept here so a lost finding is a failure rather
#: than a line silently disappearing from a document.
EXPECTED = {
    "PLTechnical.Bureaucratic": 2,
    "PLTechnical.Pleonasms": 2,
    "PLTechnical.VerbPhrases": 4,
    "PLTechnical.UnitSpacing": 7,
    "PLTechnical.LongSentences": 1,
}


def run_vale(*paths: Path) -> dict[str, list[dict]]:
    result = subprocess.run(
        ["vale", "--config=.vale.ini", "--output=JSON", *map(str, paths)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # Vale exits non-zero when it reports anything at all; that is expected.
    assert result.stdout.strip(), f"vale produced no JSON: {result.stderr}"
    return json.loads(result.stdout)


def test_the_fixture_produces_the_findings_it_claims() -> None:
    report = run_vale(FIXTURE)
    found = Counter(
        item["Check"] for items in report.values() for item in items
    )
    assert dict(found) == EXPECTED, (
        "the preset's findings no longer match what SPEC-EDIT and the fixture "
        f"record. Expected {EXPECTED}, got {dict(found)}."
    )


def test_the_passive_constructions_are_caught_and_the_active_one_is_not() -> None:
    # The rule's whole point. Both sides are asserted, because a pattern fixed
    # by broadening it could start flagging the verb-first form the guidance
    # itself recommends.
    sample = (
        "# Test\n\n"
        "Została przeprowadzona analiza ryzyka.\n\n"
        "Zostały przeprowadzone analizy.\n\n"
        "Przeprowadzono analizę ryzyka.\n"
    )
    work = ROOT / "examples" / "vale" / "_passive-probe.md"
    work.write_text(sample, encoding="utf-8")
    try:
        report = run_vale(work)
    finally:
        work.unlink()
    hits = [
        item
        for items in report.values()
        for item in items
        if item["Check"] == "PLTechnical.VerbPhrases"
    ]
    # Lines 3 and 5 are passive; line 7 is the recommended active form.
    assert sorted(hit["Line"] for hit in hits) == [3, 5], (
        "the passive constructions were not caught, or the active one was: "
        f"{[hit['Line'] for hit in hits]}"
    )
