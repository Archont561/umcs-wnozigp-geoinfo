# Assets

## `umcs-logo.png`

**The UMCS logotype** — the official mark of Uniwersytet Marii
Curie-Skłodowskiej w Lublinie (Maria Curie-Skłodowska University, Lublin,
Poland) — placed on the title page as the faculty's sample requires.

| | |
| --- | --- |
| Rightsholder | Uniwersytet Marii Curie-Skłodowskiej w Lublinie, Pl. M. Curie-Skłodowskiej 5, 20-031 Lublin |
| Mark | the **shortened** logotype (`wersja skrócona`): sygnet, dividing rule, `UMCS` wordmark |
| Colour | university grey, 70 % black tint (`#4D4D4D`) — the book's monochrome variant |
| Official download | <https://www.umcs.pl/pl/materialy-ogolnouniwersyteckie,20069.htm> → *Logotyp UMCS - skrócony* |
| Rules | UMCS *Księga Identyfikacji Wizualnej* (2024, v02), <https://phavi.umcs.pl/at/attachments/2024/0726/085914-kiw-umcs-2024v02.pdf> |

**This file is not MIT-licensed.** The MIT grant recorded in ADR-7 covers the
repository's own code and documentation; it does not extend to this image, and
nothing here relicenses it. `fonts/` is third-party too, but under a licence
that does permit redistribution — see below.

### What was reproduced, and what was copied

Extracted on 2026-11-21 from the one-page title-page sample the faculty
supplies with its own guidelines (the sample is cited in SPEC-SOURCE as
SRC-045). The image is the sample's embedded logo XObject, decoded, cropped to
its ink, and downsampled by half. **Nothing was redrawn, recoloured, or
traced**: the grey is the mark's own 70 % black tint and the proportions are
the logotype's.

Consequently this file is a *re-encoding* of UMCS's artwork, not a copy of the
university's download archive, and it will not be byte-identical to the PNG or
SVG in that archive.

Dimensions: 409 × 115 px, drawn 245.4 pt (86.6 mm) wide on the title page. The
book sets a minimum print width of 45 mm, so the cover is inside the rule, and
the mark is neither distorted nor rearranged.

### Licence status

The university publishes the logotype for download and states how it is to be
used, including a section for a thesis title page (§4.7 *Praca dyplomowa –
strona tytułowa*). **Publishing a file for download is not a redistribution
licence**, and the site reserves all rights, so this repository's right to
redistribute the mark remains **unresolved** — but the question is now routed
correctly: the rightsholder is UMCS and the contact is Centrum Promocji UMCS,
which supplies the identity system. Settle it before the first release that
includes this asset, or replace the image with a placeholder that carries no
institutional mark.

Two things this asset is *not*. It is the **university** mark, not the
faculty's: the book treats them as separate marks in one family (§2.1.1) and
lists "placing the university and faculty logos side by side" as a misuse, so
if the faculty ever requires its own mark that is a second asset and a second
decision. And it carries no tagline, because the design in use here is the
shortened logotype rather than the primary one.

A submission that uses the package is reproducing a form the faculty requires,
which is a different question from this repository redistributing the artwork.

## `fonts/`

Vendored so the title page can use the same typeface as the faculty's sample.

### `TeXGyreTermes-{Regular,Bold,Italic}.otf`

TeX Gyre Termes, the URW Nimbus Roman clone of Times that the sample's fields
and title are set in. Including it is what lets the reproduced title sit at the
sample's width instead of overflowing the right margin; the alternative,
Typst's `New Computer Modern`, is about 14 % wider for the same string.

- **Licence: GUST Font License (LPPL 1.3c).** Full text in `LICENSE-GUST.txt`,
  which travels with the fonts. The GUST licence permits redistribution and
  modification while requiring that modified versions not use the reserved
  names; these are unmodified upstream files, so that clause does not bite.
- **Provenance:** TeX Gyre Termes 2.004, upstream
  `https://www.gust.org.pl/projects/e-foundry/tex-gyre/termes/qtm2.004otf.zip`.
  Obtained from the `@quillmark/fonts` npm package, whose manifest records the
  same upstream URL and hashes.
- **Not MIT.** Like the logo, these files are third-party material that the
  repository's MIT grant does not cover. Unlike the logo, their licence
  *does* permit redistribution, so there is no open question here.

The package also sets the **body** in Termes rather than `New Computer Modern`,
because SRC-002 asks for Times New Roman and Termes is its metric-compatible
clone. That substitution has a cost the package records rather than hides:
Termes is narrower, so a line of body text holds about 92 characters where the
source asks for ~70 — a figure the source's own 12 pt and 2.5 cm margins make
unreachable (SPEC-SOURCE records the arithmetic). A test pins the measured
value.

The package does not vendor a sans: the sample's heading face (LMSans10-Bold)
cannot be selected through Typst 0.15, which exposes only the wider
`New Computer Modern`. The cover uses the narrowest sans the Pixi environment
ships, and a test asserts the resulting two-line break matches the sample.
