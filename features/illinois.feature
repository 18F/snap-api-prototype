Feature: Testing SNAP Financial Factors Web API for IL

  Scenario:
    Given the household is in IL
    Given a 1-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $0 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator...
     Then we find the family is likely eligible
     Then we find the estimated benefit is $194 per month

  Scenario:
    Given the household is in IL
    Given a 2-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $0 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator...
     Then we find the family is likely eligible
     Then we find the estimated benefit is $355 per month

  Scenario:
    Given the household is in IL
    Given a 3-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $0 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator...
     Then we find the family is likely eligible
     Then we find the estimated benefit is $509 per month

  Scenario:
    Given the household is in IL
    Given a 1-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $2000 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator...
     Then we find the family is likely not eligible
     Then we find the estimated benefit is $0 per month

   Scenario: Minimum allotment
     Given the household is in IL
     Given a 1-person household
     Given the household does not include an elderly or disabled member
     Given the household has income of $1040 monthly
     Given the household has assets of $0 monthly
      When we run the benefit estimator...
      Then we find the family is likely eligible
      Then we find the estimated benefit is $16 per month

    Scenario: Minimum allotment does not apply to larger household
      Given the household is in IL
      Given a 4-person household
      Given the household does not include an elderly or disabled member
      Given the household has income of $2323 monthly
      Given the household has assets of $0 monthly
       When we run the benefit estimator...
       Then we find the family is likely eligible
       Then we find the estimated benefit is $2 per month
