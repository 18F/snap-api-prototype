from typing import List


class TestResult:
    '''
    Expresses the result of a SNAP eligibility test.
    '''

    def __init__(self,
                 test_name: str,
                 result: bool,
                 explanation: List[str],
                 sort_order: int) -> None:

        self.test_name = test_name
        self.result = result
        self.explanation = explanation
        self.sort_order = sort_order
        self.name_and_explanation = {
            'name': test_name,
            'explanation': explanation,
        }
