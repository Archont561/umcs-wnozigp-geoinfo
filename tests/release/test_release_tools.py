"""Unit tests for the release helpers.

These are deliberately not integration tests: nothing here needs a tag, a
token, or a network. That is the point of moving the release logic out of
the workflow — the archive rules can be asserted with a temporary
directory instead of by tagging and watching CI.
"""

from __future__ import annotations

import sys
import tarfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS / "release"))

import archive as archive_tool  # noqa: E402
import publish as publish_tool  # noqa: E402


@pytest.mark.parametrize("tag", ["v0.1.0", "v1.2.3-rc.1", "v2026.11.21"])
def test_safe_tags_are_accepted(tag: str) -> None:
    assert archive_tool.validate_tag(tag) == tag


@pytest.mark.parametrize(
    "tag",
    [
        "0.1.0",  # missing the v prefix
        "v1.0.0/../../etc",  # path traversal
        "v1.0.0; rm -rf /",  # shell metacharacters
        "v1 0",  # whitespace
        "",
    ],
)
def test_unsafe_tags_are_rejected(tag: str) -> None:
    with pytest.raises(archive_tool.ReleaseError, match="unsafe or non-version"):
        archive_tool.validate_tag(tag)


@pytest.mark.parametrize(
    ("package", "relative", "excluded"),
    [
        ("typst", Path("main.typ"), True),
        ("typst", Path("tests/features/x.feature"), True),
        ("typst", Path("tests/deep/nested/file.py"), True),
        ("typst", Path("__pycache__/x.pyc"), True),
        ("typst", Path("nested/__pycache__/x.pyc"), True),
        ("typst", Path("module.pyc"), True),
        ("typst", Path("lib.typ"), False),
        ("typst", Path("typst.toml"), False),
        ("typst", Path("LICENSE"), False),
        ("typst", Path("README.md"), False),
        # A file merely *named* like a test stays in: only the tests/ tree is a
        # fixture, not every path containing the word.
        ("typst", Path("latest.typ"), False),
    ],
)
def test_exclusion_rules(package: str, relative: Path, excluded: bool) -> None:
    assert archive_tool.is_excluded(package, relative) is excluded


def test_required_entries_include_licence_and_declared_extras() -> None:
    # The cover page embeds this asset, so the archive has to carry it or the
    # packaged thesis renders a title page with no header.
    assert archive_tool.required_entries("typst") == (
        "typst/LICENSE",
        "typst/lib.typ",
        "typst/typst.toml",
        "typst/assets/fonts/TeXGyreTermes-Regular.otf",
        "typst/assets/fonts/LICENSE-GUST.txt",
    )
    assert archive_tool.required_entries("latex") == ("latex/LICENSE",)


def test_verify_rejects_a_leaked_fixture() -> None:
    entries = ("typst/LICENSE", "typst/lib.typ", "typst/main.typ")
    with pytest.raises(archive_tool.ReleaseError, match="still contains fixtures"):
        archive_tool.verify("typst", Path("unused.tar.gz"), entries)


def test_verify_rejects_a_missing_licence() -> None:
    entries = ("typst/lib.typ", "typst/typst.toml")
    with pytest.raises(archive_tool.ReleaseError, match="missing typst/LICENSE"):
        archive_tool.verify("typst", Path("unused.tar.gz"), entries)


def test_verify_rejects_a_missing_manifest() -> None:
    entries = ("typst/LICENSE", "typst/lib.typ")
    with pytest.raises(archive_tool.ReleaseError, match="missing typst/typst.toml"):
        archive_tool.verify("typst", Path("unused.tar.gz"), entries)


def test_built_archives_exclude_fixtures_and_keep_the_deliverable(
    tmp_path: Path,
) -> None:
    """Build the real packages into a temporary directory and inspect them."""
    archives = archive_tool.build_all("v9.9.9", "example-repo", tmp_path)
    built = {archive.package: archive for archive in archives}

    assert set(built) == {"latex", "typst"}
    typst_entries = set(built["typst"].entries)
    assert "typst/lib.typ" in typst_entries
    assert "typst/typst.toml" in typst_entries
    assert "typst/LICENSE" in typst_entries
    # No institutional mark ships. This is an assertion about absence, and it
    # is the point of the design rather than an accident: the university does
    # not license its logotype for redistribution.
    assert not any("logo" in entry.lower() for entry in typst_entries), typst_entries
    assert "typst/assets/fonts/TeXGyreTermes-Regular.otf" in typst_entries
    assert "typst/assets/fonts/LICENSE-GUST.txt" in typst_entries
    assert not any(entry.startswith("typst/tests/") for entry in typst_entries)
    assert not any(entry.startswith("typst/main.") for entry in typst_entries)

    for archive_path in tmp_path.glob("*.tar.gz"):
        with tarfile.open(archive_path) as handle:
            names = handle.getnames()
        assert not any("__pycache__" in name for name in names), names

    sums = (tmp_path / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert len(sums) == 2
    for line in sums:
        digest, filename = line.split("  ")
        assert len(digest) == 64
        assert (tmp_path / filename).is_file()


def test_release_assets_require_checksums(tmp_path: Path) -> None:
    (tmp_path / "repo-latex-v1.tar.gz").write_bytes(b"x")
    with pytest.raises(publish_tool.ReleaseError, match="build the archives first"):
        publish_tool.release_assets(tmp_path)


def test_release_assets_fail_loudly_when_empty(tmp_path: Path) -> None:
    with pytest.raises(publish_tool.ReleaseError, match="no archives found"):
        publish_tool.release_assets(tmp_path)


def test_release_assets_put_checksums_last(tmp_path: Path) -> None:
    (tmp_path / "b-typst-v1.tar.gz").write_bytes(b"y")
    (tmp_path / "a-latex-v1.tar.gz").write_bytes(b"x")
    (tmp_path / "SHA256SUMS").write_text("", encoding="utf-8")
    assets = publish_tool.release_assets(tmp_path)
    assert [Path(a).name for a in assets] == [
        "a-latex-v1.tar.gz",
        "b-typst-v1.tar.gz",
        "SHA256SUMS",
    ]


def test_command_creates_when_absent() -> None:
    command = publish_tool.release_command("v1.0.0", "o/r", ["a.tar.gz"], exists=False)
    assert command[:3] == ["gh", "release", "create"]
    assert "--verify-tag" in command
    assert "--generate-notes" in command
    assert "Source release v1.0.0" in command
    assert "--clobber" not in command


def test_command_updates_when_present() -> None:
    command = publish_tool.release_command("v1.0.0", "o/r", ["a.tar.gz"], exists=True)
    assert command[:3] == ["gh", "release", "upload"]
    assert "--clobber" in command
    # An update must not re-create the release or regenerate its notes.
    assert "--verify-tag" not in command
    assert "--generate-notes" not in command


def test_the_package_ships_no_institutional_mark() -> None:
    """No logo file may creep back into the package.

    The package draws its title-page mark from a path the caller supplies,
    because UMCS does not license its logotype for redistribution. A bundled
    copy would re-introduce exactly the licensing question this design removes,
    and it would do so silently.
    """
    package = Path(__file__).resolve().parents[2] / "packages" / "typst"
    offenders = [
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and "logo" in path.name.lower()
    ]
    assert offenders == [], (
        "the package must not bundle an institutional mark, but these files "
        f"look like one: {offenders}"
    )
