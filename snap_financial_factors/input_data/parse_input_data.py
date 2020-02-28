from typing import Dict
from snap_financial_factors.input_data.input_data import InputData


class ParseInputData:
    '''
    Cleans up input data sent to API:
    * Converts strings to integers as needed
    * Sets defaults
    '''

    def __init__(self, input_data: Dict) -> None:
        self.input_data = input_data

    def parse(self) -> InputData:
        input_data = self.input_data

        # Convert strings to integers as needed:
        input_data['household_size'] = int(input_data['household_size'])
        input_data['monthly_job_income'] = int(input_data['monthly_job_income'])
        input_data['monthly_non_job_income'] = int(input_data['monthly_non_job_income'])
        input_data['resources'] = int(input_data['resources'])

        # Optional value. Set default; convert to int when value supplied:
        if 'dependent_care_costs' in input_data:
            if input_data['dependent_care_costs']:
                input_data['dependent_care_costs'] = int(input_data['dependent_care_costs'])
            else:
                input_data['dependent_care_costs'] = 0
        else:
            input_data['dependent_care_costs'] = 0

        # Optional value. Set default; convert to int when value supplied:
        if 'medical_expenses_for_elderly_or_disabled' in input_data:
            if input_data['medical_expenses_for_elderly_or_disabled']:
                input_data['medical_expenses_for_elderly_or_disabled'] = int(input_data['medical_expenses_for_elderly_or_disabled'])
            else:
                input_data['medical_expenses_for_elderly_or_disabled'] = 0
        else:
            input_data['medical_expenses_for_elderly_or_disabled'] = 0

        # Parse booleans sent in as strings:
        includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        if isinstance(includes_elderly_or_disabled, str):
            input_data['household_includes_elderly_or_disabled'] = (
                includes_elderly_or_disabled == 'true'
            )

        return InputData(input_data)
