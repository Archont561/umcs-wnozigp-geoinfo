---
id: ADR-12
status: accepted
date: 2026-11-21
---

# ADR-12: Repository-owned bibliography styles, one per format

## Context

The faculty rules do not name a citation standard. They prescribe an entry syntax — `Surname B., 2003. Title. Publisher, Place.` — with the year after the author and a period, the title italicised, and journal entries punctuated as `volume, issue, pages`. They also fix in-text forms: `i in.` for three or more authors, `za:` for secondary quotation, and `1999a`/`1999b` for same-year works (SRC-027–SRC-036).

No stock citation style produces that shape. Author-year styles such as APA and Harvard parenthesise the year; numeric styles lose the author-first ordering the faculty requires.

Testing in this repository confirmed the tooling: Hayagriva YAML compiles under Typst 0.15.1, `#cite` resolves, a custom CSL file loads from disk and changes rendered output, built-in CSL styles work offline, and `biber` is absent from the Pixi environment.

## Decision

1. Drive formatting from **repository-owned style files**, not a third-party style:
   - LaTeX: a `.bbx`/`.cbx` pair for BibLaTeX.
   - Typst: a CSL file for Hayagriva.
2. Ship those files in the repository so every build is offline and no style download is required (BIB-006).
3. Accept that the two formats use **different machinery** and may not render identically. Parity is a documentation concern, not a requirement (BIB-004).
4. Do not add bibliography commands to either `main` file until the style files exist and render correctly.
5. Keep sample references synthetic or public-domain (BIB-005); the faculty document's examples are placeholders and must not be treated as real publications.

## Consequences

- A future student gets the faculty's format without knowing CSL or BibLaTeX, because the style ships with the package.
- The repository now owns two non-trivial style files that must be maintained, and a faculty rule change means editing both.
- BibLaTeX/Biber is the LaTeX choice, but **Biber is not currently installed** in the Pixi environment. Implementation of TASK-11 is blocked until the dependency question in SPEC-BIB is answered.
- Cross-format rendering differences are expected and must be documented rather than papered over; a test that compares the two outputs would encode a false guarantee.
