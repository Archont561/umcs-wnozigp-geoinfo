"""Build the placeholder Typst main document for a smoke test."""

from __future__ import annotations

from pathlib import Path

from tasknest import ToolContext, tool


@tool(
    description="Compile the Typst dummy main with the root-pinned Typst executable.",
    inputs=["packages/typst/main.typ", "tools/typst/build.py"],
    outputs=["dist/typst/main.pdf"],
)
def build(ctx: ToolContext) -> None:
    """Compile packages/typst/main.typ to dist/typst/main.pdf."""
    root = Path(__file__).resolve().parents[2]
    output_dir = root / "dist" / "typst"
    output_dir.mkdir(parents=True, exist_ok=True)
    ctx.run(
        ["typst", "compile", "main.typ", str(output_dir / "main.pdf")],
        cwd=root / "packages" / "typst",
    )
