Feature: Testing SNAP Financial Factors Web API for UT

  Scenario:
    Given the household is in UT
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario: Household passes net income test but not gross income test
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000 monthly
    And the household has dependent care costs of $1000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month
