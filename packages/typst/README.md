# Typst package

An **unofficial** Typst package for UMCS WNoZiGP Geoinformatics theses. It implements the contract in [`SPEC-TYP`](../../backlog/docs/doc-5%20-%20SPEC-TYP-%E2%80%94-Typst-package-contract.md) against the evidence ledger in [`SPEC-SOURCE`](../../backlog/docs/doc-3%20-%20SPEC-SOURCE-%E2%80%94-Source-evidence-and-requirements-traceability.md).

> **This is a prototype, not an approved thesis format.** No faculty, supervisor, or student reviewer has signed it (ADR-9). It targets the 2026/27 cohort using the 2025/26 rules as a proxy (ADR-10), so check the current official document before relying on any output.

## Usage

```typ
#import "@preview/umcs-wnozigp-thesis:0.1.0": *

#let meta = (
  programme: "Geoinformatyka",
  specialisation: "Systemy informacji geograficznej",
  author: "Imię Nazwisko",
  album: "102030",
  title: "Tytuł pracy",
  title-en: "Thesis title",
  supervisor: "dr hab. Imię Nazwisko",
  department: "Katedra Geoinformacji i Kartografii",
  city: "Lublin",
  year: "2027",
)

#show: umcs-thesis.with(cycle: "magisterska", meta: meta)

#coverpage(meta, "magisterska")
#pagebreak()
#contents()
```

Then write chapters with `= Chapter` and `== Section`. Illustrations use the wrappers, which enforce the source line the faculty requires:

```typ
#figure-with-source(caption: [Schemat], source: own-work("dane własne"))[
  #image("figure.png")
]

#table-with-source(caption: [Zestawienie], source: [opracowanie własne])[
  #table(columns: 2, [a], [b])
]

#listing(caption: [Obliczenie wskaźnika], source: own-work("skrypt własny"))[
  #raw(lang: "python", block: true, "delta = (a2 - a1) / a1 * 100")
]
```

A photograph is inserted as an ordinary figure: `figure-with-source(caption: [...], source: [...])[#image("photo.jpg")]`.

## API

| Function | Purpose | Source |
| --- | --- | --- |
| `umcs-thesis(cycle:, meta:, language:, font:)` | the `show` rule: page, fonts, spacing, headings | SRC-001–SRC-008 |
| `coverpage(meta, cycle)` | title page, no page number | SRC-012, SRC-045 |
| `contents()` | contents from the same counter as the body | SRC-013 |
| `abstract(body, limit: 4000)` | abstract with the character limit enforced | SRC-014 |
| `figure-with-source(body, source:, caption:)` | figure, caption below, source below. Photographs use this too | SRC-018–SRC-022 |
| `table-with-source(body, source:, caption:)` | table, title above, source below | SRC-015, SRC-016 |
| `listing(body, source:, caption:)` | listing, caption above, source below, own counter | SRC-021, SRC-023 |
| `list-of-figures()` / `list-of-tables()` / `list-of-listings()` | per-type indexes | SRC-023 |
| `appendix(body, title:)` / `appendices(body)` | annex pages, "Załącznik N" in the page header | SRC-024 |
| `annex-ref(n)` | renders "Załącznik n"; not a live cross-reference | SRC-024 |
| `equation-numbered(body)` | equation numbered `(2.1.)` per chapter | SRC-026 |
| `front-matter-heading(text)` | unnumbered heading that does not consume a chapter number | SRC-010 |
| `own-work(base)` / `after(work)` | attribution strings | SRC-020, SRC-047 |

`cycle` is required and has no default; unknown `meta` keys are rejected with an error naming the key; `title-en` is required.

## Four deliberate limitations

These are decisions, not oversights. Each is recorded in the specification.

1. **Photographs have no separate class, and two indexes are absent.** The faculty document names three illustration classes — tables, figures and *photographs* — and asks for a "Spis fotografii" and a "Spis załączników". By owner decision (ADR-17) the package keeps **Rycina, Tabela and Listing**, folds photographs into figures, and ships **neither** of those two indexes. A student comparing this output with the guidelines will find those three differences.
2. **The font is a substitute.** Times New Roman is proprietary and cannot ship here (TYP-006). The default is `"New Computer Modern"`. Set `font: "Times New Roman"` if you have it installed; **no build of this package claims SRC-002 compliance on the substitute.**
3. **Some spacing is approximated.** The source says "two line spaces" and "1.5 lines above", not a measurable unit. Those values are marked `APPROXIMATED` in `lib.typ` and are the first things to check against a printed copy of the guidelines.
4. **`annex-ref` is not a live reference.** Typst refuses to reference a label applied to a multi-element function result, and every single-element wrapper either floated the content or rejected the page break. `annex-ref(n)` therefore renders the right text but does not renumber itself when annexes are reordered. The "Załącznik N" label itself is in the page header, top right, as the faculty asks.

## Not published

There is a `typst.toml`, but the package is **not on Typst Universe**. Registry publication needs an owner account and a namespace decision, and the name would have to be unambiguous about the package not being faculty-approved. Until then, consume it locally:

```sh
typst compile --package-path ./preview my-thesis.typ
```

with the package extracted to `preview/preview/umcs-wnozigp-thesis/0.1.0/`. That layout is measured, not assumed: a `preview/` directory is required even for the `@preview` namespace, and an `@local` namespace is rejected.

## Build and check

From the repository root:

```sh
pixi run --locked build-typst    # writes dist/typst/main.pdf
pixi run --locked lint-typst     # typstyle --check
pixi run --locked test-smoke     # 8 BDD scenarios for this package
```

`main.typ` is a **fixture**, not part of the deliverable: it is excluded from the release tarball, which ships only `lib.typ`, `typst.toml`, `README.md` and `LICENSE`.

## Licence

This package is released under the [MIT License](LICENSE), copyright (c) 2026 Archont561 — the same terms as the repository root (ADR-14). It covers this directory's original work only. It does not extend to institutional marks, fonts, or third-party dependencies, and none are bundled.
