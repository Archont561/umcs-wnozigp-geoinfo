// Demo thesis using the package in `lib.typ`.
//
// This file is a fixture: it is excluded from the release tarball and exists
// so CI can compile the package and so a reader can see the intended usage.
// The content is synthetic. Every reference, figure and table here is a
// placeholder, not a real citation or dataset.
//
// Build:  pixi run --locked build-typst
// Check:  pixi run --locked lint-typst

#import "lib.typ": *

#let meta = (
  programme: "Geoinformatyka",
  specialisation: "Systemy informacji geograficznej",
  author: "Imię Nazwisko",
  album: "102030",
  title: "Analiza zmian pokrycia terenu w zlewni Bystrzycy",
  title-en: "Land-cover change analysis in the Bystrzyca catchment",
  supervisor: "dr hab. Jan Przykładowy",
  department: "Katedra Geoinformacji i Kartografii",
  city: "Lublin",
  year: "2027",
)

#show: umcs-thesis.with(
  cycle: "magisterska",
  meta: meta,
)

#coverpage(meta, "magisterska")
#pagebreak()
#contents()
#pagebreak()

#front-matter-heading(strings.pl.abstract)
#abstract[
  Praca dotyczy zmian pokrycia terenu w zlewni Bystrzycy w latach 2010–2025.
  Wykorzystano zdjęcia lotnicze i dane satelitarne. Wyniki wskazują na wzrost
  udziału terenów zabudowanych kosztem użytków rolnych. Wszystkie liczby
  w tym streszczeniu są przykładowe i nie pochodzą z rzeczywistego badania.
]

= Wstęp

Praca dyplomowa jest dokumentem, w którym student wykazuje umiejętność
samodzielnego prowadzenia badań. Ten akapit istnieje wyłącznie po to, żeby
pokazać układ tekstu: wcięcie akapitu 1,25 cm, interlinia półtora wiersza i
wyrównanie obustronne.

#heading(level: 2)[Cel i zakres pracy]

Celem pracy jest ocena zmian pokrycia terenu. Zakres obejmuje analizę
wieloczasową i walidację terenową.

= Przegląd literatury

Przegląd literatury jest zalecany w pracach drugiego stopnia.

= Materiały i metody

Dane pozyskano z krajowego systemu informacji geograficznej. Poniższa rycina
pokazuje schemat postępowania.

#figure-with-source(
  caption: [Schemat postępowania badawczego],
  source: own-work("dane własne"),
)[
  #rect(width: 100%, height: 3cm, stroke: 0.5pt, fill: luma(245))
]

Zestawienie zbiorów danych przedstawia tabela poniżej.

#table-with-source(
  caption: [Zestawienie wykorzystanych zbiorów danych],
  source: [opracowanie własne],
)[
  #table(
    columns: 3,
    align: left,
    stroke: 0.5pt,
    [*Zbiór*], [*Rok*], [*Rozdzielczość*],
    [Ortofotomapa], [2010], [0,25 m],
    [Ortofotomapa], [2025], [0,10 m],
    [Dane satelitarne], [2020], [10 m],
  )
]

Zdjęcie dokumentuje punkt kontrolny. Jest wstawione jako rycina, bo osobna
klasa „fotografia” i jej spis nie są w tej wersji przewidziane.

#figure-with-source(
  caption: [Punkt kontrolny nr 3 w dolinie Bystrzycy],
  source: after("dokumentacja własna"),
)[
  #rect(width: 100%, height: 3cm, stroke: 0.5pt, fill: luma(245))
]

Listing poniżej pokazuje fragment kodu obliczeniowego.

#listing(
  caption: [Obliczenie wskaźnika zmiany pokrycia],
  source: own-work("skrypt własny"),
)[
  #raw(
    lang: "python",
    block: true,
    "delta = (a2 - a1) / a1 * 100",
  )
]

#heading(level: 2)[Modelowanie]

Równanie poniżej pokazuje prosty wskaźnik zmiany.

#equation-numbered[
  $ "ΔA" = (A_2 - A_1) / A_1 dot 100% $
]

= Wyniki

Wyniki przedstawiono w podziale na klasy pokrycia terenu.

= Dyskusja

Dyskusja odnosi wyniki do literatury przedmiotu.

= Wnioski

#list-of-figures()
#list-of-tables()
#list-of-listings()

#appendices[
  #appendix(title: [Wykaz punktów kontrolnych])[
    Wszystkie punkty kontrolne zestawiono w tabeli w wersji elektronicznej.
  ]
  #appendix(title: [Skrypt obliczeniowy])[
    Kod źródłowy obliczeń wskaźnika zmiany. Patrz listing 1.
  ]
]

Odwołanie do załączników: #annex-ref(1) i #annex-ref(2).
