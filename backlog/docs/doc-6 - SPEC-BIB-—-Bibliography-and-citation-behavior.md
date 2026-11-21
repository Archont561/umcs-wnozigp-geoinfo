---
id: doc-6
title: SPEC-BIB — Bibliography and citation behavior
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-BIB — Bibliography and citation behavior

**Status:** Draft (approach selected, not implemented)  
**Version:** 0.2  
**Related tasks:** TASK-6, TASK-8, TASK-11  
**Related evidence:** SPEC-SOURCE v0.3 (SRC-027..SRC-036)  
**Related decisions:** ADR-12  
**Milestone:** M-1, M-3

## Purpose

Define a citation and bibliography workflow that satisfies the faculty's actual rules without assuming BibLaTeX, Biber, or cross-format parity is required.

## What the faculty prescribes

This is the decisive point: the faculty does **not** name a citation standard. It prescribes a **concrete entry syntax and in-text convention**, which is stricter than "any style" and weaker than "use APA".

| Rule | Requirement | Source |
| --- | --- | --- |
| Direct quotation | Quotation marks, author + year + page, max 50 words | `SRC-027` |
| Paraphrase | Author + year, no page; several authors in chronological order | `SRC-028` |
| Two authors | Both names | `SRC-029` |
| Three or more authors | First name + `i in.` | `SRC-029` |
| Edited volume | Editor + `[red.]` + year | `SRC-030` |
| Secondary quotation | `(Hart 1995, za: Parnicki 2006)` | `SRC-031` |
| Same author, same year | Letter suffix: `1999a`, `1999b` | `SRC-032` |
| Web sources in text | Only the first five URL elements | `SRC-033` |
| Bibliography order | Alphabetical by surname; *netografia* separate with access dates | `SRC-034` |
| Entry syntax | Surname + initial, year, italic title, publisher, place; chapters add page range; articles add volume, issue, pages | `SRC-035` |
| Anonymous works | Title-first pattern for atlases, yearbooks | `SRC-036` |

Canonical entry shapes from the source (Polish title italicised, not the publisher):

```text
Żarska B., 2003. Ochrona krajobrazu. Wydawnictwa SGGW, Warszawa.
Matykowski R., 1988. Badania struktury... W: T. Czyż (red.), Problemy... Wydawnictwo Naukowe UAM, Poznań: 128–156.
Kondracki J., 1960. Tymczasowy wynik... Czasopismo Geograficzne, 17, 3, 296–298.
Regionalny Atlas Polski dla gimnazjum, 2000, PPWK, Warszawa.
www.mojairlandia.pl/muzyka/muzyka (12.12.2012)
```

Notes that matter and are easy to get wrong:

- The year follows the author with a **period**, not parentheses — this alone rules out most author-year CSL styles such as APA or Harvard.
- The **title is italic**, the publisher is not.
- Journal entries use `volume, issue, pages` with no punctuation labels.
- Web entries put the date in parentheses at the end, and the in-text form truncates the URL.

## Copyright conflict, recorded rather than resolved

`SRC-028` shows a nested citation rendered as "(Hart 1995, za: Parnicki 2006)". The natural reading is that Hart's work is cited *through* Parnicki's — but reproducing it in citable form would require naming a real secondary work whose details are not supplied. **These are synthetic placeholders from the faculty's own document, not verified publications.** They must not be used as real references, and a test fixture built from them must be labelled synthetic (`BIB-005`).

## Tool reality in this repository

Verified in the restored sandbox, not assumed:

| Tool | Present | Consequence |
| --- | --- | --- |
| `biber` | **No** | BibLaTeX/Biber cannot run in this environment today |
| `bibtex` | **No** | Classic BibTeX cannot run either |
| Tectonic | Yes | Embeds support for `tectonic-biber`, but Biber itself is absent from the Pixi environment |
| Typst 0.15.1 | Yes | Hayagriva YAML compiles; `#cite` resolves |
| Custom CSL file | **Yes, loads from disk** | A missing file fails loudly (`file not found`); a present file changes rendered output |
| Built-in CSL styles | Yes, offline | No network needed |

## Selected approach

