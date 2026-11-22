---
id: doc-9
title: REVIEWERS — Open reviewer questions
type: other
created_date: '2026-11-22 16:35'
---

## REVIEWERS — Open reviewer questions

**Status:** Living document
**Version:** 0.1
**Related tasks:** TASK-1, TASK-3, TASK-7, TASK-13
**Milestones:** M-0, M-2, M-4

## Purpose

Four things block work in this repository not because nobody has done them but
because nobody outside it has answered a question. This document is where those
questions live, so they are asked rather than remembered.

They come in three kinds, and the difference matters:

- **Questions to the faculty** decide what the template should do. Until they
  are answered, the package follows the source's prose and records the gap
  (SPEC-SOURCE's conflicts section).
- **Questions to the university** decide whether an asset may ship. The logo is
  the only one; the fonts are already clear.
- **Questions to the preset's author** decide whether a dependency may ship.
  The Vale rules are the only one.

Nothing here is a request to change this repository's code. Each is a question
whose answer changes a decision that is currently recorded as open, and each
names the record it would close.

## To the faculty

Address: the Dean's office of the Faculty of Earth Sciences and Spatial
Management (Wydział Nauk o Ziemi i Gospodarki Przestrzennej) is the body that
issues the rules; the questions are about the *Zasady dyplomowania 2025/2026*
(SRC-001–SRC-048).

### F-1. Do the page targets in SRC-002 apply, and if so to what?

SRC-002 asks for Times New Roman 12 pt, 1.5 line spacing, and "~30 lines per
page at ~70 characters". SRC-003 fixes all margins at 2.5 cm. Measured against
Times metrics, those two rules together yield about **91 characters and 39
lines** per page — not 70 and 30. Reaching either target would break a stated
rule (see SPEC-SOURCE, *Conflicts within the source*).

> Does the faculty intend ~70 characters / ~30 lines as a requirement, in which
> case which of the four figures gives way — face, size, spacing or margins?
> Or are they a description of a page the author had in mind, in which case may
> a template follow the stated figures and exceed the approximations?

**Why it matters:** the package currently produces ~91 × ~39 and records that as
a known deviation. An answer turns a recorded deviation into either compliance
or a specified change. **Closes:** TASK-10 criterion 4, partly; SPEC-SOURCE's
conflict.

### F-2. May a thesis be produced in LaTeX or Typst at all?

SRC-040 records that the source names *Word, OpenOffice Writer and LibreOffice
Writer* only, and says nothing about markup-based typesetting. This repository
exists to answer that question with working software, but it cannot answer it
with evidence.

> Does the faculty accept a PDF produced by LaTeX or Typst, provided it
> satisfies the editorial rules and the required title-page form?

**Why it matters:** if the answer is no, TASK-9 and TASK-10 are educational
exercises rather than usable templates, and the README must say so more
strongly than it does. **Closes:** SPEC-SOURCE's SRC-040.

### F-3. Is the 2026/27 edition different from 2025/26?

ADR-10 records that the 2025/26 rules are a **proxy** for the 2026/27 cohort
this repository targets, because no 2026/27 edition was published when the
ledger was built.

> When the 2026/27 edition is published, which requirements changed — and may
> students starting in that year rely on this template's reading of the current
> edition in the meantime?

**Why it matters:** every requirement in SPEC-SOURCE is conditional on an
answer. **Closes:** SPEC-SOURCE's applicability note.

### F-4. Which front-matter lists are required?

SRC-042 records the source as **silent** on which lists are omitted when a
thesis has no tables or figures, and ADR-17 folds photographs into figures
because the source's prose and its sample disagree on the classes.

> Should a thesis with no listings omit *Spis listingów*, or print it with the
> heading and no entries? And is folding photographs into figures acceptable
> when the sample appears to list them separately?

**Why it matters:** the package treats each list as present only if content
exists, and asserts no photograph class. That is a maintainer decision standing
in for a missing rule. **Closes:** SRC-042, and ADR-17's recorded deviation.

## To the university

Address: **Centrum Promocji UMCS**, which publishes the visual identity system
and the logotype downloads.

### U-1. May this repository redistribute the UMCS logotype?

`packages/typst/assets/umcs-logo.png` is the shortened UMCS logotype, in
university grey, extracted from the faculty's own title-page sample and
**re-encoded** — cropped to its ink and downsampled — rather than taken from the
official download archive. The university publishes the mark for download and
governs its use in the *Księga Identyfikacji Wizualnej* (2024, v02, SRC-049),
but publishing a download is not a redistribution licence, and the site
reserves all rights.

> May a public, MIT-licensed repository bundle this file so that a student's
> build reproduces the required title page? If yes, does the university require
> a particular attribution statement, an unmodified copy of the official file,
> or a specific colour variant?

**Status: no longer blocking.** ADR-19 removed the bundled mark and made it a
`logo` parameter, so a release no longer includes the artwork and this question
no longer gates it. It stays here because a bundled official file would still
be more convenient than asking every student to fetch one, and because the
answer decides whether that convenience is available.

Note that the file the package used to ship was a re-encoding of the sample's
embedded copy, so "use the official file" is itself an answer worth having.
**Closes:** TASK-3 criterion 3, ADR-18's open question, if the answer is yes.

## To the author of the Vale preset

Address: the repository owner, who supplied `Vale_PLTechnical_preset.zip.txt`
and is the only party known to have it.

### V-1. What are the redistribution terms of the PLTechnical rules?

The supplied archive contains a `.vale.ini`, five rule files and a README, and
**no licence file** (ADR-4). The rules are committed to this public repository
under `.vale/styles/PLTechnical/`. Five files, all small: `Bureaucratic`,
`LongSentences`, `Pleonasms`, `UnitSpacing`, `VerbPhrases`.

> Who owns these rules, and under what terms may they be redistributed? If the
> answer is unknown or restrictive, should they stay committed (making this a
> private-use repository) or be removed and replaced with a short note telling a
> reader how to supply their own preset?

**Why it matters:** it is now the *only* remaining file in the repository whose
terms are unknown — with the logotype no longer bundled, nothing else is — and
it gates TASK-3 criterion 2. **Closes:** TASK-3
criterion 2, ADR-4's fifth decision.

## What this document does not do

It does not assert that any question has been asked, that any address is the
correct one, or that an answer would be binding. It records what is unresolved
and who could resolve it. Answers should be recorded against the SPEC or ADR
named under each question, and this document updated to say so.
