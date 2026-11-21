---
id: doc-4
title: SPEC-LTX — LaTeX package contract
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-LTX — LaTeX package contract

**Status:** Draft (contract proposed, not implemented)  
**Version:** 0.2  
**Related tasks:** TASK-4, TASK-8, TASK-9  
**Related evidence:** SPEC-SOURCE v0.3 (SRC-001..SRC-044)  
**Related decisions:** ADR-1, ADR-2, ADR-9, ADR-10, ADR-11  
**Milestone:** M-1, M-2

## Purpose

Pin the public interface of the future LaTeX deliverable before any of it is written, so that implementation (TASK-9) is a matter of filling in a contract rather than discovering one. Every normative statement here cites a SPEC-SOURCE record; nothing is asserted that the evidence does not support.

## Current scaffold

`packages/latex/main.tex` is a minimal compileable dummy. No `.cls` or `.sty` file exists, and no API is implemented. The dummy must not be copied into an academic submission as a template or a compliance example.

## Package form

**A single document class, `umcswnozigp.cls`** (ADR-11), not a style package and not a bundle of components.

Rationale: the rules constrain the document as a whole — page geometry (`SRC-001`–`SRC-003`), body and heading typography (`SRC-002`, `SRC-004`–`SRC-006`), paragraph form (`SRC-007`), page numbering (`SRC-008`), front-matter order (`SRC-010`), title-page fields (`SRC-012`), and caption geometry (`SRC-015`–`SRC-019`). Those are class-level decisions; a package layered over `report` would fight its defaults instead of defining them.

A component split stays possible later as internal files loaded by the class (`\input`/`\RequirePackage`), but the *public* surface is one class and one options list.

## Public API

### Loading

```latex
\documentclass[
  cycle = magisterska,   % licencjacka | inzynierska | magisterska
  language = pl,         % pl (default) | en
  spacing = onehalf,     % onehalf (default, SRC-002)
  draft = false          % draft adds a watermark and is never submittable
]{umcswnozigp}
```

| Option | Values | Default | Source |
| --- | --- | --- | --- |
| `cycle` | `licencjacka`, `inzynierska`, `magisterska` | required, no default | `SRC-010` (thesis types) |
| `language` | `pl`, `en` | `pl` | `SRC-037` (Polish default, foreign language only with approval) |
| `spacing` | `onehalf` | `onehalf` | `SRC-002` (1.5 line spacing) |
| `draft` | `true`, `false` | `false` | maintainer choice, not institutional |

Missing `cycle` is a hard error rather than a silently chosen default, because the three thesis types carry different structural expectations.

### Metadata

One key-value command, mapping onto the title-page fields in `SRC-012`:

```latex
\umcssetup{
  programme      = {Geoinformatyka},
  specialisation = {Geoinformatyka stosowana},   % omit if not applicable
  author         = {Imię Nazwisko},
  album          = {102030},
  title          = {Tytuł pracy w języku polskim},
  title-en       = {Thesis title in English},
  supervisor     = {dr hab. Imię Nazwisko},
  department     = {Katedra Geoinformacji},
  city           = {Lublin},
  year           = {2027},
}
```

- `title` and `title-en` are both required: `SRC-012` mandates the title in Polish **and** English.
- `department` maps to the source's "napisana w Katedrze (nazwa Katedry)" in the 2025/26 Annex 1 sample (SRC-045). The superseded 2017 edition used "Zakład", so the label is `Katedra` for the current edition.
- The university, faculty and programme name are fixed by the class; overriding them is not offered.
- Unknown keys raise an error. A missing required key raises an error at `\makecoverpage`, not at load time, so drafting can proceed.

### Document structure

The class supplies the order in `SRC-010`; the author calls the parts in sequence:

```latex
\begin{document}
\makecoverpage        % normalised title page, no page number (SRC-008, SRC-012)
\tableofcontents      % arabic numerals, matching body numbering (SRC-013)
\abstract{...}        % enforces the 4000-character limit (SRC-014)
\chapter{Wstęp}
...
\bibliography{refs}   % behaviour delegated to SPEC-BIB
\listoftables
\listoffigures
\listofphotographs
\listofappendices
\appendices
...
\end{document}
```

