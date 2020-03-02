from typing import Dict
from snap_financial_factors.input_data.input_data import InputData


class ParseInputData:
    '''
    Cleans up input data sent to API:
    * Converts strings to integers as needed
    * Sets defaults

    Any new input factors must be handled here and in the InputData class.
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

        # Parse optional integer input data:
        input_data['dependent_care_costs'] = self.parse_optional_integer_input('dependent_care_costs')
        input_data['medical_expenses_for_elderly_or_disabled'] = self.parse_optional_integer_input('medical_expenses_for_elderly_or_disabled')
        input_data['court_ordered_child_support_payments'] = self.parse_optional_integer_input('court_ordered_child_support_payments')

        # Parse booleans sent in as strings:
        includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        if isinstance(includes_elderly_or_disabled, str):
            input_data['household_includes_elderly_or_disabled'] = (
                includes_elderly_or_disabled == 'true'
            )

        return InputData(input_data)

    def parse_optional_integer_input(self, input_key: str) -> None:
        if input_key in self.input_data:         # Check if the key exists in the dict
            if self.input_data[input_key]:       # Parse as int if value is int or present string
                return int(self.input_data[input_key])
            else:                                # Set to zero if value is null or empty string
                return 0
        else:                                    # Set to zero if value does not exist in dict
            return 0
