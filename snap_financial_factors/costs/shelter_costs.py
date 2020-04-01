from typing import Dict


class ShelterCosts:
    '''
    Calculates total shelter costs given individual shelter costs.
    '''

    def __init__(self,
                 rent_or_mortgage: int,
                 homeowners_insurance_and_taxes: int,
                 utility_costs: int,
                 utility_allowance: str,
                 mandatory_standard_utility_allowances: bool,
                 standard_utility_allowances: Dict) -> None:
        self.rent_or_mortgage = rent_or_mortgage
        self.homeowners_insurance_and_taxes = homeowners_insurance_and_taxes
        self.utility_costs = utility_costs
        self.utility_allowance = utility_allowance
        self.mandatory_standard_utility_allowances = mandatory_standard_utility_allowances
        self.standard_utility_allowances = standard_utility_allowances

    def calculate(self) -> int:
        shelter_costs_explanation = (
            'Next, add up shelter costs by adding any costs of rent, mortgage ' +
            'payments, homeowners insurance and property taxes, and utility costs. ' +
            "Let's start with everything except utilities:"
        )
        explanation = [shelter_costs_explanation]

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
                #
                # * Explicitly told us the end user does not qualify for a
                # standard utility allowance ("NONE"), or,
                #
                # * The client has left the field blank (None); we assume that
                # the end user does not pay for utilities separately and
                # for that reason does not receive a SUA deduction:
                #
                shelter_costs = base_shelter_costs
                utilities_explanation = (
                    'In this case there is no deduction for utilities, likely ' +
                    'because the household is not billed separately for utilities.'
                )
            else:
                utility_allowance_amount = self.standard_utility_allowances[self.utility_allowance]
                shelter_costs = base_shelter_costs + utility_allowance_amount
                utilities_explanation = (
                    f"In this case, a standard utility deduction of ${utility_allowance_amount} applies, " +
                    f"so total shelter plus utilities costs come to ${shelter_costs}."
                )
        else:
            shelter_costs = base_shelter_costs + self.utility_costs
            utilities_explanation = (
                f"In this case, the household has utility costs of ${self.utility_costs}, " +
                f"so total shelter plus utilities costs come to ${shelter_costs}."
            )

        explanation.append(utilities_explanation)

        return shelter_costs
