---
id: ADR-18
status: accepted
date: 2026-11-21
---

# ADR-18: Reproduce the title page form, including the university logo

## Context

SRC-045 records that the title page has a prescribed form, and the faculty supplies a one-page sample of it. The package reproduced the *fields* the sample lists but not its *layout*: it centred everything, omitted the logo, omitted the vertical rule beside the fields, and set the university name in the body serif.

The owner directed on 2026-11-21 that the title page look like the supplied sample. Reproducing it needs two things the repository did not have:

1. the university's logo/wordmark, extracted from the sample, as an image the package can embed;
2. a measured description of the sample's geometry, so the layout is copied rather than approximated.

This engages two existing rules. ADR-7 clause 4 says not to infer a licence for institution logos and to record provenance for such assets. `AGENTS.md` says not to add an official logo/seal without a scoped task and a decision. This ADR is that decision.

## Decision

1. **Add the university's logotype as a package asset.**
   `packages/typst/assets/umcs-logo.png` is the UMCS logotype — the shortened
   variant, sygnet and `UMCS` wordmark in university grey — extracted from the
   faculty's own sample PDF, cropped to its ink, and downsampled. Nothing is
   redrawn or recoloured. It is the *university's* mark, not the faculty's, and
   it is attributed to UMCS as its rightsholder rather than left as an
   unattributed image: the university publishes the logotype for download and
   governs its use in the *Księga Identyfikacji Wizualnej* (SRC-049), so a
   bundled copy needs to say whose it is and which rules apply. Its terms ship
   beside it as `assets/UMCS-LOGO-NOTICE.md`, which the release archive
   requires for the same reason it requires the file itself.
2. **Record provenance and do not relicense it.** The asset is third-party material. The MIT grant from ADR-7 covers the repository's own code and does not extend to this file. Its provenance and the unresolved question of permission to redistribute it are recorded in `packages/typst/assets/README.md` and in the asset's own licence note.
3. **Copy the geometry from the sample.** The title page is laid out at absolute positions taken from the sample's content stream: logo ink at (52, 70.5) pt, a 1 pt rule at x = 118 pt from 292.9 pt to 709.2 pt below the top edge, heading at x = 119.5 pt, fields indented to x = 132.5 pt, city and year at 736.7 pt. `test_typst_titlepage_bdd.py` measures a render against those numbers.
4. **Vendor the sample's serif.** `packages/typst/assets/fonts/` carries
   TeX Gyre Termes, the face the sample's fields and title are set in, under its
   GUST Font Licence. It is third-party material like the logo, but unlike the
   logo its licence permits redistribution, so it can ship. Typst's
   `New Computer Modern` is about 14 % wider for the same string, which pushed
   the title past the right margin; shipping Termes is what makes the title's
   width match the sample rather than approximate it.
5. **Substitute only the heading face, and assert it.** The sample's
   LMSans10-Bold is not selectable through Typst 0.15, which exposes a single
   wider `New Computer Modern`. Typst also does not search the environment's
   `fonts/` unless `TYPST_FONT_PATHS` says so, so that variable is set in
   `pixi.toml` and in the build tool, listing both the package's fonts and the
   environment's. The cover uses the narrowest sans in that set, and a test
   asserts that the university still breaks after "Curie-Skłodowskiej", which
   is the property a wider face breaks.
6. **Keep the extra fields out of the sample's fixed blocks.** The sample has no specialisation line and fixes the bottom block at exactly three lines, so a specialisation is printed as a second identifier line beside the rule rather than appended to that block.

## Consequences

- The title page now matches the faculty's sample page for page, but the sample is a *form*, not a licence: the logo's redistribution terms are unresolved and a release must settle them before the asset ships in an archive. Attribution is now correct and specific — UMCS, shortened logotype, university grey, identity book 2024 v02 — which is what the question to Centrum Promocji UMCS needs, and it does not itself grant permission: publishing a download is not a redistribution licence and the site reserves all rights.
- The archive and build task lists now include the asset, because a tarball without it compiles to a title page with no header rather than failing loudly.
- `TYPST_FONT_PATHS` is now part of the build contract and must list two
  directories: the package's vendored fonts and the environment's. Changing
  either breaks the cover's metrics rather than the cover's existence, which is
  why the geometry is tested.
- The vendored fonts add a second third-party licence (GUST) to the package.
  It permits redistribution, unlike the logo's unresolved terms, so the release
  question remains only about the image.
- This does not authorize publishing the package or the archive, and it does not establish that a submission built with it is faculty-approved.
