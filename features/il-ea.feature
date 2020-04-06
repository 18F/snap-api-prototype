Feature: Illinois scenarios with EA (Emergency Allotment) waiver

  Background:
    Given the household is in IL
    Given an emergency allotment waiver

  Scenario: Eligible 1-person household receives the max benefit for household size
    Given a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario: Eligible 2-person household receives the max benefit for household size
    Given a 2-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $355 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario:
    Given a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Household (just barely) fails the Gross Income test for IL (165% FPL),
            passes the Net Income Test, is overall ineligible
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has dependent care costs of $300 monthly
    And the household has rent or mortgage costs of $2000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Eligible 1-person household receives the max benefit for household size
    Given a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $1040 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario: Minimum allotment does not apply to larger household
    Given a 4-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2323 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has dependent care costs of $100 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $35 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $135 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $135 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Household passes net income test but not gross income test
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    And the household has court-ordered child support payments of $100 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    And the household has court-ordered child support payments of $400 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $300 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $467 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $467 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $567 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1067 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1067 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays for AC or heat (or otherwise qualifies for AC/heat utility allowance)
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays for water and trash collection (or otherwise qualifies for limited utility allowance)
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays for a single utility besides AC, heat, and phone
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays phone bills only
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario: Eligible 3-person household receives the max benefit for household size
    Given a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household is not billed separately for any utilities
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month
