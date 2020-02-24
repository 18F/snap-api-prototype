import json
from behave import given, when, then, step
from snap_financial_factors.benefit_estimate import BenefitEstimate


@given('the household is in Illinois')
def step_impl(context):
    context.input_data = {}
    context.input_data['state_or_territory'] = 'IL'

@given('a {number:d}-person household')
def step_impl(context, number):
    context.input_data['household_size'] = number

@given('the household does not include an elderly or disabled member')
def step_impl(context):
    context.input_data['household_includes_elderly_or_disabled'] = False

@given('the household has income of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['monthly_income'] = number

@given('the household has assets of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['resources'] = number

@when('we run the benefit estimator')
def step_impl(context):
    benefit_estimate = BenefitEstimate(context.input_data)
    context.result = benefit_estimate.calculate()

@then('we find the family is likely eligible')
def step_impl(context):
    result = context.result
    assert(result['eligible'] == True)

@then('we find the estimated benefit is ${number:d} per month')
def step_impl(context, number):
    result = context.result
    assert(result['estimated_monthly_benefit'] == number)
