from typing import Dict


class FetchMaxShelterDeductions:
    '''
    Internal API for fetching data about maximum shelter deductions.
    '''

    def __init__(self,
                 state_or_territory: str,
                 household_size: int,
                 max_shelter_deductions: Dict,
                 fiscal_year: int):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.max_shelter_deductions = max_shelter_deductions
        self.fiscal_year = fiscal_year

    def state_lookup_key(self) -> str:
        return {
            'AK': 'AK',
            'HI': 'HI',
            'GUAM': 'GUAM',
            'VIRGIN_ISLANDS': 'VIRGIN_ISLANDS'
        }.get(self.state_or_territory, 'DEFAULT')

    def maximum_shelter_deduction(self):
        state_lookup_key = self.state_lookup_key()
        max_shelter_deductions = self.max_shelter_deductions

        return max_shelter_deductions['maximum_shelter_deduction'][state_lookup_key][self.fiscal_year]
