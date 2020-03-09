from typing import Dict


class FetchDeductions:
    '''
    Internal API for fetching FNS data about deduction amounts.

    Returns deduction amounts for a given state or territory, household size,
    and fiscal year.
    '''

    def __init__(self,
                 state_or_territory: str,
                 household_size: int,
                 deductions_data: Dict,
                 fiscal_year: int):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.deductions_data = deductions_data
        self.fiscal_year = fiscal_year

    def state_lookup_key(self) -> str:
        return {
            'AK': 'AK',
            'HI': 'HI',
            'GUAM': 'GUAM',
            'VIRGIN_ISLANDS': 'VIRGIN_ISLANDS'
        }.get(self.state_or_territory, 'DEFAULT')

    def standard_deduction(self) -> int:
        state_lookup_key = self.state_lookup_key()
        deductions_data = self.deductions_data

        scale = deductions_data['standard_deduction'][state_lookup_key][self.fiscal_year]

        if (0 < self.household_size < 7):
            return scale[self.household_size]
        elif (7 <= self.household_size):
            # The FNS documents refer to Household Size "6+"; the standard
            # deduction does not increase beyond household size of 6. Source:
            # https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf
            return scale[6]
        else:
            raise ValueError('Unknown value for household size.')

    def maximum_shelter_deduction(self):
        state_lookup_key = self.state_lookup_key()
        deductions_data = self.deductions_data

        return deductions_data['maximum_shelter_deduction'][state_lookup_key][self.fiscal_year]
