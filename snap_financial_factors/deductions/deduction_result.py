from typing import List


class DeductionResult:
    '''
    Expresses the result of a deduction calculation.
    '''

    def __init__(self, result: int, explanation: List[str]) -> None:
        self.result = result
        self.explanation = explanation
