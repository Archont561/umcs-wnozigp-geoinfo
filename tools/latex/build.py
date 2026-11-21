"""Build the placeholder LaTeX main document for a smoke test."""

from __future__ import annotations

from pathlib import Path

from tasknest import ToolContext, tool


@tool(
    description="Compile the LaTeX dummy main with the root-pinned Tectonic executable.",
    inputs=["packages/latex/main.tex", "tools/latex/build.py"],
    outputs=["dist/latex/main.pdf"],
)
def build(ctx: ToolContext) -> None:
    """Compile packages/latex/main.tex to dist/latex/main.pdf."""
    root = Path(__file__).resolve().parents[2]
    output_dir = root / "dist" / "latex"
    output_dir.mkdir(parents=True, exist_ok=True)
    ctx.run(
        ["tectonic", "--outdir", str(output_dir), "main.tex"],
        cwd=root / "packages" / "latex",
    )
