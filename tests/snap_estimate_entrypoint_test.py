import pytest
from snap_financial_factors.benefit_estimate.snap_estimate_entrypoint import SnapEstimateEntrypoint


def send_data_to_entrypoint(input_data):
    return SnapEstimateEntrypoint(input_data).calculate()


# The SnapEstimateEntrypoint class mostly delegates logic to ParseInputData and
# BenefitEstimate classes; it runs validations, delegates out eligibility logic
# and adds a 'status' key based on the result.

# Testing a few cases here to check the predicted shape of the result;
# more detailed validation scenarios in parse_input_data_test.py.

def test_no_input_data():
    result = send_data_to_entrypoint(None)
    assert result['status'] == 'ERROR'
    assert result['errors'] == ['No input data received.']

#
def test_valid_input_data():
    result = send_data_to_entrypoint({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0
    })
    assert result['status'] == 'OK'
    assert result['eligible'] == True


def test_missing_required_integer():
    result = send_data_to_entrypoint({
        'state_or_territory': 'IL',
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0
    })
    assert result['status'] == 'ERROR'
    assert result['errors'] == ['Missing required input: monthly_job_income']
