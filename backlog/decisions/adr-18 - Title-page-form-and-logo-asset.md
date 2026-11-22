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

1. **Add the logo as a package asset.** `packages/typst/assets/umcs-logo.png` is the eagle-and-wordmark image extracted from the faculty's own sample PDF, cropped to its ink, and downsampled. Nothing is redrawn or recoloured.
2. **Record provenance and do not relicense it.** The asset is third-party material. The MIT grant from ADR-7 covers the repository's own code and does not extend to this file. Its provenance and the unresolved question of permission to redistribute it are recorded in `packages/typst/assets/README.md` and in the asset's own licence note.
3. **Copy the geometry from the sample.** The title page is laid out at absolute positions taken from the sample's content stream: logo ink at (52, 70.5) pt, a 1 pt rule at x = 118 pt from 292.9 pt to 709.2 pt below the top edge, heading at x = 119.5 pt, fields indented to x = 132.5 pt, city and year at 736.7 pt. `test_typst_titlepage_bdd.py` measures a render against those numbers.
4. **Set the heading in a sans face.** The sample uses a sans for the university, the faculty and the fields. The root Pixi environment ships Ubuntu and DejaVu Sans but Typst does not search the environment's `fonts/` unless told to, so `TYPST_FONT_PATHS` is set both in `pixi.toml` and in the Typst build tool. A build without it renders the cover in a serif and the measured geometry drifts.
5. **Keep the extra fields out of the sample's fixed blocks.** The sample has no specialisation line and fixes the bottom block at exactly three lines, so a specialisation is printed as a second identifier line beside the rule rather than appended to that block.

## Consequences

- The title page now matches the faculty's sample page for page, but the sample is a *form*, not a licence: the logo's redistribution terms are unresolved and a release must settle them before the asset ships in an archive.
- The archive and build task lists now include the asset, because a tarball without it compiles to a title page with no header rather than failing loudly.
- `TYPST_FONT_PATHS` is now part of the build contract. Changing the environment's font layout breaks the cover's metrics rather than the cover's existence, which is why the geometry is tested.
- This does not authorize publishing the package or the archive, and it does not establish that a submission built with it is faculty-approved.
