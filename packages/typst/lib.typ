// UMCS WNoZiGP thesis package — PROTOTYPE, NOT APPROVED FOR SUBMISSION.
//
// Implements the contract in SPEC-TYP (backlog/docs/doc-5) against the
// evidence ledger in SPEC-SOURCE (backlog/docs/doc-3). No faculty reviewer
// has approved it (ADR-9); it targets the 2026/27 cohort using the 2025/26
// rules as a proxy (ADR-10).
//
// Typst cannot express every spacing rule in the source, because the source
// states several of them as "two line spaces" or "1.5 lines above" rather
// than in a unit Typst models. Each such approximation is marked
// APPROXIMATED below: those are the first places to check against a printed
// copy of the guidelines.

// ---------------------------------------------------------------------------
// Vocabulary
// ---------------------------------------------------------------------------

/// Thesis types the faculty distinguishes structurally (SRC-010).
#let cycles = ("licencjacka", "inzynierska", "magisterska")

#let strings = (
  pl: (
    university: "UNIWERSYTET MARII CURIE-SKŁODOWSKIEJ",
    university2: "W LUBLINIE",
    faculty: "Wydział Nauk o Ziemi i Gospodarki Przestrzennej",
    programme: "Kierunek",
    specialisation: "Specjalność",
    album: "Nr albumu",
    thesis: "Praca dyplomowa",
    thesis-titled: "Praca dyplomowa",
    written-in: "napisana w",
    supervised-by: "pod kierunkiem",
    contents: "Spis treści",
    abstract: "Streszczenie",
    tables: "Spis tabel",
    figures: "Spis rycin",
    photographs: "Spis fotografii",
    annexes: "Spis załączników",
    annex: "Załącznik",
    appendix-heading: "Załączniki",
    table: "Tabela",
    figure: "Rycina",
    photograph: "Fotografia",
    bibliography: "Bibliografia",
    cycle-name: "magisterska",
  ),
  en: (
    university: "MARIA CURIE-SKŁODOWSKA UNIVERSITY",
    university2: "IN LUBLIN",
    faculty: "Faculty of Earth Sciences and Spatial Management",
    programme: "Programme",
    specialisation: "Specialisation",
    album: "Student ID",
    thesis: "Thesis",
    thesis-titled: "Thesis",
    written-in: "prepared in",
    supervised-by: "supervised by",
    contents: "Contents",
    abstract: "Abstract",
    tables: "List of tables",
    figures: "List of figures",
    photographs: "List of photographs",
    annexes: "List of annexes",
    annex: "Annex",
    appendix-heading: "Annexes",
    table: "Table",
    figure: "Figure",
    photograph: "Photograph",
    bibliography: "Bibliography",
    cycle-name: "master's thesis",
  ),
)

/// Polish cycle adjectives, used on the title page (SRC-012).
#let cycle-names-pl = (
  "licencjacka": "licencjacka",
  "inzynierska": "inżynierska",
  "magisterska": "magisterska",
)

#let cycle-names-en = (
  "licencjacka": "bachelor's thesis",
  "inzynierska": "engineering thesis",
  "magisterska": "master's thesis",
)

// ---------------------------------------------------------------------------
// Validation (TYP-001: one entry point taking a dictionary, unknown keys rejected)
// ---------------------------------------------------------------------------

#let allowed-meta-keys = (
  "programme",
  "specialisation",
  "author",
  "album",
  "title",
  "title-en",
  "supervisor",
  "department",
  "city",
  "year",
)

#let required-meta-keys = (
  "author",
  "album",
  "title",
  "title-en",
  "supervisor",
  "department",
)

#let quote-list(xs) = xs.map(x => "`" + x + "`").join(", ")

