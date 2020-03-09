from snap_financial_factors.deductions.deduction_result import DeductionResult


class ExcessShelterDeduction:
    '''
    Calculates excess shelter deduction.
    '''

    def __init__(self,
                 adjusted_income: int,
                 shelter_costs: int,
                 household_includes_elderly_or_disabled: bool) -> None:
        self.adjusted_income = adjusted_income
        self.shelter_costs = shelter_costs
        self.household_includes_elderly_or_disabled = household_includes_elderly_or_disabled

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
        if raw_deduction_amount > 569:
            return DeductionResult(
                result=569,
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
