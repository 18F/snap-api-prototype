from snap_financial_factors.allotments.fetch_max_allotments import FetchMaxAllotments
from snap_financial_factors.allotments.fetch_min_allotments import FetchMinAllotments


class BenefitAmountEstimate:
    def __init__(self,
                 state_or_territory,
                 household_size,
                 max_allotments,
                 min_allotments,
                 is_eligible,
                 net_income):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.max_allotments = max_allotments
        self.min_allotments = min_allotments
        self.is_eligible = is_eligible
        self.net_income = net_income

    def calculate(self):
        if not self.is_eligible:
            return {
                'amount': 0,
                'reason': {
                    'test_name': 'Estimated Benefit Calculation',
                    'description': ['Likely not eligible for SNAP.']
                }
            }

        max_allotment = FetchMaxAllotments(self.state_or_territory,
                                           self.household_size,
                                           self.max_allotments).calculate()

        min_allotment = FetchMinAllotments(self.state_or_territory,
                                           self.household_size,
                                           self.min_allotments).calculate()

        estimated_benefit = round(max_allotment - (self.net_income * 0.3))

        if min_allotment and (min_allotment > estimated_benefit):
            estimated_benefit = min_allotment

        description = []
        description.append('Max monthly allotment for state and household size: ${}.'.format(max_allotment))
        if min_allotment:
            description.append('Min monthly allotment for state and household size: ${}.'.format(min_allotment))
        description.append('Subtract 30 percent of net monthly income to determine estimated benefit.')
        description.append('Net monthly income: ${}.'.format(self.net_income))

        if 0 > estimated_benefit:
            description.append("Eligibile, but monthly income results in zero benefit.")
            estimated_benefit = 0

        description.append('Estimated monthly benefit: ${}.'.format(estimated_benefit))

        return {
            'amount': estimated_benefit,
            'reason': {
                'test_name': 'Estimated Benefit Calculation',
                'description': description,
                'sort_order': 4
            }
        }