#let validate-meta(meta) = {
  if type(meta) != dictionary {
    panic("umcs-thesis: `meta` must be a dictionary, got " + str(type(meta)))
  }
  let unknown = meta.keys().filter(k => not allowed-meta-keys.contains(k))
  if unknown.len() > 0 {
    panic(
      "umcs-thesis: unknown meta key(s): "
        + quote-list(unknown)
        + ". Allowed keys are: "
        + quote-list(allowed-meta-keys),
    )
  }
  let missing = required-meta-keys.filter(k => not meta.keys().contains(k))
  if missing.len() > 0 {
    panic("umcs-thesis: missing required meta key(s): " + quote-list(missing))
  }
  for k in required-meta-keys {
    if type(meta.at(k)) == str and meta.at(k).trim() == "" {
      panic("umcs-thesis: meta key `" + k + "` must not be empty")
    }
  }
  // SRC-012 requires both language titles; a missing English one is an error,
  // not a silent empty placeholder.
  if meta.at("title-en").trim() == "" {
    panic(
      "umcs-thesis: `title-en` is required (SRC-012: title in Polish and English)",
    )
  }
}

// ---------------------------------------------------------------------------
// Abstract character count (SRC-014)
// ---------------------------------------------------------------------------

/// Count visible characters, ignoring markup and line breaks.
/// Typst has no built-in for this, so the content tree is walked by hand.
#let char-count(body) = {
  let walk(c) = {
    if type(c) == str {
      c.len()
    } else if type(c) == content {
      let f = c.func()
      if f == text {
        c.text.len()
      } else if f == parbreak or f == linebreak or f == h or f == v {
        0
      } else if c.has("children") {
        c.children.map(walk).sum()
      } else if c.has("body") {
        walk(c.body)
      } else {
        0
      }
    } else {
      0
    }
  }
  walk(body)
}

// ---------------------------------------------------------------------------
// Counters (SRC-021, SRC-021 → TYP-007)
//
// Three independent sequences, one per illustration class. A `figure` element
// cannot do this alone: Typst numbers figures per `kind`, but it puts every
// caption in one place and offers no caption-position control, while the
// faculty requires the caption above for tables and below for figures and
// photographs (SRC-015 vs SRC-018). Explicit counters make all three
// sequences queryable, which is what turns SRC-021 into an assertion.
// ---------------------------------------------------------------------------

#let kind-counter(kind) = counter("umcs-illustration-" + kind)

#let numbering-start = counter(page)

// ---------------------------------------------------------------------------
// Title page (SRC-012, SRC-045)
// ---------------------------------------------------------------------------

/// The normalised title page, field order per the Annex 1 sample (SRC-045).
/// Carries no page number (SRC-008).
#let coverpage(meta, cycle, language: "pl") = {
  let s = strings.at(language)
  let cycle-name = if language == "en" {
    cycle-names-en.at(cycle)
  } else {
    cycle-names-pl.at(cycle)
  }
  set par(first-line-indent: 0pt, leading: 0.5em)
  page(numbering: none)[
    #set align(center)
    #v(1.2cm)
    #text(size: 14pt, weight: "bold")[
      #s.university \
      #s.university2
    ]
    #v(0.8cm)
    #text(size: 13pt)[#s.faculty]

    #v(1.5cm)
    #set text(size: 12pt)
    #s.programme: #meta.at("programme", default: "—") \
    #s.specialisation: #meta.at("specialisation", default: "—")

    #v(2.0cm)
    #text(size: 14pt, weight: "bold")[#meta.author]

    #v(0.4cm)
    #text(size: 12pt)[#s.album: #meta.album]

    #v(2.0cm)
    #text(size: 15pt, weight: "bold")[#meta.title]
    #v(0.3cm)
    #text(size: 13pt, style: "italic")[#meta.at("title-en")]

    #v(1.8cm)
    #text(size: 12pt)[
      #s.thesis (#cycle-name)
      #linebreak()
      #s.written-in #meta.department
      #linebreak()
      #s.supervised-by #meta.supervisor
    ]

    #v(1fr)
    #text(size: 12pt, weight: "bold")[
      #upper(meta.at("city", default: "Lublin")) #meta.at(
        "year",
        default: "2027",
      )
    ]
  ]
}

