from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.integration
scenarios(str(Path(__file__).parent / "features" / "typst-smoke-build.feature"))


@given("the Typst package contains its dummy main", target_fixture="project_root")
def project_root() -> Path:
    assert (ROOT / "packages" / "typst" / "main.typ").is_file()
    return ROOT


@when("I run the Typst Tasknest build")
def run_typst_build(project_root: Path) -> Path:
    subprocess.run(["tasknest", "run", "typst", "build"], cwd=project_root, check=True)
    return project_root


@then("the Typst smoke PDF is written under dist")
def typst_pdf_exists(project_root: Path) -> None:
    assert (project_root / "dist" / "typst" / "main.pdf").is_file()


@then("the Typst PDF has a valid header and trailer")
def typst_pdf_framing_is_valid(project_root: Path) -> None:
    content = (project_root / "dist" / "typst" / "main.pdf").read_bytes()
    assert content.startswith(b"%PDF-")
    assert b"%%EOF" in content[-2048:]
