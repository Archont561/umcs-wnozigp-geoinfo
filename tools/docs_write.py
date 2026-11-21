"""Render root documentation from the Jinja2 templates."""

from __future__ import annotations

import sys
from pathlib import Path

from tasknest import ToolContext, tool

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docs import render_docs  # noqa: E402


@tool(description="Render README.md and AGENTS.md from their templates.")
def docs_write(ctx: ToolContext) -> None:
    """Write the generated root documentation files."""
    render_docs(check_only=False)
