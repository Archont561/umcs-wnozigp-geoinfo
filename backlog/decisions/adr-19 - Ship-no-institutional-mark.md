---
id: ADR-19
status: accepted
date: 2026-11-22
---

# ADR-19: Ship no institutional mark; take the logo as a parameter

## Context

ADR-18 bundled the UMCS logotype with the package so that a student's build
would reproduce the faculty's required title page without further assembly. The
mark was recorded as third-party artwork whose redistribution terms are
unresolved: the university publishes the logotype for download and governs its
use in the *Księga Identyfikacji Wizualnej* (SRC-049), but publishing a download
is not a licence to redistribute and the site reserves all rights. The question
was put to Centrum Promocji UMCS as U-1.

An unanswered question is not a neutral state. It meant the package could not be
released, and it put the burden of chasing an institution on whoever wanted to
publish a typesetting library. The maintainer asked whether the package could
instead avoid the question rather than wait on it.

## Decision

1. **Remove the bundled mark.** `packages/typst/assets/umcs-logo.png` and its
   notice are deleted. The package contains no institutional artwork, so it has
   nothing to license and U-1 no longer gates its release.

2. **Take the mark as a path parameter.** `coverpage(meta, cycle, logo: none)`
   and `umcs-thesis(..., logo: none)` accept a path to an image the caller
   supplies — the student's own copy of the file UMCS publishes. The package
   draws it at the sample's measured width, 245.4 pt.

3. **Draw a placeholder when none is supplied**, occupying exactly the mark's
   measured box — 245.4 × 63.6 pt at (52, 70.5) pt from the page's top-left.
   Every other coordinate on the title page is expressed against that box, so
   the placeholder leaves the layout identical. It is deliberately plain (no
   eagle, no wordmark) and deliberately visible: a build must not silently
   produce a title page that looks official but is missing its mark.

4. **Assert the absence.** A release test fails if any file in the package has
   "logo" in its name, so a future contributor cannot quietly re-add the mark
   and re-open the licensing question. The title-page tests assert the
   placeholder's box at the sample's coordinates, and a scenario proves that a
   supplied image replaces it.

## Consequences

- **U-1 is no longer a release blocker.** It remains worth asking — a bundled
  official file would be more convenient — but its answer now decides a
  convenience, not a permission.
- **A student must supply the mark.** The README says how. A title page built
  without one is visibly incomplete rather than silently wrong, which is the
  trade this decision accepts.
- **The package no longer reproduces the sample's title page out of the box.**
  It reproduces the sample's *form*, with the mark's place reserved. That is a
  real reduction in what "reproduces the sample" means and should be stated
  wherever the package claims parity.
- **A new dependency on the caller's file system**, and a new failure mode: a
  wrong path produces a compile error from Typst rather than a fallback. That is
  preferable to a silent placeholder in a submission.
- **The placeholder is a maintainer choice, not a source requirement.** Nothing
  in the faculty's guidance describes it.

## Alternatives rejected

- **Wait for U-1.** Rejected: it converts an institutional permission question
  into an indefinite block on work that has no other reason to wait.
- **Ship the mark and remove it on request.** Rejected: it publishes first and
  asks later, which inverts the order this repository has used everywhere else.
- **Draw a generic mark instead of a placeholder.** Rejected: a drawn stand-in
  that resembles the logotype would be a different, larger problem — it would
  look like a licensed reproduction without being one.
