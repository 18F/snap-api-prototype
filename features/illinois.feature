# Results checked against the Illinois Department of Human Services
# Potential SNAP Eligibility calculator:
#
# http://fscalc.dhs.illinois.gov/FSCalc/calculateFS.do
#
# Some calculations result in small differences, which may be due
# to rounding differences or slightly different data sets being used.


Feature: Testing SNAP Financial Factors Web API for IL

  Scenario:
    Given the household is in IL
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario:
    Given the household is in IL
    And a 2-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $355 per month

  Scenario:
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario:
    Given the household is in IL
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Minimum allotment
    Given the household is in IL
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $1040 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $16 per month

  Scenario: Minimum allotment does not apply to larger household
    Given the household is in IL
    And a 4-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2323 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $2 per month

  Scenario: Earned income
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $319 per month

  Scenario: Both earned income and other income
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $289 per month