/// A front-matter heading (abstract, contents, bibliography) that must not
/// consume a chapter number: `Wstęp` has to stay chapter 1 (SRC-010).
#let front-matter-heading(text-body) = heading(
  level: 1,
  numbering: none,
  outlined: false,
  text-body,
)

// ---------------------------------------------------------------------------
// Abstract (SRC-014)
// ---------------------------------------------------------------------------

/// Abstract with the 4000-character limit enforced at compile time. The count
/// is emitted as `<umcs-abstract>` metadata so a test reads it rather than
/// trusting a reviewer.
#let abstract(body, limit: 4000) = {
  let n = char-count(body)
  if n > limit {
    panic(
      "abstract: "
        + str(n)
        + " characters exceeds the faculty limit of "
        + str(limit)
        + " (SRC-014)",
    )
  }
  [#metadata((chars: n, limit: limit, has-source: false)) <umcs-abstract>]
  body
}

// ---------------------------------------------------------------------------
// Illustrations (SRC-015..SRC-022)
// ---------------------------------------------------------------------------

#let source-line(kind, source) = {
  if source == none {
    panic(
      kind
        + ": `source` is required; every illustration states its source (SRC-022)",
    )
  }
  if type(source) == str and source.trim() == "" {
    panic(kind + ": `source` must not be empty (SRC-022)")
  }
  // SRC-016/SRC-019: 10 pt italic, left aligned, after the object.
  block(above: 0.5em, below: 1em, width: 100%)[
    #set text(size: 10pt, style: "italic")
    #set par(first-line-indent: 0pt, leading: 0.65em)
    #set align(left)
    #source
  ]
}

#let register-illustration(kind, n, caption) = {
  [#metadata((
    kind: kind,
    n: n,
    caption: caption,
    page: here().page(),
    has-source: true,
  )) <umcs-illustration>]
}

/// A figure (*rycina*): caption below in 10 pt bold, source below that.
#let figure-with-source(
  body,
  source: none,
  caption: none,
) = {
  kind-counter("rycina").step()
  context {
    let n = kind-counter("rycina").get().first()
    let s = strings.pl.figure
    register-illustration("rycina", n, caption)
    block(breakable: false)[
      #block(width: 100%)[#body]
      #if caption != none {
        // SRC-018: caption below, 10 pt bold, single spacing.
        block(above: 0.5em, below: 0cm)[
          #set text(size: 10pt, weight: "bold")
          #set par(first-line-indent: 0pt, leading: 0.65em)
          #s #n: #caption
        ]
      }
    ]
  }
  source-line("rycina", source)
}

/// A table: bold 10 pt title above (SRC-015), italic 10 pt source below (SRC-016).
#let table-with-source(
  body,
  source: none,
  caption: none,
) = {
  kind-counter("tabela").step()
  context {
    let n = kind-counter("tabela").get().first()
    let s = strings.pl.table
    register-illustration("tabela", n, caption)
    block(breakable: false)[
      #if caption != none {
        block(above: 1.5em, below: 0.5em)[
          #set text(size: 10pt, weight: "bold")
          #set par(first-line-indent: 0pt, leading: 0.65em)
          #s #n: #caption
        ]
      }
      #block(width: 100%)[
        #set text(size: 10pt)
        #set par(first-line-indent: 0pt, leading: 0.65em)
        #body
      ]
    ]
  }
  source-line("tabela", source)
}

/// A photograph: its own counter (SRC-021, SRC-023), caption below (SRC-018).
#let photograph(
  body,
  source: none,
  caption: none,
) = {
  kind-counter("fotografia").step()
  context {
    let n = kind-counter("fotografia").get().first()
    let s = strings.pl.photograph
    register-illustration("fotografia", n, caption)
    block(breakable: false)[
      #block(width: 100%)[#body]
      #if caption != none {
        block(above: 0.5em, below: 0cm)[
          #set text(size: 10pt, weight: "bold")
          #set par(first-line-indent: 0pt, leading: 0.65em)
          #s #n: #caption
        ]
      }
    ]
  }
  source-line("fotografia", source)
}

