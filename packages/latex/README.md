# LaTeX scaffold

This directory currently contains only `main.tex`, a compileable placeholder. It is not a thesis template, does not implement the faculty guidance, and must not be used as an approved academic format.

The intended package contract is specified in [`SPEC-LTX`](../../backlog/docs/doc-4%20-%20SPEC-LTX-%E2%80%94-LaTeX-package-contract.md). Engine support, Overleaf behavior, class/style API, and bibliography tooling remain undecided. The root Pixi environment currently uses Tectonic for a smoke build and ChkTeX for a basic source lint; neither proves compatibility with pdfLaTeX, LuaLaTeX, XeLaTeX, or Overleaf.

## Licence

This package is released under the [MIT License](LICENSE), copyright (c) 2026 Archont561 — the same terms as the repository root. The licence ships inside every release tarball (ADR-14). It covers this directory's original work only: it does not extend to institutional marks, fonts, or third-party dependencies, and none are bundled.

From the repository root:

```sh
pixi run --locked lint-latex
pixi run --locked build-latex
```

The package-local pytest-bdd smoke scenario is in `tests/`; it builds this dummy and checks PDF framing, not template compliance. The build writes `dist/latex/main.pdf`. It is a dummy PDF for pipeline verification only.
