from snap_financial_factors.program_data_api.fetch_deductions import FetchDeductions
from snap_financial_factors.deductions.earned_income_deduction import EarnedIncomeDeduction
from snap_financial_factors.deductions.dependent_care_deduction import DependentCareDeduction
from snap_financial_factors.deductions.medical_expenses_deduction import MedicalExpensesDeduction
from snap_financial_factors.input_data.input_data import InputData


class NetIncome:
    '''
    Returns the adjusted net income (gross income minus deductions).
    '''

    def __init__(self, input_data: InputData, deductions_data):
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data.state_or_territory
        self.household_size = input_data.household_size
        self.monthly_job_income = input_data.monthly_job_income
        self.monthly_non_job_income = input_data.monthly_non_job_income
        self.dependent_care_costs = input_data.dependent_care_costs
        self.household_includes_elderly_or_disabled = input_data.household_includes_elderly_or_disabled
        self.medical_expenses_for_elderly_or_disabled = input_data.medical_expenses_for_elderly_or_disabled

        self.deductions_data = deductions_data

    def calculate(self):
        state_or_territory = self.state_or_territory
        household_size = self.household_size
        deductions_data = self.deductions_data
        monthly_job_income = self.monthly_job_income
        monthly_non_job_income = self.monthly_non_job_income

        explanation = []
        explanation_intro = (
            'To find out if this household is eligible for SNAP and estimate ' +
            'the benefit amount, we start by calculating net income. Net income ' +
            'is equal to total gross monthly income, minus deductions.'
        )
        explanation.append(explanation_intro)

        # Add up income.
        total_income = monthly_job_income + monthly_non_job_income
        income_explanation = (
            "Let's start with total household income. " +
            f"This household reports monthly earned income of ${monthly_job_income} " +
            f"and additional monthly income of ${monthly_non_job_income}, " +
            f"for a total income of <strong>${total_income}.</strong>"
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
            f"<a class='why why-small' href='{standard_deduction_pdf_url}' target='_blank'>why?</a>"
        )
        explanation.append(standard_deduction_explanation)

        # Earned income deduction
        earned_income_deduction_calculator = EarnedIncomeDeduction(self.monthly_job_income)
        earned_income_deduction_calculation = earned_income_deduction_calculator.calculate()
        earned_income_deduction = earned_income_deduction_calculation.result
        earned_income_deduction_explanations = earned_income_deduction_calculation.explanation
        for earned_income_deduction_explanation in earned_income_deduction_explanations:
            explanation.append(earned_income_deduction_explanation)

        # Dependent care deduction
        dependent_care_deduction_calculator = DependentCareDeduction(self.dependent_care_costs)
        dependent_care_deduction_calculation = dependent_care_deduction_calculator.calculate()
        dependent_care_deduction = dependent_care_deduction_calculation.result
        dependent_care_deduction_explanations = dependent_care_deduction_calculation.explanation
        for dependent_care_deduction_explanation in dependent_care_deduction_explanations:
            explanation.append(dependent_care_deduction_explanation)

        # Medical expenses deduction
        medical_expenses_deduction_calculator = MedicalExpensesDeduction(self.household_includes_elderly_or_disabled,
                                                                         self.medical_expenses_for_elderly_or_disabled)
        medical_expenses_deduction_calculation = medical_expenses_deduction_calculator.calculate()
        medical_expenses_deduction = medical_expenses_deduction_calculation.result
        medical_expenses_deduction_explanations = medical_expenses_deduction_calculation.explanation
        for medical_expenses_deduction_explanation in medical_expenses_deduction_explanations:
            explanation.append(medical_expenses_deduction_explanation)

        total_deductions = (standard_deduction +
                            earned_income_deduction +
                            dependent_care_deduction +
                            medical_expenses_deduction)

        total_deductions_explanation = (
            f"Next, we add all the deductions together: "
        )
        explanation.append(total_deductions_explanation)
        explanation.append('')

        total_deductions_math_explanation = (
            f"${standard_deduction} + " +
            f"${earned_income_deduction} + " +
            f"${dependent_care_deduction} + " +
            f"${medical_expenses_deduction} = " +
            f"${total_deductions}"
        )
        explanation.append(total_deductions_math_explanation)

        total_deductions_summary = (
            f"The total of all deductions is <strong>${total_deductions}</strong>. "
        )
        explanation.append(total_deductions_summary)

        net_income = total_income - total_deductions

        # Adjusted net income can't be negative
        if 0 > net_income:
            net_income = 0

        calculation_explanation = (
            f"Total income (<strong>${total_income}</strong>) minus " +
            f"total deductions (<strong>${total_deductions}</strong>) " +
            f"equals net income: <strong>${net_income}.</strong>"
        )
        explanation.append(calculation_explanation)

        return {
            'result': net_income,
            'reason': {
                'test_name': 'Net Income',
                'description': explanation,
                'sort_order': 0,
            }
        }
