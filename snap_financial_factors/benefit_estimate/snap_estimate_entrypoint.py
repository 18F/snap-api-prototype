from typing import Dict

from snap_financial_factors.input_data.parse_input_data import ParseInputData
from snap_financial_factors.benefit_estimate.benefit_estimate import BenefitEstimate


class SnapEstimateEntrypoint:
    '''
    Entrypoint to the Python API.

    Passes to SnapBenefitEstimate if inputs are valid; otherwise, surfaces errors.

    Returns a dict with a 'status' key which will be either 'OK' or 'ERROR'.
    '''

    def __init__(self, input_data: Dict) -> None:
        self.input_data = input_data

    def calculate(self):
        parsed_input_data = ParseInputData(self.input_data).parse()

        if parsed_input_data.valid is False:
            return {
                'errors': parsed_input_data.errors,
                'status': 'ERROR',
            }

        input_data = parsed_input_data.result
        benefit_estimate = BenefitEstimate(input_data).calculate()

        return {
            **benefit_estimate,
            'status': 'OK',
        }
