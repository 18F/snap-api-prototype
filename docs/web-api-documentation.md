# Web API

The web API has one endpoint. The `calculate` end point accepts inputs about a household (such as state or territory, household size, income information and deductible costs information) and returns an estimate for that household's SNAP eligibility, an estimated benefit amount, and explanation of all the logic behind the API's decision-making, plus a link to a state website where a household could apply for SNAP.

Note that not all U.S. states are supported by the prototype API at this stage.

| State | Notes | Standard Utility Allowance data included? |
| ------|-------|-------------------------------------------|
| CA    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | Not yet |
| ID    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | Not yet |
| IL    | State with the highest quality data and info so far. Regular checks against [IL's pre-screener](http://fscalc.dhs.illinois.gov/FSCalc/returnToInput.do) and consultation with local subject matter experts. | Yes |
| MA    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | Not yet |
| MI    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | Yes, but more verification needed |
| MN    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | Yes, but more verification needed |
| VT    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | Yes, but more verification needed |
| UT    | State options data plugged into API; more verification and consultation with local subject matter experts needed. | N/A |

## `/calculate`

+ [Inputs (example valid request)](#inputs-example-valid-request)
+ [Inputs (summary)](#inputs-summary)
+ [Inputs (detail)](#inputs-detail)
+ [Outputs (example output)](#outputs-example-output)
+ [Outputs (summary)](#outputs-summary)
+ [Outputs (details)](#outputs-details)

### Example requests

Please reach out to eligibility-apis-initiative at gsa.gov to request the username/password for this prototype API.

[Valid input data; eligible household in IL.]()

### Inputs (summary):

* [household_size (int, required)](#household_size-int-required)
* [state_or_territory (str, required)](#state_or_territory-str-required)
* [household_includes_elderly_or_disabled (bool, required)](#household_includes_elderly_or_disabled-bool-required)
* [monthly_job_income (int, required)](#monthly_job_income-int-required)
* [monthly_non_job_income (int, required)](#monthly_non_job_income-int-required)
* [resources (int, required)](#resources-int-required)
* [dependent_care_costs (int, optional)](#dependent_care_costs-int-optional)
* [medical_expenses_for_elderly_or_disabled (int, optional)](#medical_expenses_for_elderly_or_disabled-int-optional)
* [court_ordered_child_support_payments (int, optional)](#court_ordered_child_support_payments-int-optional)
* [rent_or_mortgage (int, optional)](#rent_or_mortgage-int-optional)
* [homeowners_insurance_and_taxes (int, optional)](#homeowners_insurance_and_taxes-int-optional)
* [utility_costs (int, optional)](#utility_costs-int-optional)
* [utility_allowance (str, optional)](#utility_allowance-str-optional)
* [use_emergency_allotment (bool, optional)](#use_emergency_allotment-bool-optional)

### Inputs (detail):

#### `household_size (int, required)`
The number of people in the household.

#### `state_or_territory (str, required)`

The [U.S. Postal Abbreviation](https//pe.usps.com/text/pub28/28apb.htm) of the household's state or U.S. territory.

*DEV NOTE:* Handling of codes for territories is currently inconsistent and needs to be fixed.

#### `household_includes_elderly_or_disabled (bool, required)`

Does the household include any household members who are 60 years of age or over, or who meet the [SNAP criteria for disability](https//www.fns.usda.gov/snap/eligibility/elderly-disabled-special-rules#Who%20is%20elderly?)?

Boolean values can be sent in as strings in the following format: `"true", "false"`.

#### `monthly_job_income (int, required)`

Monthly earned income in dollars from sources such as a job or self-employment.

#### `monthly_non_job_income (int, required)`

Monthly income in dollars from sources non-job sources as Social Security, disability, Child Support, Worker's Comp, Unemployment, Pension Income, or other sources.

#### `resources (int, required)`

Total household assets in dollars.

*DEV NOTE:* Some states have no asset limit. For other states, asset amounts are an important component of eligibility determination. This field may move from required to required-on-a-per-state-basis in the near future.

#### `dependent_care_costs (int, optional)`

Monthly dependent care costs in dollars.

#### `medical_expenses_for_elderly_or_disabled (int, optional)`

Monthly cost of medical expenses for elderly or disabled household members in dollars.

Send `0` or do not send any value for this field if `household_includes_elderly_or_disabled == False`.

#### `court_ordered_child_support_payments (int, optional)`

Monthly cost of court-ordered child support payments in dollars.

#### `rent_or_mortgage (int, optional)`

Monthly rent or mortgage payment costs in dollars.

#### `homeowners_insurance_and_taxes (int, optional)`

Monthly costs of homeowners insurance and property taxes, in dollars.

#### `utility_costs (int, optional)`

The monthly utility costs of the household in dollars, if the household is in a state or territory that does not use mandatory Standard Utility Allowances.

Send `0` or do not send any value for this field if you send a value for `utility_allowance` (see below).

#### `utility_allowance (str, optional)`

The utility allowance claimed by the household, if the household is in a state or territory that uses mandatory Standard Utility Allowances.

If a utility allowance value is provided, it must be one of the following

* `'HEATING_AND_COOLING'`
* `'BASIC_LIMITED_ALLOWANCE'`
* `'SINGLE_UTILITY_ALLOWANCE'`
* `'ELECTRICITY'`
* `'GAS_AND_FUEL'`
* `'PHONE'`
* `'SEWAGE'`
* `'TRASH'`
* `'WATER'`
* `'NONE'`

Sending an explicit value of `'NONE'` is treated the same as sending no value for this field.

See ["Standard Utility Allowances"](https//www.fns.usda.gov/snap/eligibility/deduction/standard-utility-allowances) from USDA for more information.

#### `use_emergency_allotment (bool, optional)`

Is the household in a state or territory that is currently using SNAP Emergency Allotment amounts?

If no value is provided, the API will use its most recent available data on which states are using emergency allotments.

The API trusts the client about whether or not Emergency Allotments are in effect.

Boolean values can be sent in as strings in the following format: `"true", "false"`.

### Outputs (example output):

```
{
  'status': 'OK',
  'eligible': true,
  'estimated_monthly_benefit': 355,
  'state_website':'https://abe.illinois.gov/abe/access/',
  'use_emergency_allotment': true,
  'eligibility_factors': [
    {
      name: "Gross Income"
      result: 0
      sort_order: 0
      explanation: [
        "We find gross income by adding up monthly income from both job and non-job sources.",…
      ]
    }
    ...
    {
      name: "Net Income Test",
      result: true,
      sort_order: 3,
      explanation: [
        "To be eligible for SNAP, a household's net income needs to be below the net monthly income limit.",…
      ]
    }
    ...
  ]
}
```

### Outputs (summary):

* [status (str)](#status-str)
* [eligible (bool)](#eligible-bool)
* [estimated_monthly_benefit (int)](#estimated_monthly_benefit-int)
* [state_website (str)](#state_website-str)
* [use_emergency_allotment (bool)](#use_emergency_allotment-bool)
* [eligibility_factors (array)](#eligibility_factors-array)

### Outputs (details):

* #### `status (str)`

  * `"OK"`: Request handled successfully by API.
  * `"ERROR"`: API encountered one or more errors in handling the request.

* #### `eligible (bool)`

  * `true`: Household likely eligible for SNAP benefits.
  * `false`: Household likely ineligible for SNAP benefits.

* #### `estimated_monthly_benefit (int)`

Estimated monthly SNAP benefit for household, in dollars.

* #### `state_website (str)`

URL for the state or territorial website where a household can apply for SNAP benefits, or, if no such website exists, link to a page with more information about how to apply for SNAP benefits.

* #### `use_emergency_allotment (bool)`

Did the API use an emergency allotment amount in calculating its results?

* #### `eligibility_factors (array)`

Experimental feature. This is an array of objects that explain the different factors involved in the final eligibility estimate and estimated benefit amount. See below for the shape of each object in the array.

* #### `eligibility_factor (object)`

  * `name`: Name of the factor.
  * `sort_order`: Order in which to logically display the factor.
  * `result`: A boolean or integer result for this factor. (Boolean results for test such as "Gross Income Test" or "Net Income Test", integers for factors such as "Gross Income" or "Net Income".)
  * `explanation`: An array of sentences (strings) that explain the logic and math behind this factor. Each sentence in the array represents a line or paragraph.