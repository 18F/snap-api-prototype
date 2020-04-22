from typing import TypedDict
from typing import Dict
from typing import List

from snap_financial_factors.input_data.parse_input_data import ParseInputData
from snap_financial_factors.benefit_estimate.benefit_estimate import BenefitEstimate


class ApiResponseDict(TypedDict, total=False):
    status: str                             # Always returned by API
    errors: List[str]                       # Always returned if status is "ERROR"
    eligible: bool                          # Always returned if status is "OK"
    estimated_monthly_benefit: int          # Always returned if status is "OK"
    eligibility_factors: List[str]          # Ususally returned if status is "OK"; not guaranteed
    state_website: str                      # Ususally returned if status is "OK"; not guaranteed
    use_emergency_allotment: bool           # Ususally returned if status is "OK"; not guaranteed


class SnapEstimateEntrypoint:
    '''
    Entrypoint to the Python API.

    Passes to SnapBenefitEstimate if inputs are valid; otherwise, surfaces errors.

    Returns a dict with a 'status' key which will be either 'OK' or 'ERROR'.
    '''

    def __init__(self, input_data: Dict) -> None:
        self.input_data = input_data

    def calculate(self) -> ApiResponseDict:
        parsed_input_data = ParseInputData(self.input_data).parse()

        if parsed_input_data.valid is False:
            return {
                'status': 'ERROR',
                'errors': parsed_input_data.errors,
            }

        input_data = parsed_input_data.result
        result = BenefitEstimate(input_data).calculate()

        return {
            'status': 'OK',
            'eligible': result['eligible'],
            'estimated_monthly_benefit': result['estimated_monthly_benefit'],
            'eligibility_factors': result.get('eligibility_factors', None),
            'state_website': result.get('state_website', None),
            'use_emergency_allotment': result.get('use_emergency_allotment', None),
        }
