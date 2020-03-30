from typing import Dict, List
from snap_financial_factors.input_data.input_data import InputData


class ParseInputData:
    '''
    Detects if input data is valid, returns error messages if not.

    Also, cleans up input data sent to API:

    * Converts strings to integers as needed
    * Sets defaults

    Any new input factors must be handled here and in the InputData class.
    '''

    def __init__(self, input_data: Dict) -> None:
        self.input_data: Dict = input_data
        self.valid: bool = True        # Default; set to False if invalid data detected.
        self.errors: List[str] = []    # Initialize array to fill with error messages.
        self.result = None

    # This method returns a self; apparently this case isn't well-handled until
    # Python 4.x.
    def parse(self):
        input_data = self.input_data

        # Handle case when no input data is received:
        if input_data is None:
            self.valid = False
            self.errors.append('No input data received.')
            return self

        # Handle required integer fields:
        required_integer_inputs = [
            'household_size',
            'monthly_job_income',
            'monthly_non_job_income',
            'resources',
        ]
        for input_key in required_integer_inputs:
            self.handle_required_integer_input(input_data=input_data, input_key=input_key)

        # Handle required boolean field (can be sent in as either a Python
        # boolean value or a string, "true" will convert to True):
        required_boolean_input = 'household_includes_elderly_or_disabled'
        self.handle_required_bool_input(input_data=input_data, input_key=required_boolean_input)

        # Handle optional integer fields:
        optional_integer_inputs = [
            'dependent_care_costs',
            'medical_expenses_for_elderly_or_disabled',
            'court_ordered_child_support_payments',
            'rent_or_mortgage',
            'homeowners_insurance_and_taxes',
            'utility_costs',
        ]
        for input_key in optional_integer_inputs:
            self.set_optional_integer_input(input_data=input_data, input_key=input_key)

        # Handle utility allowance input, string that must match tuple of
        # allowances the API knows about
        self.handle_utility_allowance_input(input_data=input_data)

        if self.valid:
            self.result = InputData(input_data)

        return self

    def handle_required_integer_input(self, input_data: Dict, input_key: str) -> None:
        input_value = input_data.get(input_key, None)

        if input_value is None:
            self.valid = False
            self.errors.append(f"Missing required input: {input_key}")
            return None

        try:
            input_data[input_key] = int(input_value)
        except ValueError:
            self.valid = False
            self.errors.append(f"Value for {input_key} is not an integer.")
            return None

    def handle_required_bool_input(self, input_data: Dict, input_key: str) -> None:
        input_value = input_data.get(input_key, None)

        if input_value is None:
            self.valid = False
            self.errors.append(f"Missing required input: {input_key}")
            return None

        # Convert to a Python boolean if a "string-y" boolean is passed in:
        if isinstance(input_value, str):
            input_data[input_key] = (input_value == 'true')

    def handle_utility_allowance_input(self, input_data: Dict) -> None:
        input_value = input_data.get('utility_allowance', None)

        # Utility allowance can be blank if the input is coming from a state
        # that uses raw utility costs instead of standard utility allowances
        if input_value is None:
            input_data['utility_allowance'] = None
            return None

        UTILITY_ALLOWANCES = (
            'HEATING_AND_COOLING',
            'BASIC_LIMITED_ALLOWANCE',
            'SINGLE_UTILITY_ALLOWANCE',
            'ELECTRICITY',
            'GAS_AND_FUEL',
            'PHONE',
            'SEWAGE',
            'TRASH',
            'WATER',
        )

        if input_value in UTILITY_ALLOWANCES:
            input_data['utility_allowance'] = input_value
        else:
            self.valid = False
            self.errors.append(f"Unknown standard utility allowance: {input_value}")
            return None

    def set_optional_integer_input(self, input_data: Dict, input_key: str) -> None:
        input_data[input_key] = self.parse_optional_integer_input(input_key)

    def parse_optional_integer_input(self, input_key: str) -> int:
        if input_key in self.input_data:         # Check if the key exists in the dict
            if self.input_data[input_key]:       # Parse as int if value is int or present string
                return int(self.input_data[input_key])
            else:                                # Set to zero if value is null or empty string
                return 0
        else:                                    # Set to zero if value does not exist in dict
            return 0