**LaTeX:** BibLaTeX with **Biber**, formatting driven by a **repository-owned `.bbx`/`.cbx` pair** rather than an off-the-shelf style, because no stock style produces `Surname B., 2003. Title.` — they all place the year in parentheses or after a colon.

**Typst:** Hayagriva YAML with a **repository-owned CSL file**, which is confirmed to load from disk offline.

**Consequence, stated plainly:** the two formats satisfy the same rules through **different machinery**, and therefore may not render identically. `BIB-004` already forbids presuming parity, and ADR-12 records this as accepted.

## Dependency gap that blocks implementation

Biber is **not in the Pixi environment**. Choosing BibLaTeX/Biber therefore adds a dependency the repository does not currently install, while the release and CI paths must build it. Options, none yet decided:

1. Add `biber` to `pixi.toml` (Conda-forge provides it) and re-lock.
2. Use Tectonic's bundled Biber support, which still expects a `tectonic-biber` binary that is absent here.
3. Fall back to classic BibTeX with a hand-written `.bst`, which avoids Biber but constrains field handling and Unicode/diacritics.

This is recorded as open question 1 and as the reason TASK-11 cannot start yet.

## Behaviour to specify (TASK-6 criterion 3)

| Concern | Decision | Evidence |
| --- | --- | --- |
| Sorting | Alphabetical by surname, Polish collation | `SRC-034` |
| Language | Polish labels and connector words; English thesis still renders a Polish abstract | `SRC-037` |
| Diacritics | Must survive unchanged: `Ż`, `ń`, `ó`, `ł`, `ś`, `ż`, `ź`, `ć`, `ą`, `ę` | implied by `SRC-035` examples |
| Web sources | Separate *netografia* with access date; in-text truncation to five URL elements | `SRC-033`, `SRC-034` |
| Missing year | Print `b.r.` (bez roku), per SRC-048 — not `(n.d.)` or `[b.m.]` | `SRC-048` |
| Other missing fields | Omit the element; do not invent a placeholder the source does not use | maintainer choice, recorded |
| Page ranges | En dash in chapter entries (`128–156`), comma-separated volume/issue/pages for articles | `SRC-035` |
| Italics | Title only | `SRC-035` |

## Requirements

- **BIB-001:** Any supported citation workflow shall document adding a source, citing it, and generating the bibliography.
- **BIB-002:** Citation style and language behavior shall be reviewed against current faculty guidance.
- **BIB-003:** Tests shall cover representative books, articles, websites, Polish diacritics, and missing metadata.
- **BIB-004:** LaTeX and Typst behavior shall be tested separately; visual parity shall not be presumed.
- **BIB-005:** Sample references shall be synthetic or public-domain and contain no personal student data.
- **BIB-006:** The bibliography style files (`.bbx`/`.cbx` or CSL) shall live in the repository, so a build needs no network and no style download.
- **BIB-007:** A test shall assert the rendered ordering and the required punctuation of at least one book, one chapter, one article, and one web entry.
- **BIB-008:** The in-text citation forms in `SRC-027`–`SRC-033` shall be reproduced by test fixtures, including the `za:` and `1999a` cases.

## Decision gate

Approved in principle by ADR-12 (repository-owned styles, one per format). Implementation is blocked on the Biber dependency decision above. No bibliography commands or dependencies have been added to either `main` file, and neither format's main imports a style yet.

## Open questions

1. **Biber availability.** Add it to Pixi, rely on Tectonic's integration, or fall back to BibTeX?
2. **Style fidelity.** A hand-written `.bbx`/`.cbx` and a hand-written CSL are both non-trivial. Which subset of entry types is in the first release — book, chapter, article, web only?
3. ***Netografia* separation.** Is a separate authored section acceptable, or must web sources appear in the single alphabetical list with access dates?
4. **CSL rendering.** Custom CSL files load, but whether Typst's CSL engine reproduces the exact punctuation of the faculty examples is **unverified**; a rendered comparison is required before claiming compliance.
5. **Photograph and table source lines.** The source line format (`SRC-016`) interacts with citation macros; confirm whether the source line takes a full citation or a free-text attribution.