/// Attribution strings from SRC-020 / SRC-047, so the punctuation is not a
/// thing a student has to remember.
#let own-work(base) = [(opracowanie własne na podstawie: #base)]
#let after(work) = [(według: #work)]

// ---------------------------------------------------------------------------
// Per-type illustration indexes (SRC-023)
// ---------------------------------------------------------------------------

#let illustration-index(kind, title, supplement) = {
  context {
    let items = query(<umcs-illustration>).filter(m => m.value.kind == kind)
    if items.len() == 0 {
      // SRC-023: these indexes appear "if such items exist".
      return
    }
    heading(level: 1, numbering: none, outlined: false, title)
    v(0.5em)
    for item in items {
      par(first-line-indent: 0pt, leading: 0.65em)[
        #supplement #item.value.n: #item.value.caption
        #box(width: 1fr, align(right)[#str(item.value.page)])
      ]
    }
  }
}

#let list-of-tables() = illustration-index(
  "tabela",
  strings.pl.tables,
  strings.pl.table,
)
#let list-of-figures() = illustration-index(
  "rycina",
  strings.pl.figures,
  strings.pl.figure,
)
#let list-of-photographs() = illustration-index(
  "fotografia",
  strings.pl.photographs,
  strings.pl.photograph,
)

// ---------------------------------------------------------------------------
// Annexes (SRC-024, SRC-025)
// ---------------------------------------------------------------------------

#let appendix-counter = counter("umcs-appendix")

/// One annex: "Załącznik N" at the top right (SRC-024).
///
/// APPROXIMATED — "top right of the page" is rendered as right-aligned text
/// at the top of the text block rather than in the page margin. A running
/// header was tried and rejected: a `page()` container nested inside the
/// show rule's context silently dropped its body in Typst 0.15.1, which is a
/// worse defect than a margin offset.
#let appendix(title: none, body) = {
  appendix-counter.step()
  // A level-1 `heading` cannot be used here: its show rule starts a new page,
  // and a page break emitted inside a `page()` container produced a blank
  // page carrying only the running header. The annex title is therefore a
  // styled block, and the page break happens before the container.
  pagebreak(weak: true)
  context [
    #let n = appendix-counter.get().first()
    #let label = strings.pl.annex
    #page(header: align(right)[#text(size: 12pt)[#label #n]])[
      #metadata((n: n, title: title)) <umcs-appendix>
      #if title != none {
        block(above: 0cm, below: 2em)[
          #set text(size: 16pt, weight: "bold")
          #set par(first-line-indent: 0pt)
          #title
        ]
      }
      #body
    ]
  ]
}

/// Marks the annex section and resets its numbering (SRC-024).
#let appendices(body) = {
  appendix-counter.update(0)
  body
}

/// The annex list, with titles (SRC-025). Omitted when there are no annexes.
#let list-of-annexes() = {
  context {
    let items = query(<umcs-appendix>)
    if items.len() == 0 {
      return
    }
    heading(level: 1, outlined: false)[#strings.pl.annexes]
    for item in items {
      par(first-line-indent: 0pt)[
        #strings.pl.annex #item.value.n
        #if item.value.title != none [: #item.value.title]
        #box(width: 1fr, align(right)[#str(item.location().page())])
      ]
    }
  }
}

// ---------------------------------------------------------------------------
// Numbered equations (SRC-026)
// ---------------------------------------------------------------------------

#let equation-counter = counter("umcs-equation")

/// An equation numbered per chapter as "(2.1.)", number right-aligned in a
/// 2 cm column (SRC-026).
#let equation-numbered(body) = {
  equation-counter.step()
  context {
    let chapter = counter(heading).get().first()
    let n = equation-counter.get().first()
    grid(
      columns: (1fr, 2cm),
      align: (center + horizon, right + horizon),
      [#body], text(size: 12pt)[(#chapter.#n.)],
    )
  }
}

