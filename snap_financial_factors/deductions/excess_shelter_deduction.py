from typing import Dict
from snap_financial_factors.deductions.deduction_result import DeductionResult
from snap_financial_factors.program_data_api.fetch_deductions import FetchDeductions


class ExcessShelterDeduction:
    '''
    Calculates excess shelter deduction.
    '''

    def __init__(self,
                 adjusted_income: int,
                 shelter_costs: int,
                 household_includes_elderly_or_disabled: bool,
                 state_or_territory: str,
                 household_size: int,
                 deductions_data: Dict) -> None:
        self.adjusted_income = adjusted_income
        self.shelter_costs = shelter_costs
        self.household_includes_elderly_or_disabled = household_includes_elderly_or_disabled
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.deductions_data = deductions_data

    def calculate(self) -> DeductionResult:
        half_adjusted_income = round(self.adjusted_income / 2)

        # If shelter costs are less than half of adjusted income, no deduction applied.
        if half_adjusted_income > self.shelter_costs:
            return DeductionResult(
                result=0,
                explanation=[
                    'Shelter costs do not exceed half of adjusted income.'
                ]
            )

        raw_deduction_amount = self.shelter_costs - half_adjusted_income

        # If household includes elderly or disabled person, no limit on
        # the amount of the excess shelter deduction.
        if self.household_includes_elderly_or_disabled:
            deduction_amount = raw_deduction_amount

            return DeductionResult(
                result=deduction_amount,
                explanation=[
                    'Because household includes an elderly or disabled household ' +
                    'member, there is no limit to the excess shelter deduction ' +
                    'amount.'
                ]
            )

        # If household does not include an elderly or disabled person,
        # check to see if the deduction amount would be above the limit.
        deductions_api = FetchDeductions(
            state_or_territory=self.state_or_territory,
            household_size=self.household_size,
            deductions_data=self.deductions_data,
            fiscal_year=2020
        )

        maximum_shelter_deduction = deductions_api.maximum_shelter_deduction()

        if raw_deduction_amount > maximum_shelter_deduction:
            return DeductionResult(
                result=maximum_shelter_deduction,
                explanation=[
                    'Household has a maximum excess shelter deduction of $569.'
                ]
            )

        # Finally, handle case where household does not include an elderly or
        # disabled person and the deduction amount does not exceed the limit.
        deduction_amount = raw_deduction_amount

        return DeductionResult(
            result=deduction_amount,
            explanation=[
                ''
            ]
        )
