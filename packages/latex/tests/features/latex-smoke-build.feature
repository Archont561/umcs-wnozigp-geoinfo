Feature: Smoke-build the LaTeX placeholder

  Scenario: Build the LaTeX dummy through its Tasknest task
    Given the LaTeX package contains its dummy main
    When I run the LaTeX Tasknest build
    Then the LaTeX smoke PDF is written under dist
    And the LaTeX PDF has a valid header and trailer
