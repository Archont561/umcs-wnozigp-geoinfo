"""Build the Typst demo thesis, which imports the package in lib.typ."""

from __future__ import annotations

import os
from pathlib import Path

from tasknest import ToolContext, tool


@tool(
    description="Compile the Typst demo thesis against lib.typ with the root-pinned Typst executable.",
    inputs=[
        "packages/typst/main.typ",
        "packages/typst/lib.typ",
        "packages/typst/typst.toml",
        "packages/typst/assets/umcs-logo.png",
        "tools/typst/build.py",
    ],
    outputs=["dist/typst/main.pdf"],
)
def build(ctx: ToolContext) -> None:
    """Compile packages/typst/main.typ to dist/typst/main.pdf."""
    root = Path(__file__).resolve().parents[2]
    output_dir = root / "dist" / "typst"
    output_dir.mkdir(parents=True, exist_ok=True)
    # Typst finds no font the environment ships unless it is told where to look.
    # Without this the cover's sans face silently falls back to a serif and the
    # measured geometry drifts, so the path is set here rather than left to
    # whoever runs the command.
    env = dict(os.environ)
    env["TYPST_FONT_PATHS"] = str(root / ".pixi" / "envs" / "default" / "fonts")
    ctx.run(
        ["typst", "compile", "main.typ", str(output_dir / "main.pdf")],
        cwd=root / "packages" / "typst",
        env=env,
    )
