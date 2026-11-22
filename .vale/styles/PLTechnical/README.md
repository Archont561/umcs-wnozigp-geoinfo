# PLTechnical Vale rules

These five rule files came from the user-supplied Vale preset archive. Their intended scope, provenance, and limitations are specified in [`SPEC-EDIT`](../../../backlog/docs/doc-7%20-%20SPEC-EDIT-%E2%80%94-Editorial-quality-and-Vale.md).

Vale is provided by the root Pixi Conda environment. From the repository root:

```sh
pixi install --locked
pixi run --locked lint-vale
pixi run --locked vale-demo
```

The rules are local under `.vale/styles/`; `vale sync` is not required. `vale-demo` emits intentional findings as JSON with `--no-exit` for inspection. Review every suggestion manually; it is not an automated rewriting instruction.

## Provenance

These five rule files are **written for this repository** and derive from the
Polish plain-language guidance published on `gov.pl` (Ministry of Digital
Affairs, Civil Service, accessibility and editorial pages — listed in
[`SPEC-EDIT`](../../../backlog/docs/doc-7%20-%20SPEC-EDIT-%E2%80%94-Editorial-quality-and-Vale.md)).
**That guidance is the only source**: nothing here comes from another style
guide, another Vale style, or a third party's checklist. The author confirmed on
2026-11-22 that the rules were written by them from it, which is what lets MIT
cover the files while the guidance stays a citation.
They are not an official artefact of any ministry: the guidance says nothing
about Vale, the tokens and patterns are ours, and the rule messages are our own
sentences. They are MIT-licensed with the rest of the repository.

The guidance is written for administrative correspondence to the public, and
this preset lints technical and academic prose, so several rules are
deliberately weaker than it advises — passive voice and verbal nouns as a class
are not checked, and sentence length is 30 tokens rather than 15–20.
`UnitSpacing` has no basis in the guidance at all; it is a local editorial
convention. SPEC-EDIT records each departure and why.
