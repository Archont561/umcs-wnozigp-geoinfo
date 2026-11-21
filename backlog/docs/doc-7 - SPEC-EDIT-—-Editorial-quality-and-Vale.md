---
id: doc-7
title: SPEC-EDIT — Editorial quality and Vale
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-EDIT — Editorial quality and Vale

**Status:** Draft (rules measured and documented; licence review open)  
**Version:** 0.2  
**Related decisions:** ADR-4, ADR-5, ADR-9, ADR-13  
**Related tasks:** TASK-7, TASK-10  
**Milestone:** M-2

## Purpose and limits

Use the supplied PLTechnical Vale preset as a conservative Polish technical-prose review aid. Its findings are editorial prompts. They are not automatic corrections, a full Polish grammar check, or proof of academic correctness.

## Provisioning and configuration

- Vale is pinned as `vale==3.26.0` in the root Pixi Conda dependencies.
- `.vale.ini` and `.vale/styles/PLTechnical/*.yml` are local, so `vale sync` is not required.
- `lint-vale` runs with `--minAlertLevel=warning`, so suggestion-level findings are reported but do not fail the gate; warnings do.
- Rules apply to Markdown and plain text only. There is no LaTeX or Typst prose extractor, so the preset does **not** check thesis body text.
- Two fixtures exist: `examples/vale/preset-demo.md` (advisory demo) and `examples/vale/rule-cases.md` (expectation fixture, see below).

## Measured rule behaviour

Every row below was observed by running Vale 3.26.0 against the fixtures on 2026-11-21, not inferred from the rule names.

| Rule | Level | Matched examples | Non-matches that matter |
| --- | --- | --- | --- |
| Bureaucratic | suggestion | `w dniu dzisiejszym`, `na chwilę obecną`, `niniejszym informujemy`, `w przedmiotowej sprawie` | Only the seven listed phrases; ordinary bureaucratic prose passes |
| Pleonasms | suggestion | `w okresie czasu`, `wzajemna współpraca`, `cofać się do tyłu`, `fakt autentyczny` | Fixed list of six; it is not a redundancy parser |
| VerbPhrases | suggestion | `Dokonano analizy`, `przeprowadzono analizę` | Pattern-based; correct nominalisations may still be flagged |
| LongSentences | suggestion | One sentence above 30 tokens | 29 tokens passes; the count is a regex token count, not a linguistic word count |
| UnitSpacing | warning | `20cm`, `5kg`, `20°C`, `3,5cm`, `3.5cm`, `-5°C` | `20 m`, `45°`, `45°30′`, and anything inside a code span or URL |

### UnitSpacing is narrower and wider than its message says

The rule message states that `°`, `′`, `″` are exceptions. Measurement shows this is true for a bare angular value and false for a temperature:

- `Kąt wynosi 45°.` → **no finding** (correct, matches the message)
- `Temperatura 20°C.` → **finding** (the unit here is `°C`, not a bare degree sign)
- `Kąt wynosi 45°30′.` → **no finding** (correct)

So the message is right about angle signs and silently incomplete about temperature. Recorded because a reviewer reading only the message would expect `20°C` to pass.

Additional measured behaviour: `%` is deliberately excluded from the pattern, so `20%` produces no finding and the preset never chooses a percent-spacing convention. Negative and signed values are matched (`-5°C`, `+5°C`). Matches inside inline code (`` `20cm` ``) and URLs are suppressed by Vale's `nonword` handling.

## Expectation fixture and its guards

`examples/vale/rule-cases.md` states the expected finding count in each section heading, then supplies the triggering text. Two guards keep it honest:

1. **The same word must appear in a heading and in a body line.** Vale treats a Markdown heading as a sentence, so a phrase in a heading is flagged too. The fixture deliberately puts each phrase in both places and expects **two** findings. A test that diffs the JSON can therefore assert the exact count.
2. **A clean control section** expects zero findings, so a rule that starts matching everything is caught.

