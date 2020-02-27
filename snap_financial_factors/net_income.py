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
        self.dependent_care_costs = input_data['dependent_care_costs']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.medical_expenses_for_elderly_or_disabled = input_data['medical_expenses_for_elderly_or_disabled']

        self.deductions_data = deductions_data

    def calculate(self):
        state_or_territory = self.state_or_territory
        household_size = self.household_size
        deductions_data = self.deductions_data
        monthly_job_income = self.monthly_job_income
        monthly_non_job_income = self.monthly_non_job_income
        explanation = []

        # Add up income.
        total_income = monthly_job_income + monthly_non_job_income
        income_explanation = (
            "Let's start with total household income. " +
            f"This household reports monthly earned income of ${monthly_job_income} " +
            f"and additional monthly income of ${monthly_non_job_income}, " +
            f"for a total income of ${total_income}."
        )
        explanation.append(income_explanation)

        # Add up deductions:

        # Standard deduction
        deductions = FetchDeductions(state_or_territory, household_size, deductions_data)
        standard_deduction = deductions.standard_deduction()

        standard_deduction_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf'
        standard_deduction_explanation = (
            "\nNext, we need to take into account deductions. " +
            f"We start with a standard deduction of ${standard_deduction}. " +
            f"<a class='why-link' href='{standard_deduction_pdf_url}'>why?</a>"
        )
        explanation.append(standard_deduction_explanation)

        # Earned income deduction
        earned_income_deduction = 0.2 * monthly_job_income
        earned_income_deduction_explanation = (
            "Next, we add the earned income deduction. " +
            "This is equal to 20% of income from jobs or self-employment, " +
            f"and comes to ${earned_income_deduction}."
        )
        explanation.append(earned_income_deduction_explanation)

        # Dependent care deduction
        dependent_care_deduction = self.dependent_care_costs
        dependent_care_deduction_explanation = (
            f"Next, we add a deduction for dependent care costs: ${dependent_care_deduction}."
        )
        explanation.append(dependent_care_deduction_explanation)

        # Medical expenses deduction
        medical_expenses_deduction = 0  # Set default
        if self.household_includes_elderly_or_disabled:
            medical_deduction_explanation = "Next, deduct monthly medical expenses for elderly or disabled household members beyond $35. "
            if self.medical_expenses_for_elderly_or_disabled > 0:
                if self.medical_expenses_for_elderly_or_disabled > 35:
                    medical_expenses_deduction = self.medical_expenses_for_elderly_or_disabled - 35
                    medical_deduction_explanation += f"Medical expenses deduction: ${medical_expenses_deduction}. "
                else:
                    medical_deduction_explanation += "In this case, medical expenses are below the $35 monthly threshold for deduction. "
            else:
                medical_deduction_explanation += "In this case, there are no monthly medical expenses to deduct. "

            explanation.append(medical_deduction_explanation)

        total_deductions = (standard_deduction +
                            earned_income_deduction +
                            dependent_care_deduction +
                            medical_expenses_deduction)

        explanation.append(f"The total of all deductions is ${total_deductions}. ")

        net_income = total_income - total_deductions

        # Adjusted net income can't be negative
        if 0 > net_income:
            net_income = 0

        calculation_explanation = (
            f"Total income ${total_income} minus total deductions {total_deductions} ." +
            "equals net income: ${net_income}."
        )
        explanation.append(calculation_explanation)

        return {
            'result': net_income,
            'reason': {
                'test_name': 'Net Income',
                'description': description,
                'sort_order': 0,
            }
        }
