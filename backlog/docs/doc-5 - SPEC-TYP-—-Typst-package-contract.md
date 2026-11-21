---
id: doc-5
title: SPEC-TYP — Typst package contract
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-TYP — Typst package contract

**Status:** Draft (contract proposed, not implemented)  
**Version:** 0.2  
**Related tasks:** TASK-5, TASK-8, TASK-10  
**Related evidence:** SPEC-SOURCE v0.3 (SRC-001..SRC-044)  
**Related decisions:** ADR-2, ADR-9, ADR-10, ADR-12  
**Milestone:** M-1, M-2

## Purpose

Pin the public interface of the future Typst deliverable before any of it exists, mirroring SPEC-LTX's approach so the two formats stay independent (SCOPE-001) while sharing one evidence base.

## Current scaffold

`packages/typst/main.typ` is a minimal compileable dummy. No `lib.typ`, no `typst.toml` manifest, and no registry entry exist. The dummy compiles to a valid PDF in CI, which proves the pipeline only (ADR-8).

## Package shape

**A template package with a single entry point**, `lib.typ`, exporting one `show`-style function that takes a content body plus a configuration dictionary.

```typst
#import "@local/umcswnozigp:0.1.0": umcs-thesis

#show: umcs-thesis.with(
  cycle: "magisterska",   // licencjacka | inzynierska | magisterska
  language: "pl",         // pl (default) | en
  meta: (
    programme: "Geoinformatyka",
    author: "Imię Nazwisko",
    album: "102030",
    title: "Tytuł pracy",
    "title-en": "Thesis title",
    supervisor: "dr hab. Imię Nazwisko",
    department: "Katedra Geoinformacji",
    city: "Lublin",
    year: "2027",
  ),
)
```

| Element | Rule | Source |
| --- | --- | --- |
| `cycle` required, no default | Three thesis types differ structurally | `SRC-010` |
| `meta.title` and `meta.title-en` both required | Title in Polish **and** English | `SRC-012` |
| Unknown `meta` keys raise an error | Same strictness as the LaTeX class | maintainer choice, ADR-11 parity |
| University and faculty name fixed | Not overridable | `SRC-012` |

Using a dictionary rather than positional arguments keeps the API stable as fields are added, and mirrors `\umcssetup` in the LaTeX class so a student switching formats does not relearn the field set.

## Public API surface

| Function / element | Behaviour | Source |
| --- | --- | --- |
| `umcs-thesis(...)` | The `show` rule: geometry, fonts, headings, page numbering | `SRC-001`–`SRC-008` |
| `coverpage(...)` | Normalised title page, no page number | `SRC-008`, `SRC-012` |
| `abstract(body)` | Abstract with the 4000-character limit enforced | `SRC-014` |
| `figure-with-source(...)` | Figure plus required source line below | `SRC-018`, `SRC-019`, `SRC-022` |
| `table-with-source(...)` | Table title above, source below | `SRC-015`, `SRC-016` |
| `photograph(...)` | Third illustration class with its own counter | `SRC-021`, `SRC-023` |
| `appendices(body)` | `Załącznik N`, top right | `SRC-024` |
| `list-of-photographs` | Separate photograph index | `SRC-023` |

Typst has no `\listoffigures` equivalent that distinguishes three counters, so the package must maintain table, figure and photograph counters itself. That is the largest implementation risk in this contract and is called out for TASK-10.

## Language and fonts

