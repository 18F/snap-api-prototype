from typing import List


class BenefitAmountResult:
    '''
    Expresses the result of a SNAP benefit amount estimate test.

    Duck types with IncomeResult and TestResult across `name`,
    `explanation`, and `sort_order`.
    '''

    def __init__(self,
                 name: str,
                 amount: int,
                 explanation: List[str],
                 sort_order: int) -> None:
        self.name = name
        self.amount = amount
        self.explanation = explanation
        self.sort_order = sort_order
