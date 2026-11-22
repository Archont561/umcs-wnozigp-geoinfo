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
    listings: "Spis listingów",
    annex: "Załącznik",
    appendix-heading: "Załączniki",
    table: "Tabela",
    figure: "Rycina",
    listing: "Listing",
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
    listings: "List of listings",
    annex: "Annex",
    appendix-heading: "Annexes",
    table: "Table",
    figure: "Figure",
    listing: "Listing",
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

/// The sample is typeset in Computer Modern. Its fields — including the title —
/// are **TeXGyreTermes-Regular**, which the package vendors under
/// `assets/fonts/` with its GUST licence because it is what makes the width of
/// the reproduced title match the sample's instead of overflowing the margin.
/// Its university and faculty lines are **LMSans10-Bold**, which Typst 0.15
/// cannot select by that name: it exposes only `New Computer Modern` (a
/// different, wider design) and silently ignores `Latin Modern Sans`. So the
/// heading keeps `Ubuntu`, the narrowest sans the environment ships, because
/// only a narrow face keeps the sample's two-line break instead of wrapping to
/// three.
///
/// That one substitution is asserted, not assumed: the title-page scenarios
/// require the university block to stay two lines.
#let cover-sans = "Ubuntu"
#let cover-serif = "TeXGyreTermes"

/// The body face. SRC-002 asks for Times New Roman 12 pt; Times New Roman is
/// proprietary and cannot ship here, so the package sets the body in TeX Gyre
/// Termes, the metric-compatible Times clone it already vendors for the cover
/// (TYP-006: a substitution must be documented, and no build may claim SRC-002
/// compliance on a substitute).
///
/// Termes is narrower than the `New Computer Modern` it replaced, so a fixed
/// text width carries *more* characters per line, not fewer: about 92 against
/// New Computer Modern's 84 at A4 with 2.5 cm margins. SRC-002 also asks for
/// ~70, which no available face reaches at 12 pt and 16 cm; a test pins the
/// measured value so narrowing the measure becomes a deliberate decision
/// rather than an accident.
#let body-font = "TeXGyreTermes"

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
// Three independent sequences, one per registered class: tables, figures and
// listings. A `figure` element cannot do this alone: Typst numbers figures per
// `kind`, but it puts every caption in one place and offers no
// caption-position control, while the caption belongs above for tables and
// listings and below for figures (SRC-015 vs SRC-018). Explicit counters make
// every sequence queryable, which is what turns a numbering rule into a
// tested assertion.
//
// OWNER DECISION (2026-11-21), diverges from SRC-021: the faculty document
// names three classes — tables, figures and *photographs* — each with its own
// index. The repository owner directed that photographs be folded into figures
// and that "Spis fotografii" not exist, so a photograph is inserted as an
// ordinary `figure-with-source` and numbered with the figures. Listings are
// added as the third class in their place. This is a deliberate deviation, not
// an oversight, and it must be re-checked if the faculty text is revised.
// ---------------------------------------------------------------------------

#let kind-counter(kind) = counter("umcs-illustration-" + kind)

#let numbering-start = counter(page)

// ---------------------------------------------------------------------------
// Title page (SRC-012, SRC-045)
// ---------------------------------------------------------------------------

/// The normalised title page, field order per the Annex 1 sample (SRC-045).
/// Carries no page number (SRC-008).
///
/// The geometry is measured from the faculty's own sample rather than chosen:
/// the logo's ink starts 52 pt from the left edge and 70.5 pt from the top, the
/// university and faculty are sans and sit on a 119.5 pt left edge, a 1 pt rule
/// runs from x = 118 pt between 292.9 pt and 709.2 pt below the top edge, and
/// every field is indented 13.5 pt past that rule.
///
/// The page is laid out with `place` at absolute positions rather than as a
/// flow, because a title page is a fixed form: its fields do not reflow, and
/// the sample's own coordinates are the only defensible source for where each
/// one belongs.
///
/// Each line takes the distance from the top of the page to the top of its ink,
/// computed from the sample's baseline. `size` does two things and both are
/// needed: it sets the type size, and it converts the baseline to a top offset
/// through the face's ascent. An earlier version used it only for the offset,
/// which drew the title at the body's 12 pt instead of 24.79 pt.
// A4 height, used to convert the sample's baselines (measured up from the
// bottom edge, as PDF coordinates are) into distances from the top.
#let a4-height = 841.89pt

// 0.760 is the ratio measured on the sample's own faces: at 11.96 pt the
// ascender puts the ink 9.1 pt above the baseline, and that scales with size.
// Widths are explicit because `place` otherwise offers unbounded room, so a
// long title would run past the margin instead of wrapping where the sample's
// would.
//
// Titles and bottom block: the sample's text ends at x = 510.4 pt and these
// blocks start at 133 pt, so 377 pt reaches the same right edge.
#let cover-width = 377pt
// Headings: the sample starts them at 119.5 pt and its faculty line ends at
// 510 pt, i.e. 391 pt. Ubuntu is about 3.5 % wider than the sample's LMSans10,
// so the substitute needs 405 pt for the same words; allowing 420 pt keeps the
// faculty on the one line the sample gives it, which matters more than ending
// at the sample's exact x — a wrapped faculty line reads as a different form.
#let cover-heading-width = 420pt

