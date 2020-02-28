from snap_financial_factors.deductions.deduction_result import DeductionResult


class DependentCareDeduction:
    '''
    Calculates dependent care deduction given dependent care costs.
    '''

    def __init__(self, dependent_care_costs: int) -> None:
        self.dependent_care_costs = dependent_care_costs

    def calculate(self) -> DeductionResult:
        explanation = [
            f"Next, we deduct dependent care costs: ${self.dependent_care_costs}."
        ]

        return DeductionResult(
            result = self.dependent_care_costs,
            is_applicable = (self.dependent_care_costs > 0),
            explanation = explanation
        )
