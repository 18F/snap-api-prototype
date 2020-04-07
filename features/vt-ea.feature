Feature: VT scenarios with EA (Emergency Allotment) waiver

  Background:
    Given the household is in VT
    Given an emergency allotment waiver

  Scenario:
    Given a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario: Household that would (just barely) fail the Gross Income test if
            they lived in IL (165% FPL), passes Gross and Net Income Test,
            is overall eligible, and receives max allotment because of
            VT emergency SNAP allotment waiver
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has dependent care costs of $300 monthly
    And the household has rent or mortgage costs of $2000 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month
