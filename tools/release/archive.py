"""Build and verify the source archives attached to a tagged release.

This module is the whole of the archive step that used to live inline in
`.github/workflows/release.yml`. Keeping it in Python does two things the
shell version could not: the exclusion and presence rules become ordinary
functions that can be tested without a tag, and the workflow stops being a
place where logic hides.

The rules it enforces come from QA-009 (fixtures are not deliverable) and
ADR-14 (each archive carries its own licence):

- fixtures (`main.*`, `tests/`) never enter an archive;
- `LICENSE` must always be present;
- a package may declare further files that its archive must contain, because
  asserting only the absences would let a tarball of READMEs pass.

Run it directly (`python3 tools/release/archive.py v1.2.3`) or through the
Tasknest task `release.archive`. Both routes call the same functions, so the
workflow and a maintainer's laptop cannot drift apart.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tarfile
from typing import NamedTuple
from pathlib import Path

from tasknest import ToolContext, tool

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path("dist") / "release"

#: A tag becomes a filename, so it is validated before it is used as one.
TAG_PATTERN = re.compile(r"^v[0-9A-Za-z._-]+$")

#: Directory names that never belong in a source archive.
EXCLUDED_DIR_NAMES = frozenset({"__pycache__", ".pytest_cache"})

#: File suffixes that are build noise regardless of location.
EXCLUDED_FILE_SUFFIXES = (".pyc", ".pyo")

#: Per-package required entries, relative to the package directory. `LICENSE`
#: is added to every package by :func:`required_entries`.
PACKAGE_EXTRAS = {
    "latex": (),
    # The cover page embeds the logo, so a tarball without it compiles to a
    # page missing its header rather than failing loudly.
    "typst": ("lib.typ", "typst.toml", "assets/umcs-logo.png"),
}


class ReleaseError(RuntimeError):
    """A release precondition failed."""


class Archive(NamedTuple):
    """One built archive and the entries it was verified to contain."""

    package: str
    path: Path
    entries: tuple[str, ...]

    @property
    def digest(self) -> str:
        """Return the SHA-256 of the archive."""
        return hashlib.sha256(self.path.read_bytes()).hexdigest()


def validate_tag(tag: str) -> str:
    """Return ``tag`` if it is safe to embed in a filename."""
    if not TAG_PATTERN.fullmatch(tag):
        raise ReleaseError(f"Refusing unsafe or non-version tag name: {tag!r}")
    return tag


def required_entries(package: str) -> tuple[str, ...]:
    """Return the archive paths that must exist for ``package``."""
    extras = PACKAGE_EXTRAS[package]
    return (f"{package}/LICENSE", *(f"{package}/{name}" for name in extras))


def is_excluded(package: str, relative: Path) -> bool:
    """Decide whether ``relative`` (inside ``package``) stays out of the archive."""
    parts = relative.parts
    if any(part in EXCLUDED_DIR_NAMES for part in parts[:-1]):
        return True
    if parts[0] == "tests":
        # The whole colocated test tree is a fixture (TYP-004, LTX-003).
        return True
    if len(parts) == 1 and parts[0].startswith("main."):
        # The smoke main is a fixture, not the deliverable.
        return True
    if relative.name.endswith(EXCLUDED_FILE_SUFFIXES):
        return True
    return False


def iter_archive_members(package: str, package_dir: Path) -> list[tuple[Path, str]]:
    """Yield sorted ``(source, arcname)`` pairs for one package.

    Sorting makes the archive deterministic for a given checkout, so a
    rebuild of the same commit produces the same file order.
    """
    members: list[tuple[Path, str]] = []
    for path in sorted(package_dir.rglob("*")):
        relative = path.relative_to(package_dir)
        if is_excluded(package, relative):
            continue
        members.append((path, f"{package}/{relative.as_posix()}"))
    return members


def build_archive(package: str, tag: str, repository_name: str, output_dir: Path) -> Archive:
    """Create ``<repo>-<package>-<tag>.tar.gz`` and verify its entries."""
    package_dir = ROOT / "packages" / package
    if not package_dir.is_dir():
        raise ReleaseError(f"Package directory is missing: {package_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{repository_name}-{package}-{tag}.tar.gz"

    members = iter_archive_members(package, package_dir)
    with tarfile.open(archive_path, "w:gz") as archive:
        for source, arcname in members:
            archive.add(source, arcname=arcname, recursive=False)

    with tarfile.open(archive_path, "r:gz") as archive:
        entries = tuple(sorted(archive.getnames()))

    verify(package, archive_path, entries)
    return Archive(package=package, path=archive_path, entries=entries)


def verify(package: str, archive_path: Path, entries: tuple[str, ...]) -> None:
    """Fail if the archive still contains fixtures or has lost a required file."""
    present = set(entries)
    leaked = sorted(
        entry
        for entry in present
        if entry.split("/")[0] == package
        and is_excluded(package, Path(*entry.split("/")[1:]))
    )
    if leaked:
        raise ReleaseError(
            f"the {package} archive still contains fixtures: {', '.join(leaked)}"
        )
    for required in required_entries(package):
        if required not in present:
            raise ReleaseError(f"the {package} archive is missing {required}")


def build_all(tag: str, repository_name: str, output_dir: Path) -> list[Archive]:
    """Build every package archive and write ``SHA256SUMS`` beside them."""
    validate_tag(tag)
    archives = [
        build_archive(package, tag, repository_name, output_dir) for package in PACKAGE_EXTRAS
    ]
    sums = output_dir / "SHA256SUMS"
    sums.write_text(
        "".join(f"{archive.digest}  {archive.path.name}\n" for archive in archives),
        encoding="utf-8",
    )
    return archives


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point used by the release workflow."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tag", help="release tag, for example v0.1.0")
    parser.add_argument(
        "--repository-name",
        required=True,
        help="repository name used as the archive filename prefix",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="directory for the archives and SHA256SUMS",
    )
    args = parser.parse_args(argv)

    try:
        archives = build_all(args.tag, args.repository_name, args.output_dir)
    except ReleaseError as error:
        print(f"::error::{error}", file=sys.stderr)
        return 1

    for archive in archives:
        size = archive.path.stat().st_size
        print(f"{archive.path}  ({size} bytes, {len(archive.entries)} entries)")
    return 0


@tool(
    description="Build and verify the per-package source archives for a tagged release.",
    inputs=["packages", "tools/release/archive.py"],
    outputs=["dist/release"],
)
def archive(ctx: ToolContext) -> None:
    """Build the release archives from the environment, not from arguments."""
    import os

    tag = os.environ.get("TAG_NAME")
    repository_name = os.environ.get("REPOSITORY_NAME")
    if not tag or not repository_name:
        raise ReleaseError("TAG_NAME and REPOSITORY_NAME must be set")

    for built in build_all(tag, repository_name, ROOT / OUTPUT_DIR):
        print(built.path.relative_to(ROOT), len(built.entries), "entries")


if __name__ == "__main__":
    raise SystemExit(main())
