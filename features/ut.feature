Feature: UT scenarios without an EA (Emergency Allotment) waiver

  Background:
    Given the household is in UT
    Given no emergency allotment waiver

  Scenario:
    Given a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario: Household passes net income test but not gross income test
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2400 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Child support payments deduction does not push household into eligibility
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2400 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    And the household has court-ordered child support payments of $100 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month
