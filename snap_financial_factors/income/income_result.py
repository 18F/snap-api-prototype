from typing import List


class IncomeResult:
    '''
    Expresses the result of an income calculation.
    '''

    def __init__(self,
                 name: str,
                 result: int,
                 explanation: List[str],
                 sort_order: int) -> None:
        self.name = name
        self.result = result
        self.explanation = explanation
        self.sort_order = sort_order
        self.name_and_explanation = {
            'name': name,
            'explanation': explanation,
        }
