class GrossIncomeTest:
    def __init__(self, input_data, income_limits, gross_income_limit_factor):
        # Load user input data
        self.input_data = input_data
        self.monthly_earned_income = input_data['monthly_earned_income']
        self.monthly_other_income = input_data['monthly_other_income']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']

        self.income_limits = income_limits
        self.gross_income_limit_factor = gross_income_limit_factor

    def calculate(self):
        if self.household_includes_elderly_or_disabled:
            return {
                'result': True,
                'reason': {
                    'test_name': 'Gross Income Test',
                    'test_passed?': True,
                    'description': ['Households with an elderly or disabled member do not need to meet a gross income test.']
                }
            }

        total_income = self.monthly_earned_income + self.monthly_other_income

        gross_monthly_income_limit = self.gross_income_limit_factor * self.income_limits.net_monthly_income_limit()
        below_gross_income_limit = gross_monthly_income_limit > total_income

        description = []
        description.append('Gross monthly income limit for state and household size: ${}'.format(gross_monthly_income_limit))
        description.append('Total monthly income submitted to API: ${}'.format(total_income))
        description.append('Meets eligibility test? {}.'.format(below_gross_income_limit))

        return {
            'result': below_gross_income_limit,
            'reason': {
                'test_name': 'Gross Income Test',
                'test_passed?': below_gross_income_limit,
                'description': description
            }
        }
