from snap_financial_factors.fetch_deductions import FetchDeductions

class NetIncomeTest:
    # TODO (ARS): Deductions beyond the standard deduction.

    def __init__(self, input_data, deductions_data, monthly_income, income_limits):
        # Load user input data
        self.input_data = input_data
        self.monthly_income = monthly_income
        self.monthly_earned_income = input_data['monthly_earned_income']
        self.monthly_other_income = input_data['monthly_other_income']
        self.state_or_territory = input_data['state_or_territory']
        self.household_size = input_data['household_size']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']

        self.deductions_data = deductions_data
        self.income_limits = income_limits

    def calculate(self):
        deductions = FetchDeductions(self.state_or_territory, self.household_size, self.deductions_data)
        standard_deduction = deductions.standard_deduction()
        net_monthly_income_limit = self.income_limits.net_monthly_income_limit()
        below_net_income_limit = (net_monthly_income_limit) > (self.monthly_income - standard_deduction)

        description = ['Net monthly income limit for state and household size: ${}'.format(net_monthly_income_limit)]
        description.append('Standard deduction for state and household size: ${}'.format(standard_deduction))
        description.append('Monthly income submitted to API: ${}'.format(self.monthly_income))
        description.append('Eligibility factor -- Is household income (minus deductions) below net monthly income limit? {}.'.format(below_net_income_limit))

        return {
            'result': below_net_income_limit,
            'reason': {
                'test_name': 'Net Income Test',
                'test_passed?': below_net_income_limit,
                'description': description
            }
        }