// ---------------------------------------------------------------------------
// Contents (SRC-013)
// ---------------------------------------------------------------------------

/// The contents page. Numbering is Arabic and comes from the same counter as
/// the body, which is what SRC-013 requires them to match.
#let contents() = {
  front-matter-heading[#strings.pl.contents]
  outline(title: none, indent: auto, depth: 2)
}

// ---------------------------------------------------------------------------
// The show rule (SRC-001..SRC-008)
// ---------------------------------------------------------------------------

/// Textbook body settings.
///
/// - `cycle` is required and has no default: the three thesis types differ
///   structurally, so a silent default would be a silent wrong answer.
/// - `font` defaults to a documented substitute; Times New Roman is
///   proprietary and cannot ship here (TYP-006).
#let umcs-thesis(
  body,
  cycle: none,
  language: "pl",
  meta: (:),
  font: "New Computer Modern",
) = {
  if cycle == none {
    panic("umcs-thesis: `cycle` is required; one of " + str(cycles))
  }
  if not cycles.contains(cycle) {
    panic(
      "umcs-thesis: unknown cycle `"
        + cycle
        + "`; expected one of "
        + str(cycles),
    )
  }
  if language != "pl" and language != "en" {
    panic(
      "umcs-thesis: `language` must be \"pl\" or \"en\", got \""
        + language
        + "\"",
    )
  }
  validate-meta(meta)

  set document(title: meta.title, author: meta.author)

  // SRC-001 A4. SRC-003 margins 2.5 cm on all four sides.
  // SRC-008 page number at the bottom, centred.
  set page(
    paper: "a4",
    margin: 2.5cm,
    numbering: "1",
    number-align: center + bottom,
  )

  // SRC-002: 12 pt body. TYP-006: the face is a documented substitute.
  set text(font: font, size: 12pt, lang: "pl")

  // SRC-002: 1.5 line spacing, expressed as leading above a 1em em-box.
  // SRC-007: first-line indent 1.25 cm.
  set par(first-line-indent: 1.25cm, leading: 0.5em, justify: true)

  // SRC-013: Arabic numerals, matching between contents and body.
  set heading(numbering: "1.1")

  // SRC-004: a chapter starts on a new page. APPROXIMATED — the source says
  // the title is separated from the text by "two line spaces"; this uses 2em.
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    equation-counter.update(0)
    // SRC-013: expose the resolved chapter number so a test asserts it
    // instead of reading the rendered text, which carries no number.
    context [
      #metadata((
        number: counter(heading).get().first(),
        title: it.body,
      )) <umcs-chapter>
    ]
    set text(size: 16pt, weight: "bold") // SRC-006: "np. 16 and 14 pt"
    set par(first-line-indent: 0pt)
    block(above: 0cm, below: 2em, it)
  }

  // SRC-005: subsection title with more space above than below.
  // APPROXIMATED — the source gives "1.5 lines above, 1 line below".
  show heading.where(level: 2): it => {
    set text(size: 14pt, weight: "bold")
    set par(first-line-indent: 0pt)
    block(above: 1.5em, below: 1em, it)
  }

  show heading.where(level: 3): it => {
    set text(size: 12pt, weight: "bold")
    set par(first-line-indent: 0pt)
    block(above: 1em, below: 0.5em, it)
  }

  body

  // Machine-readable summary, so a test asserts SRC-021 instead of a reviewer
  // counting by eye.
  context {
    [#metadata((
      cycle: cycle,
      language: language,
      font: font,
      tables: kind-counter("tabela").get().first(),
      figures: kind-counter("rycina").get().first(),
      photographs: kind-counter("fotografia").get().first(),
      abstracts: query(<umcs-abstract>).len(),
      annexes: appendix-counter.get().first(),
    )) <umcs-counters>]
  }
}
