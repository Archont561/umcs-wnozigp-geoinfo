# Assets

The package bundles **one** third-party asset: the body and cover typeface.
It bundles no institutional mark, by design — see `packages/typst/README.md`.

## `fonts/`

Vendored so the title page and the body can use the same typeface as the
faculty's sample.

### `TeXGyreTermes-{Regular,Bold,Italic}.otf`

TeX Gyre Termes, the URW Nimbus Roman clone of Times that the sample's fields
and title are set in, and the package's default body face. Including it is what
lets the reproduced title sit at the sample's width instead of overflowing the
right margin, and what gives the body Times's letterforms; the alternative,
Typst's `New Computer Modern`, is about 14 % wider and is not a Times design at
all.

- **Licence: GUST Font License (LPPL 1.3c).** Full text in `LICENSE-GUST.txt`,
  which travels with the fonts. The GUST licence permits redistribution and
  modification while requiring that modified versions not use the reserved
  names; these are unmodified upstream files, so that clause does not bite.
- **Provenance:** TeX Gyre Termes 2.004, upstream
  `https://www.gust.org.pl/projects/e-foundry/tex-gyre/termes/qtm2.004otf.zip`.
  Obtained from the `@quillmark/fonts` npm package, whose manifest records the
  same upstream URL and hashes.
- **Not MIT.** These files are third-party material that the repository's MIT
  grant does not cover. Unlike the university's logotype, their licence *does*
  permit redistribution, so there is no open question here.

The package does not vendor a sans: the sample's heading face (LMSans10-Bold)
cannot be selected through Typst 0.15, which exposes only the wider
`New Computer Modern`. The cover uses the narrowest sans the Pixi environment
ships, and a test asserts the resulting two-line break matches the sample.

## No institutional mark

`umcs-logo.png` and its notice were removed. UMCS publishes its logotype for
download and governs its use, but publishing a download is not a redistribution
licence and the site reserves all rights, so the package stopped shipping the
file rather than waiting for an answer (ADR-19). A caller supplies their own
copy of the university's official file through the `logo` parameter; without
one, the title page draws a placeholder box of exactly the same size, so the
geometry is unchanged and the omission is visible rather than silent.
