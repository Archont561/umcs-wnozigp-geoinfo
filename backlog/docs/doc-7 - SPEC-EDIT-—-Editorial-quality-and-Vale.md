---
id: doc-7
title: SPEC-EDIT — Editorial quality and Vale
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-EDIT — Editorial quality and Vale

**Status:** Draft  
**Version:** 0.1  
**Related decision:** ADR-4  
**Related tasks:** TASK-7, TASK-10  
**Milestone:** M-2

## Purpose and limits

Use the supplied PLTechnical Vale preset as a conservative Polish technical-prose review aid. Its findings are editorial prompts. They are not automatic corrections, a full Polish grammar check, or proof of academic correctness.

## Provisioning and configuration

- Vale is pinned as `vale==3.26.0` in the root Pixi Conda dependencies. `pixi install --locked` downloads the executable through Conda channels.
- `.vale.ini` and `.vale/styles/PLTechnical/*.yml` are local, so `vale sync` is not required.
- `lint-vale` runs with a warning-level threshold. Suggestion-level findings remain available for manual review but do not fail the repository gate.
- `examples/vale/preset-demo.md` contains intentional findings; `pixi run --locked vale-demo` prints JSON with `--no-exit` for review only.
- The rules are applied to Markdown and plain text. Literal output should be fenced or inline-coded in Markdown. This repository does not configure a LaTeX prose extractor.

## Included rule intent

| Rule | Level | Scope |
| --- | --- | --- |
| Bureaucratic | suggestion | Candidate bureaucratic phrases; review meaning before editing. |
| Pleonasms | suggestion | A small editorial list of possible redundancies. |
| VerbPhrases | suggestion | Candidate noun-heavy phrases; preserve tense, aspect, and agency. |
| LongSentences | suggestion | More than 30 approximate tokens; an editorial threshold, not a linguistic norm. |
| UnitSpacing | warning | A limited list of number/unit patterns; not a full SI validator. |

The preset deliberately does not ban passive voice, negation, technical terms, nominalizations, or full numeric precision. It does not automatically choose a percent-spacing convention.

## Requirements

- **EDIT-001:** Suggestions shall require human judgment; no automated rewrite is authorized.
- **EDIT-002:** The style files and their limitations shall remain version-controlled with this repository.
- **EDIT-003:** Tests shall cover clean examples, expected alerts, code spans/fences, and unit-space cases.
- **EDIT-004:** The source and redistribution license of the supplied preset shall be reviewed before a public release.

## Provenance and source basis

The rules and accompanying README were supplied by the user in `Vale_PLTechnical_preset.zip.txt`. The archive contains no explicit license file. The included README cites the following principles:

- Fundacja Języka Polskiego et al., *Prosty język – ustandaryzowane zasady*, especially §§3–4 and the warning against mechanical application in §6: <https://www.fundacjajezykapolskiego.pl/wp-content/uploads/2025/01/Prosty-jezyk-ustandaryzowane-zasady.pdf>
- Polish public-sector plain-language guidance, used as readability advice rather than a mandate to remove specialist terminology: <https://www.gov.pl/web/sluzbacywilna/prosty-jezyk> and <https://www.gov.pl/web/dostepnosc-cyfrowa/prosty-jezyk>
- GUM SI materials for number/unit spacing: <https://www.gum.gov.pl/download/1/7095/UlotkaSI-druk.pdf> and <https://www.gum.gov.pl/ftp/pdf/Wydawnictwa/Miedzynarodowy_uklad_jednostek_miar_broszura_2023_oznak_.pdf>

The exact phrase lists are editorial examples, not verbatim normative lists from those sources. This preset is not an official government product or a full Polish orthography standard. Preserve these cautions and review ownership/redistribution terms before publishing or relicensing the rules.
