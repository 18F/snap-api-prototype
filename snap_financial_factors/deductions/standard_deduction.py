from typing import Dict
from snap_financial_factors.deductions.deduction_result import DeductionResult
from snap_financial_factors.program_data_api.fetch_deductions import FetchDeductions


class StandardDeduction:
    '''
    Calculates standard deduction amount.
    '''
    def __init__(self,
                 state_or_territory: str,
                 household_size: int,
                 deductions_data: Dict) -> None:
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.deductions_data = deductions_data

    def calculate(self) -> DeductionResult:
        deductions = FetchDeductions(self.state_or_territory,
                                     self.household_size,
                                     self.deductions_data)
        standard_deduction = deductions.standard_deduction()

        standard_deduction_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf'
        explanation = [
            "\nNext, we need to take into account deductions. " +
            f"We start with a standard deduction of ${standard_deduction}. " +
            f"<a class='why why-small' href='{standard_deduction_pdf_url}' target='_blank'>why?</a>"
        ]

        return DeductionResult(
            result=standard_deduction,
            is_applicable=True,
            explanation=explanation
        )