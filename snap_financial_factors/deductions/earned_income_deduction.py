from snap_financial_factors.deductions.deduction_result import DeductionResult


class EarnedIncomeDeduction:
    '''
    Calculates earned income deduction amount given a monthly income.
    '''

    def __init__(self, monthly_job_income: int) -> None:
        self.monthly_job_income = monthly_job_income

    def calculate(self) -> DeductionResult:
        earned_income_deduction = round(0.2 * self.monthly_job_income)
        explanation = [
            (
                "Next, we add the earned income deduction. " +
                f"This is equal to 20% of income from jobs or self-employment: "
            ),
            (''),
            (
                f"${self.monthly_job_income} x 0.2 = " +
                f"${earned_income_deduction} earned income deduction"
            )
        ]

        return DeductionResult(
            result=earned_income_deduction,
            explanation=explanation
        )
