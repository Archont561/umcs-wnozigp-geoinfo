---
id: ADR-16
status: accepted
date: 2026-11-21
---

# ADR-16: Use Tectonic's embedded BibTeX engine, not Biber

## Context

ADR-12 chose BibLaTeX with Biber for the LaTeX half and left one blocker: Biber was absent from the environment. SPEC-BIB listed three ways out — add `biber` from conda-forge, rely on Tectonic's `tectonic-biber` integration, or fall back to classic BibTeX.

Measured on 2026-11-21, all three of those premises were wrong or unavailable:

1. **conda-forge does not ship a `biber` package.** `conda-forge/biber-feedstock` returns 404, and `feedstock-outputs` contains no `biber`, `biblatex` or `tectonic-biber` output among its 33,918 entries. SPEC-BIB's option 1 — "Conda-forge provides it" — is simply false.
2. **`tectonic-biber` is not a released binary.** Tectonic 0.17.0 searches for `./tectonic-biber` then `tectonic-biber` on `PATH` (`src/driver.rs`, `check_biber_requirement`), but no such artifact exists in the release assets and no feedstock builds one. `tectonic -X biber` fails with "no internal or external subcommand `biber`". SPEC-BIB's option 2 was never viable.
3. **Biber is not vendorable here.** A Perl program, it would need scripting and a TeX Live tree, and sandbox egress reaches neither `conda.anaconda.org` nor `prefix.dev` (both time out), so nothing can be added and re-locked from this environment anyway.

Meanwhile the third option is stronger than SPEC-BIB credited it: **Tectonic embeds a complete BibTeX engine** as a Rust crate (`crates/engine_bibtex`, compiled into the binary — 307 symbols), so `.bst`-driven `.bib` processing runs with no external binary, no Perl, and no network. It is the same engine the Tectonic test suite covers.

## Decision

1. **LaTeX uses classic BibTeX with a repository-owned `.bst`**, run by the Tectonic engine already in the lockfile. No `biber`, no `biblatex`, no Perl.
2. **Withdraw the `.bbx`/`.cbx` half of ADR-12.** Its rationale — a stock style cannot produce `Surname B., 2003.` — still holds, so the style is still repository-owned; only the processor changes.
3. **Add no dependency.** The toolchain stays exactly as locked, so `check-pixi-lock` and the offline restore path are untouched.
4. **Typst is unchanged:** Hayagriva plus a repository-owned CSL file (ADR-12, verified offline).
5. **Record what this costs.** BibTeX's `.bst` language is weaker than BibLaTeX's: no `\DeclareNameFormat`, no full Unicode in the engine's 8-bit string model, and diacritics require `{\'z}`-style escapes rather than raw UTF-8. SPEC-BIB must state these limits instead of promising UTF-8 Polish sorting.

## Consequences

- TASK-11 unblocks with **zero new dependencies**, which is the outcome that keeps the offline restore guarantee intact.
- Polish diacritics in the bibliography become an explicit, testable constraint: either escape them in `.bib` or verify the engine passes raw UTF-8 through. This must be measured before BIB-003 is claimed.
- The `.bst` is a genuinely harder artifact to write than a `.bbx`, and it is language-limited in ways a modern user may not expect. That burden is accepted in exchange for an offline, lockfile-stable build.
- Cross-format parity remains explicitly not promised (BIB-004): the two formats now differ in processor as well as style.
- If a future Pixi environment gains Biber, this decision can be revisited — but nothing in the repository may assume it exists.

## What this does not authorize

It does not add a `.bib` file, a `.bst`, a bibliography command, or any claim that either format reproduces the faculty's punctuation. It records a processor choice only.
