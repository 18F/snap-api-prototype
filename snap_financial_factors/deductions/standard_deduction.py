from typing import Dict
from snap_financial_factors.deductions.deduction_result import DeductionResult
from snap_financial_factors.program_data_api.fetch_standard_deductions import FetchStandardDeductions


class StandardDeduction:
    '''
    Calculates standard deduction amount.
    '''
    def __init__(self,
                 state_or_territory: str,
                 household_size: int,
                 standard_deductions: Dict) -> None:
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.standard_deductions = standard_deductions

    def calculate(self) -> DeductionResult:
        deductions_api = FetchStandardDeductions(
            state_or_territory=self.state_or_territory,
            household_size=self.household_size,
            standard_deductions=self.standard_deductions,
            fiscal_year=2020
        )

        standard_deduction = deductions_api.standard_deduction()

        standard_deduction_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf'
        explanation = [
            "\nNext, we need to take into account deductions. " +
            f"We start with a standard deduction of ${standard_deduction}. " +
            f"<a class='why why-small' href='{standard_deduction_pdf_url}' target='_blank'>why?</a>"
        ]

        return DeductionResult(
            result=standard_deduction,
            explanation=explanation
        )
