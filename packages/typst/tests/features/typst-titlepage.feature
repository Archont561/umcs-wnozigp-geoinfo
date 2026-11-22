Feature: The title page reproduces the faculty's sample form

  The form is measured from the sample the faculty supplies, not chosen by the
  package: the logo sits in the top-left corner, the university and the faculty
  are sans and left aligned, a vertical rule separates them from the fields,
  and the city and year close the page. These scenarios render the page and
  measure where the ink lands, because the claim is about the page a reader
  gets rather than about the source that produces it.

  Scenario: The logo sits in the top-left corner
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then the first band of ink is the logo, at the sample's position

  Scenario: The rule divides the heading from the fields
    Given the demo thesis compiled to a PDF
    When I measure the vertical rule on the title page
    Then the rule spans the sample's range below the heading

  Scenario: The fields are indented past the rule
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then every field starts to the right of the rule

  Scenario: The city and year close the page
    Given the demo thesis compiled to a PDF
    When I render the title page and measure its bands of ink
    Then the last band of ink is the city and year, near the bottom
