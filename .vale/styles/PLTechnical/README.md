# PLTechnical Vale rules

These five rule files were copied from the user-supplied Vale preset archive. Their intended scope, provenance, and limitations are specified in [`SPEC-EDIT`](../../../backlog/docs/doc-7%20-%20SPEC-EDIT-%E2%80%94-Editorial-quality-and-Vale.md).

Vale is provided by the root Pixi Conda environment. From the repository root:

```sh
pixi install --locked
pixi run --locked lint-vale
pixi run --locked vale-demo
```

The rules are local under `.vale/styles/`; `vale sync` is not required. `vale-demo` emits intentional findings as JSON with `--no-exit` for inspection. Review every suggestion manually; it is not an automated rewriting instruction. Public redistribution remains gated on license/provenance review.