- Default language `pl` (`SRC-037`); Polish hyphenation and label strings are package data, not a dependency.
- **Times New Roman is the required body face (`SRC-002`) and is proprietary.** Typst cannot use a font that is not installed, and the repository bundles none. The package therefore takes a `font` parameter defaulting to `"New Computer Modern"` (Typst's built-in serif) and documents that a submission must set `font: "Times New Roman"` where that font exists. This is a documented substitution, not silent compliance.
- Verified in this environment: the root Pixi environment ships 31 font files and **none of them is Times or a Times metric clone**, so a faithful build cannot be produced locally. Recorded as open question 1.

## Compiler version

Two distinct facts, kept apart per TASK-5 criterion 2:

| Fact | Value |
| --- | --- |
| Version tested in this repository | **0.15.1** (`typst 0.15.1 (6734eafd)`), pinned in `pixi.toml` |
| Future minimum supported version | **Undecided**; must be set when the package is implemented and its feature use is known |

The dummy compiling on 0.15.1 says nothing about the package's minimum, because the package does not exist. Recording a minimum now would be a guess.

## Bibliography

Delegated to SPEC-BIB. The package accepts a `bibliography` path and passes a style file; it does not implement citation formatting. Verified behaviour in this environment:

- Hayagriva YAML compiles and `#cite` resolves.
- A **custom CSL file is loaded from disk** and changes rendered output; a missing file fails with `file not found`, so a style error is loud rather than silent.
- Built-in CSL styles need no network.
- `type: webpage` is rejected by Hayagriva; the accepted value is `web`. Schema details matter and are recorded in SPEC-BIB.

## Editor and distribution

- **No editor compatibility claim.** No Overleaf test exists for Typst and none is made (ADR-11 parity).
- **No registry submission.** No `typst.toml` manifest is present, and Typst Universe naming is not decided (ADR-12). The package is addressed as `@local/umcswnozigp` in examples until the owner chooses a distribution channel.
- A local-package workflow (`--package-path`) is the assumed development path; it is untested here and recorded as such.

## Fixture and package separation

| Path | Role | Distributed |
| --- | --- | --- |
| `packages/typst/lib.typ` | the deliverable | yes |
| `packages/typst/typst.toml` | manifest, when registry naming is decided | yes |
| `packages/typst/README.md` | package documentation | yes |
| `packages/typst/main.typ` | smoke fixture, currently the dummy | no |
| `packages/typst/tests/` | BDD and compile fixtures | no |

As with LaTeX, the release archive currently ships the whole `packages/typst/` directory, so this separation is **not yet enforced**.

## Requirements

- **TYP-001:** The package shall expose one documented entry point taking a configuration dictionary, and shall reject unknown keys.
- **TYP-002:** The package shall not require network access at build time; any style file it uses ships in the repository.
- **TYP-003:** Any imported third-party package shall have a dependency and licence record.
- **TYP-004:** Test fixtures shall remain separate from the distributable package files.
- **TYP-005:** The minimum supported compiler version shall be stated only after the package's feature use is known, and shall then be tested.
- **TYP-006:** A font substitution shall be documented wherever the default face is not Times New Roman, and no build shall claim `SRC-002` compliance on a substitute.
- **TYP-007:** Table, figure and photograph counters shall be independent, matching `SRC-021`.

## Test plan

| Level | What it does | Status |
| --- | --- | --- |
| Compile the dummy | Typst builds `main.typ` in CI | Implemented (ADR-8) |
| Compile the package | Build a fixture importing `lib.typ` | Not implemented |
| Counter assertions | Query the document and assert three independent counters | Feasible: `typst query` works here |
| Source coverage | Query for figures lacking a source element | Feasible once the API exists |
| Visual | Human review against `SRC-004`–`SRC-021` | Manual, TASK-12 |

`typst query` is the leverage point: a custom `figure-with-source` element can be labelled and queried, turning `SRC-022` into an assertion instead of a reviewer's checklist.

## Open questions

1. **Font.** Times New Roman is proprietary and absent from this environment. Require the real font and fail loudly, or document a substitute and accept metric drift?
2. **Registry.** Typst Universe publication needs an owner account, a package name, and a licence decision (ADR-12). None is decided.
3. **Minimum compiler version.** Only decidable once the package exists.
4. **Three illustration counters.** Typst does not provide this out of the box; confirm the counter model matches faculty practice, or collapse photographs into figures if the faculty does.
5. **Annexes 1–5.** `SRC-041`: the normative layouts are still unobtained, so `coverpage` cannot be called correct.
6. **Parity scope.** The two formats share an evidence base but not an implementation. Must their rendered output match, or is parity a documentation concern only (BIB-004)?

## Acceptance evidence

Before Approval: implemented entry point, compiler version actually tested, dependency and licence records, a clean offline build, output review against `SRC-001`–`SRC-026`, and recorded limitations. TASK-5 records the contract; TASK-8 and TASK-10 supply the evidence.
