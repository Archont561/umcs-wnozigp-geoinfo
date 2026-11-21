Feature: Smoke-build the Typst placeholder

  Scenario: Build the Typst dummy through its Tasknest task
    Given the Typst package contains its dummy main
    When I run the Typst Tasknest build
    Then the Typst smoke PDF is written under dist
    And the Typst PDF has a valid header and trailer
