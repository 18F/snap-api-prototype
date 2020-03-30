# Results checked against the Illinois Department of Human Services
# Potential SNAP Eligibility calculator:
#
# http://fscalc.dhs.illinois.gov/FSCalc/calculateFS.do
#
# Some calculations result in small differences, which may be due
# to rounding differences or slightly different data sets being used.

# A few surprising results from the Illinois calculator:
# * Standard deduction listed as $160 instead of $167.
# * Family of 3 with an elderly or disabled household member, medical expenses
#   of $135 lists Medical Deduction as $165 instead of $100.

Feature: Testing SNAP Financial Factors Web API for IL

  Scenario:
    Given the household is in IL
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $194 per month

  Scenario:
    Given the household is in IL
    And a 2-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $355 per month

  Scenario:
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $509 per month

  Scenario:
    Given the household is in IL
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Household (just barely) fails the Gross Income test for IL (165% FPL),
            passes the Net Income Test, is overall ineligible
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has dependent care costs of $300 monthly
    And the household has rent or mortgage costs of $2000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Minimum allotment
    Given the household is in IL
    And a 1-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $1040 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $16 per month

  Scenario: Minimum allotment does not apply to larger household
    Given the household is in IL
    And a 4-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $0 monthly
    And the household has other income of $2323 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Earned income
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $317 per month

  Scenario: Both earned income and other income
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $287 per month

  Scenario: Dependent care deduction
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has dependent care costs of $100 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $317 per month

  Scenario: Medical expenses of $0 do not affect benefit amount
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $0 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $341 per month

  Scenario: Medical expenses of $35 do not affect benefit amount
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $35 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $341 per month

  Scenario: Medical expenses of $135 increase benefit by $30
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $135 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $371 per month

  Scenario: Medical expenses do not affect benefit if household does not include an elderly or disabled member
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $400 monthly
    And the household has other income of $400 monthly
    And the household has assets of $0
    And the household has medical expenses for elderly or disabled members of $135 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $341 per month

  Scenario: Household passes net income test but not gross income test
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    When we run the benefit estimator...
      Then we find the family is likely not eligible
      And we find the estimated benefit is $0 per month

  Scenario: Child support payments exclusion pushes household into eligibility
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    And the household has court-ordered child support payments of $100 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $47 per month

  Scenario: More child support payments increase estimated benefit
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $1000 monthly
    And the household has other income of $2000 monthly
    And the household has assets of $1000
    And the household has dependent care costs of $1000 monthly
    And the household has court-ordered child support payments of $400 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $137 per month

  Scenario: Household where shelter costs do not exceed half of adjusted income
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $300 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $287 per month

  Scenario: Household where shelter costs exceed half of adjusted income by ~$100
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $467 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $316 per month

  Scenario: Household where shelter costs exceed half of adjusted income by ~$100 and the household includes an elderly or disabled household member
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $467 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $316 per month

  Scenario: Household where shelter costs exceed half of adjusted income by ~$200
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $567 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $346 per month

  Scenario: Household with excess shelter costs that exceed the IL 2020 max ($569) that includes an elderly or disabled household member
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1067 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $496 per month

  Scenario: Household with excess shelter costs that exceed the IL 2020 max ($569) that does not include an elderly or disabled household member
    Given the household is in IL
    And a 3-person household
    And the household does not include an elderly or disabled member
    And the household has earned income of $500 monthly
    And the household has other income of $500 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1067 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $458 per month

  Scenario: Household that would have a low benefit amount without taking utilities into account
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $41 per month

  Scenario: Household pays for AC or heat separately
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays for AC or heat (or otherwise qualifies for AC/heat utility allowance)
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $184 per month

  Scenario: Household pays for two utilities besides AC and heat
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays for water and trash collection (or otherwise qualifies for limited utility allowance)
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $139 per month

  Scenario: Household pays a single utilities besides AC, heat, and phone
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays for a single utility besides AC, heat, and phone
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $63 per month

  Scenario: Household pays for telephone only
    Given the household is in IL
    And a 3-person household
    And the household does include an elderly or disabled member
    And the household has earned income of $3000 monthly
    And the household has other income of $0 monthly
    And the household has assets of $0
    And the household has rent or mortgage costs of $1800 monthly
    And the household pays phone bills only
    When we run the benefit estimator...
      Then we find the family is likely eligible
      And we find the estimated benefit is $50 per month
