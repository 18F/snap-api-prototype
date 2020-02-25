import json
from behave import given, when, then, step
from snap_financial_factors.benefit_estimate import BenefitEstimate


@given('the household is in {state}')
def step_impl(context, state):
    context.input_data = {}
    context.input_data['state_or_territory'] = state

@given('a {number:d}-person household')
def step_impl(context, number):
    context.input_data['household_size'] = number

@given('the household {does_or_does_not} include an elderly or disabled member')
def step_impl(context, does_or_does_not):
    result = (does_or_does_not == 'does')
    context.input_data['household_includes_elderly_or_disabled'] = result

@given('the household has earned income of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['monthly_earned_income'] = number

@given('the household has other income of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['monthly_other_income'] = number

@given('the household has assets of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['resources'] = number

@when('we run the benefit estimator...')
def step_impl(context):
    benefit_estimate = BenefitEstimate(context.input_data)
    context.api_result = benefit_estimate.calculate()

@then('we find the family is likely {eligible}')
def step_impl(context, eligible):
    expected_result = (eligible == 'eligible')
    api_result = context.api_result['eligible']

    if (api_result != expected_result):
        print('api_result:')
        print(api_result)
        print('expected_result:')
        print(expected_result)

    assert(api_result == expected_result)

@then('we find the estimated benefit is ${number:d} per month')
def step_impl(context, number):
    expected_result = number
    api_result = context.api_result['estimated_monthly_benefit']

    if (api_result != expected_result):
        print('api_result:')
        print(api_result)
        print('expected_result:')
        print(expected_result)

    assert(api_result == expected_result)