#let cover-page-baseline(baseline-from-bottom, size, body) = place(
  top + left,
  dx: 133pt,
  dy: a4-height - baseline-from-bottom - 0.760 * size,
  block(width: cover-width, {
    set text(size: size, font: cover-serif)
    body
  }),
)

#let coverpage(meta, cycle, language: "pl") = {
  let s = strings.at(language)
  let cycle-name = if language == "en" {
    cycle-names-en.at(cycle)
  } else {
    cycle-names-pl.at(cycle)
  }
  // SRC-012 lists the programme, not the specialisation, and the sample
  // carries one line only, so a specialisation is printed after the fields.
  let programme = meta.at("programme", default: "")
  let specialisation = meta.at("specialisation", default: "")

  // The heading is placed by its own coordinates rather than through
  // `cover-page-baseline`, because it sits on a different left edge.
  let heading(baseline, size, body) = place(
    top + left,
    dx: 119.5pt,
    dy: a4-height - baseline - 0.760 * size,
    block(width: cover-heading-width, {
      set text(size: size, weight: "bold", font: cover-sans)
      body
    }),
  )

  page(margin: 0pt, numbering: none)[
    #set par(first-line-indent: 0pt, leading: 1.2em, justify: false)
    #set text(size: 11.96pt, font: cover-serif)

    // The UMCS logotype (shortened variant, university grey). It is the
    // university's mark, not this package's: its attribution, the identity
    // rules that govern it, and its unresolved redistribution terms are in
    // assets/UMCS-LOGO-NOTICE.md. 86.6 mm wide, which is inside the identity
    // book's 45 mm minimum print width.
    #place(top + left, dx: 52pt, dy: 70.5pt, image(
      "assets/umcs-logo.png",
      width: 245.4pt,
    ))
    // The rule does not start under the logo: in the sample it begins level
    // with the "Kierunek" line and ends just below "pod kierunkiem".
    #place(top + left, dx: 118pt, dy: 292.9pt, box(
      width: 1pt,
      height: 416.3pt,
      fill: black,
    ))

    // The university and the faculty: sans, bold, at the sample's sizes and
    // with the sample's own line break.
    #heading(659.2pt, 20.66pt)[Uniwersytet Marii Curie-Skłodowskiej]
    #heading(634.7pt, 20.66pt)[w Lublinie]
    #heading(598.8pt, 17.22pt)[Wydział Nauk O Ziemi i Gospodarki Przestrzennej]

    // The fields. Serif, at the sample's sizes and intervals.
    #cover-page-baseline(525.5pt, 11.96pt)[#s.programme: #programme]
    // The sample has no specialisation field, so it is printed as a second
    // identifier line rather than appended to the three-line bottom block,
    // which the sample fixes at exactly three lines.
    #if specialisation != "" {
      cover-page-baseline(503.0pt, 11.96pt)[
        #s.specialisation: #specialisation
      ]
    }
    #cover-page-baseline(475.5pt, 17.22pt)[#meta.author]
    #cover-page-baseline(452.7pt, 11.96pt)[#s.album: #meta.album]
    // The two titles share one placed block so the gap between them is a
    // property of the block and not of two independent baselines: in the
    // sample both are one line, but a title long enough to wrap must push the
    // English one down by its own height rather than run into it.
    #place(
      top + left,
      dx: 133pt,
      dy: a4-height - 388.5pt - 0.760 * 24.79pt,
      block(width: cover-width, {
        set par(leading: 1.05em)
        set text(size: 24.79pt, font: cover-serif)
        meta.title
        // 21 pt is the sample's ink gap between the two titles.
        v(9pt)
        set text(size: 14.35pt)
        meta.at("title-en")
      }),
    )
    #cover-page-baseline(274.3pt, 11.96pt)[#s.thesis (#cycle-name)]
    #cover-page-baseline(252.6pt, 11.96pt)[
      #s.written-in #meta.department
    ]
    #cover-page-baseline(230.9pt, 11.96pt)[
      #s.supervised-by #meta.supervisor
    ]
    // City and year, below the rule.
    #cover-page-baseline(95.7pt, 11.96pt)[
      #meta.at("city", default: "Lublin") #meta.at("year", default: "2027")
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
  // SRC-016/SRC-019: 10 pt italic, left aligned, after the object. Spacing is
  // explicit for the same reason as the caption: a block's `above`/`below` is
  // discarded at a container boundary, which made the gap between a source
  // line and the next paragraph vary from illustration to illustration.
  v(0.5em, weak: false)
  block(width: 100%)[
    #set text(size: 10pt, style: "italic")
    #set par(first-line-indent: 0pt, leading: 0.65em)
    #set align(left)
    #source
  ]
  v(0.75em, weak: false)
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

