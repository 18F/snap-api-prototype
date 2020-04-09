# API documentation

## Web API

The Web API has one endpoint:

### `/calculate`

Inputs:

#### `household_size (int, required)`

The number of people in the household.

#### `state_or_territory (str, required)`

The [U.S. Postal Abbreviation](https://pe.usps.com/text/pub28/28apb.htm) of the household's state or U.S. territory.

#### `household_includes_elderly_or_disabled (bool, required)`

Does the household include any household members who are 60 years of age or over, or who meet the [SNAP criteria for disability](https://www.fns.usda.gov/snap/eligibility/elderly-disabled-special-rules#Who%20is%20elderly?)?

#### `monthly_job_income (int, required)`

Monthly earned income in dollars from sources such as a job or self-employment.

#### `monthly_non_job_income (int, required)`

Monthly income in dollars from sources non-job sources as

#### `resources (int, required)`

Total household assets in dollars.

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

If a utility allowance value is provided, it must be one of the following:

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

See ["Standard Utility Allowances"](https://www.fns.usda.gov/snap/eligibility/deduction/standard-utility-allowances) from USDA for more information.

#### `use_emergency_allotment (bool, optional)`

Is the household in a state or territory that is currently using SNAP Emergency Allotment amounts?

If no value is provided, the API will use its most recent available data on which states are using emergency allotments.

The API trusts the client about whether or not Emergency Allotments are in effect.