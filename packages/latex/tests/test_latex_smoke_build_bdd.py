from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.integration
scenarios(str(Path(__file__).parent / "features" / "latex-smoke-build.feature"))


@given("the LaTeX package contains its dummy main", target_fixture="project_root")
def project_root() -> Path:
    assert (ROOT / "packages" / "latex" / "main.tex").is_file()
    return ROOT


@when("I run the LaTeX Tasknest build")
def run_latex_build(project_root: Path) -> Path:
    subprocess.run(["tasknest", "run", "latex", "build"], cwd=project_root, check=True)
    return project_root


@then("the LaTeX smoke PDF is written under dist")
def latex_pdf_exists(project_root: Path) -> None:
    assert (project_root / "dist" / "latex" / "main.pdf").is_file()


@then("the LaTeX PDF has a valid header and trailer")
def latex_pdf_framing_is_valid(project_root: Path) -> None:
    content = (project_root / "dist" / "latex" / "main.pdf").read_bytes()
    assert content.startswith(b"%PDF-")
    assert b"%%EOF" in content[-2048:]
