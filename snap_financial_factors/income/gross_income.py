from snap_financial_factors.input_data.input_data import InputData
from snap_financial_factors.income.income_result import IncomeResult


class GrossIncome:
    '''
    Returns the adjusted net income (income minus exclusions).
    '''

    def __init__(self, input_data: InputData, child_support_payments_treatment: str) -> None:
        self.monthly_job_income = input_data.monthly_job_income
        self.monthly_non_job_income = input_data.monthly_non_job_income
        self.child_support_payments_treatment = child_support_payments_treatment
        self.court_ordered_child_support_payments = input_data.court_ordered_child_support_payments

    def child_support_payments_excluded(self) -> bool:
        if self.child_support_payments_treatment != 'EXCLUDE':
            return False

        if self.court_ordered_child_support_payments == 0:
            return False

        return True

    def calculate(self) -> IncomeResult:
        child_support_payments_excluded = self.child_support_payments_excluded()

        if child_support_payments_excluded:
            return self.calculate_with_child_support_payments_excluded()
        else:
            explanation = []

            gross_income_intro = (
                'We find gross income by adding up monthly income from both ' +
                'job and non-job sources.'
            )
            explanation.append(gross_income_intro)

            monthly_income = self.monthly_job_income + self.monthly_non_job_income

            gross_income_math = (
                f"${self.monthly_job_income} monthly job income + " +
                f"${self.monthly_non_job_income} monthly non-job income = " +
                f"<strong>${monthly_income} gross income</strong>"
            )
            explanation.append(gross_income_math)

            return IncomeResult(
                name='Gross Income',
                result=monthly_income,
                explanation=explanation,
                sort_order=0
            )

    def calculate_with_child_support_payments_excluded(self) -> IncomeResult:
        monthly_income = self.monthly_job_income + self.monthly_non_job_income

        explanation = []
        child_support_payments_explanation = (
            'In this state, court-ordered child support payments are ' +
            'counted as a gross income exclusion. The gross income is ' +
            'adjusted to exclude monthly court-ordered child support:'
        )
        explanation.append(child_support_payments_explanation)

        monthly_income_minus_child_support = (
            monthly_income - self.court_ordered_child_support_payments
        )

        child_support_payments_math = (
            f"${monthly_income} - " +
            f"${self.court_ordered_child_support_payments} = " +
            f"${monthly_income_minus_child_support} gross income"
        )
        explanation.append(child_support_payments_math)

        monthly_income = monthly_income_minus_child_support

        return IncomeResult(
            name='Gross Income',
            result=monthly_income,
            explanation=explanation,
            sort_order=0
        )