| Command | Behaviour | Source |
| --- | --- | --- |
| `\makecoverpage` | Emits the normalised title page; suppresses the page number | `SRC-008`, `SRC-012` |
| `\abstract{text}` | Type-sets the abstract; warns above 4000 characters, errors above 4500 | `SRC-014` |
| `\appendices` | Switches annex numbering to `Załącznik N` in the top-right corner | `SRC-024` |
| `\listofphotographs` | Separate photograph index, distinct from figures | `SRC-023` |
| `\figsource{...}`, `\tabsource{...}` | Emit the italic 10 pt source line under the object | `SRC-016`, `SRC-019` |

`\figsource` and `\tabsource` are explicit commands rather than an optional-argument convention because `SRC-022` requires a source for *every* illustration. Making the source a separate, greppable command lets a test assert that each float has one.

### Floats and numbering

- `table`, `figure` and `photograph` environments, each with an independent counter (`SRC-021`), matching the source's separate *Spis tabel / rycin / fotografii*.
- Caption placement is fixed by the class, not the author: table titles above (`SRC-015`), figure and photograph titles below (`SRC-018`).
- Caption typography is fixed: Times-compatible 10 pt bold, single spacing, 1.5-line space before (`SRC-015`, `SRC-018`).
- A photograph environment exists because the source treats photographs as a third illustration class; mapping them onto `figure` would collapse two indexes into one.
- No scale check is possible automatically. `SRC-019` requires a scale on every map, so the class documents the obligation and TASK-12 reviews it visually.

### Equations

`SRC-026` fixes numbering as per-chapter with a trailing period inside the parentheses — `(2.1.)`. The class defines:

```latex
\theequation          % -> 2.1.  (chapter.number.)
```

and sets equations in a two-column layout with a 2 cm right column, per `SRC-026`. Whether the trailing period is reproduced inside the parentheses is a formatting detail the source states explicitly, so it is reproduced rather than normalised away.

### Language

Polish is the default (`SRC-037`). A foreign-language thesis requires approval and then needs the title, figure and table captions, and the abstract translated into Polish. The class therefore does **not** offer a "just switch `language=en`" path: `language=en` sets English labels, and the contract records that a compliant English thesis still needs the Polish title and abstract supplied separately. That obligation is documented, not automated.

## Engine matrix

`SRC-002` requires Times New Roman. That single requirement splits the engines, because Times New Roman is a proprietary font:

| Engine | Status | Times handling | Evidence |
| --- | --- | --- | --- |
| Tectonic (XeTeX) | **Smoke-tested only** | Requires a font or a Times-compatible substitute; Tectonic compiles the dummy with `report`, not the class | ADR-8, CI `smoke` job |
| XeLaTeX | Candidate | Can use Times New Roman if the font is installed; otherwise a metric-compatible substitute | Not tested |
| LuaLaTeX | Candidate | Same as XeLaTeX | Not tested |
| pdfLaTeX | Candidate, constrained | Cannot use system fonts; needs a Times clone such as `newtxtext`/`mathptmx` | Not tested |

**No engine is claimed as supported.** The only executed engine is Tectonic, and only against the dummy main; that establishes the build pipeline (ADR-8), not class compatibility. Engine support becomes a claim only when TASK-8's matrix runs the class itself on each engine and records the result.

The font question is an open decision, not a detail: shipping a Times clone changes glyph metrics versus true Times New Roman, and bundling the proprietary font is not an option. Recorded as open question 1.

## Editor compatibility

**No editor compatibility claim is made** (TASK-4 criterion 3, satisfied by declining). Overleaf has not been tested, and the class does not exist to test. The contract states what a future test would have to show: a clean import with no shell escape, no local font dependency, and a build within the free-tier timeout. Until that runs, no README, specification, or release note may describe the deliverable as Overleaf-compatible.

## Dependencies

`LTX-002` requires an inventory. The policy:

1. Prefer the LaTeX kernel and packages shipped with a current TeX Live.
2. Every non-kernel dependency is listed with a minimum version and engine notes before first use.
3. No dependency is added for a rule that can be satisfied in ten lines of class code.
4. No bundled fonts, institutional marks, or seals without documented permission (`SRC-041` remains unobtained).
5. Each dependency's licence is recorded; a dependency with unclear terms blocks inclusion.

Anticipated dependencies, all unconfirmed until TASK-9:

