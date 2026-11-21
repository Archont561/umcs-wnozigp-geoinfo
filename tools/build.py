"""Build both placeholder mains through the per-format Tasknest tools."""

from __future__ import annotations

from tasknest import ToolContext, tool


@tool(
    depends=["latex.build", "typst.build"],
    description="Build the LaTeX and Typst placeholder PDFs.",
    outputs=["dist/latex/main.pdf", "dist/typst/main.pdf"],
)
def build(ctx: ToolContext) -> None:
    """Aggregate the two opt-in smoke-build tasks."""
    print("Built both placeholder PDFs; this is not a template compliance test.")
