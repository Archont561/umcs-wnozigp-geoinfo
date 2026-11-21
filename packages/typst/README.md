# Typst scaffold

This directory currently contains only `main.typ`, a compileable placeholder. It is not a thesis template, does not implement the faculty guidance, and must not be used as an approved academic format.

The intended package contract is specified in [`SPEC-TYP`](../../backlog/docs/doc-5%20-%20SPEC-TYP-%E2%80%94-Typst-package-contract.md). The minimum compiler version, public API, package namespace, and registry policy remain undecided. The root Pixi environment uses Typst for a smoke build and Typstyle for a basic formatter check; neither proves institutional compliance or editor compatibility.

From the repository root:

```sh
pixi run --locked lint-typst
pixi run --locked build-typst
```

The package-local pytest-bdd smoke scenario is in `tests/`; it builds this dummy and checks PDF framing, not template compliance. The build writes `dist/typst/main.pdf`. It is a dummy PDF for pipeline verification only.
