"""Create or update the GitHub Release for a tag.

The shell version of this step was four lines of `gh` that could not be
exercised without a token. Here the decision is a pure function
(:func:`release_command`) and only :func:`publish` touches the network, so a
test can assert the exact argv without creating anything.

The rule the workflow relied on — upload over an existing release, create
only when absent — stays identical, so re-running a failed release remains
safe.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from tasknest import ToolContext, tool

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path("dist") / "release"


class ReleaseError(RuntimeError):
    """A publishing precondition failed."""


def release_assets(output_dir: Path) -> list[str]:
    """Return the asset paths to attach, in a stable order."""
    archives = sorted(output_dir.glob("*.tar.gz"))
    if not archives:
        raise ReleaseError(f"no archives found in {output_dir}; build them first")
    sums = output_dir / "SHA256SUMS"
    if not sums.is_file():
        # Publishing archives without their checksums defeats the point of
        # generating SHA256SUMS in the first place.
        raise ReleaseError(f"missing {sums}; build the archives first")
    return [str(path) for path in (*archives, sums)]


def release_exists(tag: str, repo: str) -> bool:
    """Return whether a release for ``tag`` already exists."""
    result = subprocess.run(
        ["gh", "release", "view", tag, "--repo", repo],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def release_command(tag: str, repo: str, assets: list[str], exists: bool) -> list[str]:
    """Return the `gh` argv for this release, without running it."""
    if exists:
        return ["gh", "release", "upload", tag, *assets, "--repo", repo, "--clobber"]
    return [
        "gh",
        "release",
        "create",
        tag,
        *assets,
        "--repo",
        repo,
        "--title",
        f"Source release {tag}",
        "--generate-notes",
        "--verify-tag",
    ]


def publish(tag: str, repo: str, output_dir: Path, *, dry_run: bool = False) -> list[str]:
    """Publish the release and return the argv that was (or would be) run."""
    assets = release_assets(output_dir)
    command = release_command(tag, repo, assets, release_exists(tag, repo))
    if dry_run:
        return command
    subprocess.run(command, check=True)
    return command


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point used by the release workflow."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tag", help="release tag, for example v0.1.0")
    parser.add_argument("--repo", required=True, help="owner/name of the repository")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the gh command instead of running it",
    )
    args = parser.parse_args(argv)

    try:
        command = publish(args.tag, args.repo, args.output_dir, dry_run=args.dry_run)
    except ReleaseError as error:
        print(f"::error::{error}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(f"::error::gh failed with exit code {error.returncode}", file=sys.stderr)
        return error.returncode
    if args.dry_run:
        print(" ".join(command))
    return 0


@tool(
    description="Create or update the GitHub Release for a tag from dist/release.",
    inputs=["dist/release"],
)
def release(ctx: ToolContext) -> None:
    """Publish using the environment the workflow provides."""
    import os

    tag = os.environ.get("TAG_NAME")
    repo = os.environ.get("REPO")
    if not tag or not repo:
        raise ReleaseError("TAG_NAME and REPO must be set")
    if shutil.which("gh") is None:
        raise ReleaseError("the `gh` CLI is required to publish a release")
    publish(tag, repo, ROOT / OUTPUT_DIR)


if __name__ == "__main__":
    raise SystemExit(main())
