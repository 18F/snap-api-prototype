from snap_financial_factors.fetch_deductions import FetchDeductions


class NetIncome:
    '''
    Returns the adjusted net income (gross income minus deductions).
    '''

    def __init__(self, input_data, deductions_data):
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data['state_or_territory']
        self.household_size = input_data['household_size']
        self.monthly_job_income = input_data['monthly_job_income']
        self.monthly_non_job_income = input_data['monthly_non_job_income']

        self.deductions_data = deductions_data

    def calculate(self):
        state_or_territory = self.state_or_territory
        household_size = self.household_size
        deductions_data = self.deductions_data
        monthly_job_income = self.monthly_job_income
        monthly_non_job_income = self.monthly_non_job_income
        description = []

        # Add up income
        total_income = monthly_job_income + monthly_non_job_income

        # Add up deductions
        deductions = FetchDeductions(state_or_territory, household_size, deductions_data)
        standard_deduction = deductions.standard_deduction()
        description.append('Standard deduction: ${}.'.format(standard_deduction))

        earned_income_deduction = 0.2 * monthly_job_income
        description.append('Earned income deduction: ${}.'.format(earned_income_deduction))

        total_deductions = standard_deduction + earned_income_deduction
        description.append('Total deductions: ${}.'.format(total_deductions))

        net_income = total_income - total_deductions
        description.append('Total income: ${}.'.format(total_income))

        # Adjusted net income can't be negative
        if 0 > net_income:
            net_income = 0

        description.append('Net income (total income minus deductions): ${}.'.format(net_income))

        return {
            'result': net_income,
            'reason': {
                'test_name': 'Net Income',
                'description': description,
                'sort_order': 0,
            }
        }
