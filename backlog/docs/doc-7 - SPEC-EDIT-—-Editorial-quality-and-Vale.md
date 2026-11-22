---
id: doc-7
title: SPEC-EDIT — Editorial quality and Vale
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-EDIT — Editorial quality and Vale

**Status:** Draft (rules measured, provenance and departures documented, no second source, licence reading confirmed by the author)  
**Version:** 0.5  
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

## Provenance: the gov.pl plain-language guidance

The preset is a **maintainer-written** set of Vale rules derived from the Polish
public-administration plain-language guidance published on `gov.pl`, not an
official artefact of any ministry. The relevant pages, all retrieved
2026-11-22:

| Source | What it supplies |
| --- | --- |
| <https://www.gov.pl/web/cyfryzacja/prosty-jezyk> | The Ministry of Digital Affairs guidance, including the `w dniu dzisiejszym → dzisiaj` and `dedykowany → przeznaczony` examples |
| <https://www.gov.pl/web/sluzbacywilna/prosty-jezyk> | The Civil Service 21-point rule set: short sentences, no verbal nouns, no passive voice, no participles |
| <https://www.gov.pl/web/dostepnosc-cyfrowa/prosty-jezyk> | The accessibility framing |
| <https://www.gov.pl/web/cyfryzacja-badania-i-projektowanie/proste-jak-jezyk> | The CIO's 10 rules, incl. the four-syllable/foreign-origin definition of a hard word |
| <https://www.gov.pl/web/redakcyjne-abc/prosty-jezyk> | Editorial practice for administrative text |

**There is no second source.** The maintainer confirms that these pages are the
preset's only external basis: nothing was taken from a third party's checklist, a
commercial style guide, or another Vale style. That is worth stating because the
archive `Vale_PLTechnical_preset.zip.txt` arrived with no licence file and no
provenance note, so until now the absence of a second source was an assumption
rather than a fact.

**None of these pages states a licence.** They are public guidance and are
cited here as the basis for rules that are themselves original to this
repository: the tokens and regular expressions were written here, the examples
the guidance gives were not copied wholesale, and the rule messages are our own
sentences. That is what makes the five rule files MIT-licensable while the
guidance stays a citation.

**Confirmed by the author, 2026-11-22:** the rules were written by them from this
guidance. That is an assertion of authorship by the repository's copyright
holder, not third-party review — the single-person limitation ADR-9 records —
but the reading carries an explicit statement behind it now. V-1 in the reviewer
ledger is closed; see its *Answered* section for what the confirmation does and
does not establish.

### Where the preset departs from the guidance it cites

This matters more than the provenance. The guidance is written for
**administrative correspondence addressed to the public**; this preset lints
**technical and academic prose**. Several rules were therefore deliberately
weakened, and one is weaker than its own stated basis suggests:

- **Passive voice is not checked.** The Civil Service rules forbid it (point
  11); academic and technical writing uses it legitimately and constantly
  (method sections, procedural descriptions). Shipped as a rule, it would fire
  on nearly every page.
- **Verbal nouns are not checked as a class.** The guidance forbids `–anie`,
  `–enie`, `–cie` nouns (points 13, 5). `VerbPhrases` covers three specific
  phrases (`dokonano oceny`, …), not the class.
- **Participles and `nieosobowe` forms are not checked** (points 12, 14).
- **Sentence length is 30 tokens, not the guidance's 15–20 words.** `superior`
  technical sentences carrying qualifiers are routinely 25–30 words; a 20-token
  limit would make the gate unusable on this repository's own prose. The rule
  message says so explicitly, which is the right way to record a policy choice.
- **`UnitSpacing` has no basis in the plain-language guidance at all.** It is an
  editorial convention this repository added. It is the only rule at `warning`
  level, i.e. the only one that can fail CI, which is a notable asymmetry: the
  rule with the weakest external basis is the one with teeth.

Two rules do track the guidance closely: `Bureaucratic` implements the
`w dniu dzisiejszym → dzisiaj` example and its neighbours, and `Pleonasms`
implements the concision advice.

| Rule | Guidance it derives from |
| --- | --- |
| `Bureaucratic` | Ministry of Digital Affairs: `w dniu dzisiejszym → dzisiaj`; "unikaj przesady, patosu i podniosłego stylu (zamiast np. niniejszy – ten)" |
| `Pleonasms` | "Unikaj zbędnych słów. Pisz zwięźle" (all pages) |
| `VerbPhrases` | Civil Service points 10 and 13: prefer verbs, avoid `–anie`/`–enie`/`–cie` nouns |
| `LongSentences` | Civil Service point 7 and CIO rule 2: 15–20 words; relaxed here to 30 tokens |
| `UnitSpacing` | **None.** A local editorial convention, added by this repository |

### What this means for the ledger

The rules are a **technical-prose profile inspired by** the guidance, not an
implementation of it. Calling them "PLTechnical" is accurate; calling them
"gov.pl's rules" would not be, and the READMEs must not. ADR-4 records the same
conclusion from the provisioning side.

## Measured rule behaviour

Every row below was observed by running Vale 3.26.0 against the fixtures on 2026-11-21, not inferred from the rule names.

| Rule | Level | Matched examples | Non-matches that matter |
| --- | --- | --- | --- |
| Bureaucratic | suggestion | `w dniu dzisiejszym`, `na chwilę obecną`, `niniejszym informujemy`, `w przedmiotowej sprawie` | Only the seven listed phrases; ordinary bureaucratic prose passes |
| Pleonasms | suggestion | `w okresie czasu`, `wzajemna współpraca`, `cofać się do tyłu`, `fakt autentyczny` | Fixed list of six; it is not a redundancy parser |
| VerbPhrases | suggestion | `Dokonano analizy`, `Została przeprowadzona analiza`, `Zostały przeprowadzone analizy` | `Przeprowadzono analizę` passes — that is the active form, which the rule is not meant to catch |
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

### A rule that matched nothing, found on 2026-11-22

Writing the provenance section above prompted a re-measurement, which found that
`VerbPhrases`' second pattern could never match real Polish. It read
`przeprowadzo(?:no|na) została (?:analiza|ocena|weryfikacja)`, which only matches
the ungrammatical "Przeprowadzono została analiza". Every real sentence passed
silently — including **"Została przeprowadzona analiza"**, the passive
construction the guidance names as the thing to avoid.

Nothing caught it because the fixture's `VerbPhrases` section only exercised the
`dokonano` pattern, and no test compared the fixture's findings to a number. Both
gaps are now closed: the pattern covers the real passive forms, the fixture
exercises them, and `tests/vale/test_vale_preset.py` asserts the exact finding
count per rule plus both directions of the passive/active distinction. Reverting
the pattern fails two tests.

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
