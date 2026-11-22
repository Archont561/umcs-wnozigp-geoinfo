# Assets

## `umcs-logo.png`

The university's eagle-and-wordmark logo, placed on the title page.

**This file is not MIT-licensed.** The MIT grant recorded in ADR-7 covers the
repository's own code and documentation; it does not extend to this image, and
nothing here relicenses it. ADR-18 records the decision to include it and the
open question below. `fonts/` is third-party too, but under a licence that does
permit redistribution — see below.

### Provenance

Extracted on 2026-11-21 from the one-page title-page sample the faculty supplies
with its own guidelines (the sample is cited in SPEC-SOURCE as SRC-045). The
image is the sample's embedded logo XObject, decoded, cropped to its ink, and
downsampled by half. Nothing was redrawn, recoloured, or traced.

Dimensions: 409 × 115 px, drawn 245.4 pt wide on the title page.

### Open question

The sample embeds the logo so that a student can reproduce the required title
page; it does not state a redistribution licence. This repository is public and
its release archives would carry the file, so **redistribution permission is
unresolved**. Settle it before the first release that includes this asset, or
replace the image with a placeholder that carries no institutional mark.

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

The package does not vendor a sans: the sample's heading face (LMSans10-Bold)
cannot be selected through Typst 0.15, which exposes only the wider
`New Computer Modern`. The cover uses the narrowest sans the Pixi environment
ships, and a test asserts the resulting two-line break matches the sample.
