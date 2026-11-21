"""Check that generated root documentation matches its templates."""

from __future__ import annotations

import sys
from pathlib import Path

from tasknest import ToolContext, tool

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docs import render_docs  # noqa: E402


@tool(description="Fail if README.md or AGENTS.md differ from their templates.")
def docs_check(ctx: ToolContext) -> None:
    """Verify the generated root documentation."""
    if not render_docs(check_only=True):
        raise RuntimeError("Generated docs are stale; run `pixi run docs-write`.")
