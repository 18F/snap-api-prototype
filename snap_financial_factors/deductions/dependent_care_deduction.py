from typing import Dict


class DependentCareDeduction:
    '''
    Calculates dependent care deduction given dependent care costs.
    '''

    def __init__(self, dependent_care_costs: int) -> None:
        self.dependent_care_costs = dependent_care_costs

    def calculate(self) -> Dict:
        explanation = [
            f"Next, we deduct dependent care costs: ${self.dependent_care_costs}."
        ]

        return {
            'result': self.dependent_care_costs,
            'explanation': explanation,
            'applies?': (self.dependent_care_costs > 0)
        }
