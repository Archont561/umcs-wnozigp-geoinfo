Feature: The Typst package renders the faculty's structural rules

  These scenarios assert what the faculty document actually says, using the
  package that implements SPEC-TYP. They are not a compliance certificate:
  ADR-9 records that no faculty reviewer has approved the output, and
  ADR-10 records that the 2025/26 rules are a proxy for the 2026/27 cohort.

  Scenario: The package compiles its demo thesis
    Given the Typst package has a demo main
    When I compile the demo main with Typst
    Then the compiled PDF has a valid header and trailer

  Scenario: The illustration counters run independently
    Given the Typst package has a demo main
    When I query the document counters
    Then the counters report one table, two figures and one listing

  Scenario: Every illustration carries a source
    Given the Typst package has a demo main
    When I query the registered illustrations
    Then every illustration reports a source and a caption
    And every illustration carries a per-kind sequence number

  Scenario: The abstract character count is reported
    Given the Typst package has a demo main
    When I query the abstract
    Then the abstract reports a character count within the faculty limit

  Scenario: An unknown configuration key is rejected
    Given a document setting an unknown meta key
    When I compile it with Typst
    Then the compiler fails and names the offending key

  Scenario: A missing cycle is rejected
    Given a document omitting the cycle
    When I compile it with Typst
    Then the compiler fails and says the cycle is required

  Scenario: An illustration without a source is rejected
    Given a document with an unsourced figure
    When I compile it with Typst
    Then the compiler fails and says the source is required

  Scenario: Photographs have no separate class or index
    Given the Typst package has a demo main
    When I query the document counters
    Then no photograph counter is reported

  Scenario: The contents numbering matches the body
    Given the Typst package has a demo main
    When I query the chapters
    Then the first chapter is numbered one

  Scenario: The body is set in the vendored Times substitute
    Given the Typst package has a demo main
    When I query the document counters
    Then the body face is the vendored Times substitute
    And the body face is not the wider Computer Modern

  Scenario: Body text fits about 92 characters on a line
    Given the Typst package has a demo main
    When I query the document counters
    And I measure a line of body text at the document's own settings
    Then the measured characters per line is about 92

  Scenario: A page holds about 39 lines at the source's own settings
    Given the Typst package has a demo main
    When I query the document counters
    And I measure a line of body text at the document's own settings
    Then a page holds about 39 lines