| Need | Package | Status |
| --- | --- | --- |
| Geometry (`SRC-003`) | `geometry` | kernel-adjacent, expected |
| Caption typography (`SRC-015`, `SRC-018`) | `caption` | expected |
| Polish labels (`SRC-037`) | `babel` (pdfLaTeX) or `polyglossia` (Xe/Lua) | engine-dependent, open |
| Times-compatible text (`SRC-002`) | `newtxtext` or fontspec + system font | open, see font question |
| Table and figure indexes (`SRC-023`) | kernel `\listof...` extensions | expected |

## Fixture and package separation

`LTX-003` requires fixtures to stay out of the distributable files.

| Path | Role | Distributed |
| --- | --- | --- |
| `packages/latex/umcswnozigp.cls` | the deliverable | yes |
| `packages/latex/README.md` | package documentation | yes |
| `packages/latex/main.tex` | smoke fixture, currently the dummy | no |
| `packages/latex/tests/` | BDD and compile fixtures | no (kept in-repo, excluded from archives) |
| `packages/latex/examples/` | short usage examples | optional, decided in TASK-9 |

The release workflow currently archives the whole `packages/latex/` directory, so this separation is **not yet enforced**; TASK-9 must adjust the archive step or the layout before release.

## Requirements

- **LTX-001:** A future package shall expose a documented entry point and stable configuration interface.
- **LTX-002:** Every non-standard dependency shall be inventoried with supported version and engine notes.
- **LTX-003:** Test fixtures shall remain separate from the distributable package files.
- **LTX-004:** The supported engine/editor matrix shall be evidence-backed and tested independently.
- **LTX-005:** Rendered output shall be checked against accepted source requirements; a successful compile alone is insufficient.
- **LTX-006:** The title page shall be emitted by one command from a single key-value metadata block, so `SRC-012`'s field list is enforced in one place.
- **LTX-007:** Every float shall require an explicit source command, so `SRC-022` can be asserted by a test rather than by review alone.
- **LTX-008:** The abstract command shall enforce the character limit in `SRC-014` at compile time.
- **LTX-009:** No editor or engine shall be described as supported without a recorded test run against the class.

## Test plan (LaTeX side)

TASK-8 owns the full matrix; this is the LaTeX contribution.

| Level | What it does | Status |
| --- | --- | --- |
| Compile | Tectonic builds the dummy in CI | Implemented (ADR-8) |
| Compile the class | Build a fixture using `umcswnozigp.cls` on each candidate engine | Not implemented |
| Assertion | `\typeout` the computed values (`\theequation`, `\textwidth`, page style) and grep the log | Not implemented; feasible without a PDF diff |
| Source coverage | Grep fixtures for `\figsource`/`\tabsource` per float | Not implemented |
| Visual | Human review against `SRC-004`–`SRC-021` | Manual, TASK-12 |

The assertion level is the useful one: `geometry` values, `\theequation`, and caption placement can be checked mechanically in the log, which turns several of these rules into tests instead of review checklist items.

## Open questions

1. **Font substitution.** Times New Roman is proprietary. Is a metric-compatible clone (`newtxtext`) acceptable for a submission, or must the class require the real font and fail loudly when it is absent? This affects every engine except a system that has the font installed.
2. **Engine priority.** Which engine becomes the single supported target, and are the others best-effort or explicitly unsupported?
3. **Bilingual titles.** `SRC-012` requires both titles. Should `title-en` be mandatory for a Polish-language thesis, or default to an empty placeholder?
4. **Annexes 1–5.** The title-page and contents samples are embedded in the faculty PDF and are now recorded as SRC-045/SRC-046, so `\makecoverpage` and the contents style have a documented target. No separate editable template file was found, and the samples are reproduced in prose rather than measured, so exact spacing still needs the source PDF itself.
5. **Photograph counter.** Is a third float class the right model, or does the faculty accept photographs under the figure index?
6. **AI disclosure — decided, no.** The class offers no declaration environment (ADR-15). The faculty AI policy is out of scope, so there is no wording to implement and inventing one would fabricate institutional text.

## Acceptance evidence

Before this specification is Approved, record: the implemented API, the engine matrix results, dependency versions and licences, a clean build procedure, output review against `SRC-001`–`SRC-026`, and the user-facing limitations. TASK-4 records the contract; TASK-8 and TASK-9 supply the evidence.
