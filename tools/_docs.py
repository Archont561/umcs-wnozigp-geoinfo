"""Shared rendering helpers for the Tasknest documentation tools."""

from __future__ import annotations

import difflib
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
CONTEXT = {"project_title": "UMCS WNoZiGP Geoinformatics thesis templates"}


def render_docs(*, check_only: bool) -> bool:
    """Render generated root documentation or fail if it is stale."""
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        autoescape=False,
    )
    success = True
    for name in ("README.md", "AGENTS.md"):
        expected = env.get_template(name + ".j2").render(**CONTEXT)
        target = ROOT / name
        actual = target.read_text(encoding="utf-8") if target.exists() else ""
        if actual == expected:
            print(f"OK {name}")
        elif check_only:
            success = False
            print(
                "".join(
                    difflib.unified_diff(
                        actual.splitlines(True),
                        expected.splitlines(True),
                        fromfile=name,
                        tofile=f"generated/{name}",
                    )
                )
            )
        else:
            target.write_text(expected, encoding="utf-8")
            print(f"WROTE {name}")
    return success
