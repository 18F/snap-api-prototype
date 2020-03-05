from typing import List


class IncomeResult:
    '''
    Expresses the result of an income calculation.
    '''

    def __init__(self, result: int, explanation: List[str], sort_order: int) -> None:
        self.result = result
        self.explanation = explanation
        self.sort_order = sort_order
