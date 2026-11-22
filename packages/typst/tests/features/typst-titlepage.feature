Feature: The title page reproduces the faculty's sample form

  The form is measured from the sample the faculty supplies, not chosen by the
  package: the logo sits in the top-left corner, the university and the faculty
  are sans and left aligned, a vertical rule separates them from the fields,
  and the city and year close the page. These scenarios render the page and
  measure where the ink lands, because the claim is about the page a reader
  gets rather than about the source that produces it.

  Scenario: The mark's box sits in the top-left corner
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then the first band of ink occupies the mark's box at the sample's position

  Scenario: The rule divides the heading from the fields
    Given the demo thesis compiled to a PDF
    When I measure the vertical rule on the title page
    Then the rule spans the sample's range below the heading

  Scenario: The fields are indented past the rule
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then every field starts to the right of the rule

  Scenario: The title is set at the sample's size and face
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then the title is taller than the fields around it, at the sample's size

  Scenario: The university stays on two lines
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then the university heading occupies exactly two lines

  Scenario: A long title does not run into the English title
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then every line of the two titles is separated from the next

  Scenario: The city and year close the page
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then the last band of ink is the city and year, near the bottom

  Scenario: A supplied mark replaces the placeholder
    Given a document supplying its own mark
    When I render its title page and measure the bands of ink
    Then the first band is the supplied image, not the placeholder
