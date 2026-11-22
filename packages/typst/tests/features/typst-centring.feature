Feature: Illustrations are centred on the text column

  The faculty document states no alignment rule for illustrations (SPEC-TYP
  records the omission), so centring is a maintainer choice. These scenarios
  pin that choice down by measuring the rendered page, because the claim is
  about what the reader sees, not about the source that produces it.

  Scenario: A figure is centred with its caption
    Given a document containing only a narrow figure
    When I render the first page and measure its bands of ink
    Then the figure body is centred on the text column
    And the figure caption is centred on the text column

  Scenario: A table is centred with its caption
    Given a document containing only a narrow table
    When I render the first page and measure its bands of ink
    Then the table body is centred on the text column
    And the table caption is centred on the text column

  Scenario: A listing keeps its code left aligned
    Given a document containing only a listing
    When I render the first page and measure its bands of ink
    Then the listing caption is centred on the text column
    And the listing code starts at the left margin like its source line
