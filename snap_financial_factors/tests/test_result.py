from typing import List


class TestResult:
    '''
    Expresses the result of a SNAP eligibility test.

    Duck types with IncomeResult and BenefitAmountResult across `name`,
    `explanation`, and `sort_order`.
    '''

    def __init__(self,
                 name: str,
                 result: bool,
                 explanation: List[str],
                 sort_order: int) -> None:

        self.name = name
        self.result = result
        self.explanation = explanation
        self.sort_order = sort_order
