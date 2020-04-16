class ValidateStateOptions:
    '''
    Validates state options data and checks for any problems or inconsistencies.
    '''

    def __init__(self, state_options_data) -> None:
        self.state_options_data = state_options_data

    def validate_state_data(self, state_abbreviation, state_data):
        '''
        Returns nothing if no errors are found; otherwise raises an error.
        '''

        mandatory_standard_utility_allowances = state_data.get('mandatory_standard_utility_allowances', None)
        standard_utility_allowances = state_data.get('standard_utility_allowances', None)

        if (mandatory_standard_utility_allowances is False and standard_utility_allowances):
            raise ValueError(
                f"Error in {state_abbreviation} data: A state that does not use mandatory SUAs should not have SUA data."
            )

        if (mandatory_standard_utility_allowances is True and standard_utility_allowances is None):
            raise ValueError(
                f"Error in {state_abbreviation} data: A state that uses mandatory SUAs needs SUA data."
            )

        return

    def validate(self) -> None:
        for state_abbreviation in self.state_options_data:
            state_data = self.state_options_data[state_abbreviation][2020]
            self.validate_state_data(state_abbreviation, state_data)

        return
