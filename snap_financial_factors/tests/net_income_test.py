from snap_financial_factors.fetch_deductions import FetchDeductions

class NetIncomeTest:
    '''
    Evaluates net income against the appropriate net income threshold.
    '''

    def __init__(self, input_data, net_income, income_limits):
        self.input_data = input_data
        self.state_or_territory = input_data['state_or_territory']
        self.monthly_income = input_data['monthly_income']
        self.household_size = input_data['household_size']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']
        self.net_income = net_income
        self.income_limits = income_limits

    def calculate(self):
        net_monthly_income_limit = self.income_limits.net_monthly_income_limit()
        below_net_income_limit = net_monthly_income_limit > self.net_income

        description = ['Net monthly income limit for state and household size: ${}'.format(net_monthly_income_limit)]
        description.append('Net monthly income : ${}'.format(self.net_income))
        description.append('Eligibility factor -- Is household income (minus deductions) below net monthly income limit? {}.'.format(below_net_income_limit))

        return {
            'result': below_net_income_limit,
            'reason': {
                'test_name': 'Net Income Test',
                'test_passed?': below_net_income_limit,
                'description': description
            }
        }
