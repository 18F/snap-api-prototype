from typing import Dict

from snap_financial_factors.deductions.deduction_result import DeductionResult
from snap_financial_factors.program_data_api.fetch_max_shelter_deductions import FetchMaxShelterDeductions


class ExcessShelterDeduction:
    '''
    Calculates excess shelter deduction.
    '''

    def __init__(self,
                 adjusted_income: int,
                 rent_or_mortgage: int,
                 homeowners_insurance_and_taxes: int,
                 household_includes_elderly_or_disabled: bool,
                 state_or_territory: str,
                 household_size: int,
                 max_shelter_deductions: Dict,
                 utility_costs: int,
                 utility_allowance: str,
                 mandatory_standard_utility_allowances: bool,
                 standard_utility_allowances: Dict) -> None:
        self.adjusted_income = adjusted_income
        self.rent_or_mortgage = rent_or_mortgage
        self.homeowners_insurance_and_taxes = homeowners_insurance_and_taxes
        self.household_includes_elderly_or_disabled = household_includes_elderly_or_disabled
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.max_shelter_deductions = max_shelter_deductions
        self.utility_costs = utility_costs
        self.utility_allowance = utility_allowance
        self.mandatory_standard_utility_allowances = mandatory_standard_utility_allowances
        self.standard_utility_allowances = standard_utility_allowances

    def calculate(self) -> DeductionResult:
        explanation = [
            'Next, we calculate the Excess Shelter Deduction. To calculate ' +
            'this deduction, we need to find half of the household adjusted income. ' +
            'Adjusted income is equal to gross income, minus all deductions calculated ' +
            'up to this point.'
        ]

        half_adjusted_income = round(self.adjusted_income / 2)

        half_adjusted_income_explanation = (
            f"For this household, adjusted income is ${self.adjusted_income} " +
            f"and half of adjusted income is ${half_adjusted_income}."
        )
        explanation.append(half_adjusted_income_explanation)

        shelter_costs_explanation = (
            'Next, add up shelter costs by adding any costs of rent, mortgage ' +
            'payments, homeowners insurance and property taxes, and utility costs. ' +
            "Let's start with everything except utilities:"
        )
        explanation.append(shelter_costs_explanation)

        base_shelter_costs = self.rent_or_mortgage + self.homeowners_insurance_and_taxes

        shelter_costs_math_explanation = (
            f"${self.rent_or_mortgage} rent or mortgage + " +
            f"${self.homeowners_insurance_and_taxes} homeowners insurance and taxes = " +
            f"${base_shelter_costs}"
        )
        explanation.append(shelter_costs_math_explanation)

        # Handle utilities:
        start_utilities_explanation = ("Now let's factor in utility costs.")
        explanation.append(start_utilities_explanation)

        if self.mandatory_standard_utility_allowances:
            if self.utility_allowance is None or self.utility_allowance == 'NONE':
                # In this case the client has either:
                # * Explicitly told us the end user does not qualify for a
                # standard utility allowance ("NONE"), or,
                # * The client has left the field blank (None); we assume that
                # the end user does not pay for utilities separately and
                # for that reason does not receive a SUA deduction.
                shelter_costs = base_shelter_costs
                utilities_explanation = (
                    'In this case there is no deduction for utilities, likely ' +
                    'because the household is not billed separately for utilities.'
                )
            else:
                utility_allowance_amount = self.standard_utility_allowances[self.utility_allowance]
                shelter_costs = base_shelter_costs + utility_allowance_amount
                utilities_explanation = ('')
        else:
            shelter_costs = base_shelter_costs + self.utility_costs
            utilities_explanation = ('')

        explanation.append(utilities_explanation)

        # If shelter costs are less than half of adjusted income, no deduction applied.
        if half_adjusted_income > shelter_costs:
            explanation.append(
                'In this case, shelter costs do not exceed half of adjusted income, ' +
                'so the excess shelter deduction does not apply.'
            )

            return DeductionResult(result=0, explanation=explanation)

        raw_deduction_amount = shelter_costs - half_adjusted_income

        excess_shelter_costs_math_intro = (
            'Subtract half of adjusted income from shelter costs to find ' +
            'the base deduction amount:'
        )
        explanation.append(excess_shelter_costs_math_intro)

        excess_shelter_costs_math_explanation = (
            f"${shelter_costs} shelter costs - " +
            f"${half_adjusted_income} half of adjusted income = " +
            f"${raw_deduction_amount} base deduction"
        )
        explanation.append(excess_shelter_costs_math_explanation)

        # If household includes elderly or disabled person, no limit on
        # the amount of the excess shelter deduction.
        if self.household_includes_elderly_or_disabled:
            deduction_amount = raw_deduction_amount
            explanation.append(
                'Because the household includes an elderly or disabled household ' +
                'member, there is no limit to the excess shelter deduction ' +
                f"amount, so the full deduction amount of ${deduction_amount} applies."
            )

            return DeductionResult(result=deduction_amount, explanation=explanation)

        # If household does not include an elderly or disabled person,
        # check to see if the deduction amount would be above the limit.
        deductions_api = FetchMaxShelterDeductions(
            state_or_territory=self.state_or_territory,
            household_size=self.household_size,
            max_shelter_deductions=self.max_shelter_deductions,
            fiscal_year=2020
        )

        maximum_shelter_deduction = deductions_api.maximum_shelter_deduction()

        if raw_deduction_amount > maximum_shelter_deduction:
            explanation.append(
                'In this case, the household has a maximum excess shelter ' +
                f"deduction of ${maximum_shelter_deduction}, so the maximum " +
                'deduction amount applies.'
            )

            return DeductionResult(
                result=maximum_shelter_deduction,
                explanation=explanation
            )

        # Finally, handle case where household does not include an elderly or
        # disabled person and the deduction amount does not exceed the limit.
        deduction_amount = raw_deduction_amount

        return DeductionResult(
            result=deduction_amount,
            explanation=explanation
        )
