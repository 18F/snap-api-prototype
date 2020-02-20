class GrossIncomeTest:
    def __init__(self, input_data, income_limits, gross_income_limit_factor):
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data['state_or_territory']
        self.monthly_income = input_data['monthly_income']
        self.household_size = input_data['household_size']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']

        self.income_limits = income_limits
        self.gross_income_limit_factor = gross_income_limit_factor

    def calculate(self):
        # TODO (ARS): Confirm we can remove the gross monthly income table
        # and replace it with 1.3 (or the state multiplier) of the net
        # income table.
        gross_monthly_income_limit = self.gross_income_limit_factor * self.income_limits.net_monthly_income_limit()
        below_gross_income_limit = (gross_monthly_income_limit > self.monthly_income)

        print('\033[1mGross monthly income limit: \033[0m')
        print('Gross monthly income limit for state and household size: ${}'.format(gross_monthly_income_limit))
        print('Monthly income submitted to API: ${}'.format(self.monthly_income))
        print('Eligibility factor -- Is household monthly income below gross monthly income limit? {}.'.format(below_gross_income_limit))
        print('')

        return below_gross_income_limit