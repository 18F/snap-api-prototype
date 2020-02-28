from typing import List

class DeductionResult:
    '''
    Expresses the result of a deduction calculation.
    '''

    def __init__(self, result: int, is_applicable: bool, explanation: List[str]) -> None:
        self.result = result
        self.is_applicable = is_applicable
        self.explanation = explanation