/// Caption styling shared by the three illustration classes.
///
/// The source is silent on horizontal alignment for illustrations, so centred
/// is a maintainer choice, recorded in SPEC-TYP. Table and listing sources
/// stay left aligned because SRC-016 says so explicitly.
#let illustration-caption(prefix, n, caption, gap: 0.5em) = {
  // Spacing is an explicit, non-weak `v()`, not `block(above: …)`: a block's
  // own spacing is discarded when it starts a container, which made the
  // caption collide with the object beneath it. A weak `v()` additionally
  // collapses against paragraph spacing, which produced the uneven gaps
  // between captions and following paragraphs.
  v(gap, weak: false)
  // `width: 100%` as well: a bare `block` shrinks to its content, and
  // `set align(center)` then has nothing to centre within.
  block(width: 100%)[
    #set text(size: 10pt, weight: "bold")
    #set par(first-line-indent: 0pt, leading: 0.65em, justify: false)
    #set align(center)
    #prefix #n: #caption
  ]
}

/// Centres the object inside the text block without forcing a width, so a
/// `#rect(width: 40%)` or a narrow `#table` sits in the middle of the line.
#let illustration-body(body) = align(center, body)

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
    // `width: 100%` is required: an unbreakable block shrinks to its content,
    // so an inner `align(center)` would have no free width and the object
    // would sit flush left instead of centred.
    block(breakable: false, width: 100%)[
      // SRC-018: caption below, 10 pt bold, single spacing. Centring is a
      // maintainer choice; the source does not state an alignment.
      #illustration-body[#body]
      #if caption != none { illustration-caption(s, n, caption) }
      // The source line belongs inside the unbreakable block: left outside it,
      // a page break could strand "opracowanie własne" alone at the top of the
      // next page, separated from the illustration it annotates.
      #source-line("rycina", source)
    ]
  }
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
    // `width: 100%`: see the note in `figure-with-source`.
    block(breakable: false, width: 100%)[
      #if caption != none { illustration-caption(s, n, caption, gap: 1.5em) }
      #align(center)[
        #block[
          #set text(size: 10pt)
          #set par(first-line-indent: 0pt, leading: 0.65em)
          #body
        ]
      ]
      #source-line("tabela", source)
    ]
  }
}

/// A listing: source code or a data extract, numbered with its own sequence.
///
/// The caption sits above the block, the way a table's does, because a listing
/// is read top-down and the reader needs to know what it is before the code.
#let listing(
  body,
  source: none,
  caption: none,
) = {
  kind-counter("listing").step()
  context {
    let n = kind-counter("listing").get().first()
    let s = strings.pl.listing
    register-illustration("listing", n, caption)
    // `width: 100%`: see the note in `figure-with-source`.
    block(breakable: false, width: 100%)[
      #if caption != none { illustration-caption(s, n, caption, gap: 1.5em) }
      // The caption is centred but the code itself stays left aligned: a
      // centred code block would misalign its own indentation.
      #block(width: 100%)[
        #set text(size: 9pt)
        #set par(first-line-indent: 0pt, leading: 0.65em, justify: false)
        #set align(left)
        #body
      ]
      #source-line("listing", source)
    ]
  }
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
#let list-of-listings() = illustration-index(
  "listing",
  strings.pl.listings,
  strings.pl.listing,
)

// ---------------------------------------------------------------------------
// Annexes (SRC-024, SRC-025)
// ---------------------------------------------------------------------------

#let appendix-counter = counter("umcs-appendix")

/// A reference to an annex, e.g. `#annex-ref(2)` renders "Załącznik 2".
///
/// Typst's `ref` cannot target a label applied to a function that returns
/// several elements ("cannot reference sequence"), and every attempt to wrap
/// the annex in a single element either floated the content or refused the
/// page break inside a container. A counter-driven helper is the honest
/// workaround: it renders the right text and is testable, at the cost of not
/// being a live `ref` that renumbers itself. Recorded as a limitation.
#let annex-ref(n) = [#strings.pl.annex #n]

/// One annex. The label sits in the page header, top right (SRC-024), and the
/// annex starts on a new page.
#let appendix(title: none, body) = {
  appendix-counter.step()
  // The header is applied by a page break followed by a `page()` wrapper. That
  // combination previously emitted a blank page when a level-1 heading was
  // also inside the wrapper, so the annex title is a styled block, not a
  // heading, and the break happens outside the container.
  pagebreak(weak: true)
  context [
    #let n = appendix-counter.get().first()
    #let label = strings.pl.annex
    #page(header: align(right)[#text(size: 10pt)[#label #n]])[
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
  font: body-font,
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
      listings: kind-counter("listing").get().first(),
      abstracts: query(<umcs-abstract>).len(),
      annexes: appendix-counter.get().first(),
    )) <umcs-counters>]
  }
}