A first draft of this fixture asserted `20°C` and `20 cm` behaved one way and the run disagreed; the expectations were corrected against the output rather than the output being argued with. That is the intended workflow.

## Included rule intent

| Rule | Level | Scope |
| --- | --- | --- |
| Bureaucratic | suggestion | Candidate bureaucratic phrases; review meaning before editing. |
| Pleonasms | suggestion | A small editorial list of possible redundancies. |
| VerbPhrases | suggestion | Candidate noun-heavy phrases; preserve tense, aspect, and agency. |
| LongSentences | suggestion | More than 30 approximate tokens; an editorial threshold, not a linguistic norm. |
| UnitSpacing | warning | A limited list of number/unit patterns; not a full SI validator. |

The preset deliberately does not ban passive voice, negation, technical terms, nominalizations, or full numeric precision.

## Overriding an alert

Maintainers may silence a specific finding without weakening the gate globally (TASK-7 criterion 4). In order of preference:

| Method | Scope | Effect on other checks |
| --- | --- | --- |
| Rewrite the sentence | one place | none |
| Inline code span | one phrase | none — Vale skips code |
| `.vale.ini` section for one path | one file | none |
| `MinAlertLevel` change | **repository-wide** | weakens or strengthens everything; requires an ADR |

The first three are local and need no approval. The fourth changes the meaning of the gate for every file, so it is a policy change, not an edit — which is why `lint-vale` keeps `--minAlertLevel=warning` in the Pixi task rather than in `.vale.ini`, where a casual edit would silently disable warnings.

## Requirements

- **EDIT-001:** Suggestions shall require human judgment; no automated rewrite is authorized.
- **EDIT-002:** The style files and their limitations shall remain version-controlled with this repository.
- **EDIT-003:** Tests shall cover clean examples, expected alerts, code spans/fences, and unit-space cases.
- **EDIT-004:** The source and redistribution license of the supplied preset shall be reviewed before a public release. **Still open.**
- **EDIT-005:** The observed behaviour of each rule shall be recorded from a run, not from the rule names, and re-measured when a rule changes.
- **EDIT-006:** Threshold changes and rule additions shall require an ADR, because they alter the meaning of the whole gate.
- **EDIT-007:** The preset shall not be described as checking thesis prose until a LaTeX or Typst extractor exists.

## Provenance and licence status

The rules and README were supplied in `Vale_PLTechnical_preset.zip.txt`. The archive contains **no licence file**, and no licence was stated in the supplying message.

Current position, unchanged since ADR-4 and ADR-5:

- The rules are used **locally within this repository** and are not redistributed as a standalone package.
- **MIT (ADR-7) does not cover them.** The repository licence applies to original work only.
- The `v*` release workflow publishes the package directories, which do **not** include `.vale/`, so a source release does not currently redistribute the preset.
- Review by a Polish-language reviewer and confirmation of reuse rights **remain open** (TASK-7 criterion 3, EDIT-004).

The included README cites:

- Fundacja Języka Polskiego et al., *Prosty język – ustandaryzowane zasady*, §§3–4 and the §6 warning against mechanical application: <https://www.fundacjajezykapolskiego.pl/wp-content/uploads/2025/01/Prosty-jezyk-ustandaryzowane-zasady.pdf>
- Polish public-sector plain-language guidance: <https://www.gov.pl/web/sluzbacywilna/prosty-jezyk> and <https://www.gov.pl/web/dostepnosc-cyfrowa/prosty-jezyk>
- GUM SI materials for number/unit spacing: <https://www.gum.gov.pl/download/1/7095/UlotkaSI-druk.pdf> and <https://www.gum.gov.pl/ftp/pdf/Wydawnictwa/Miedzynarodowy_uklad_jednostek_miar_broszura_2023_oznak_.pdf>

The phrase lists are editorial examples, not verbatim normative lists from those sources. The preset is not an official government product, not a Polish orthography standard, and not a compliance tool.
