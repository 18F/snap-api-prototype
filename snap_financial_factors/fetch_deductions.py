class FetchDeductions:

    def __init__(self, state_or_territory, household_size, deductions_data):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.deductions_data = deductions_data

    def state_lookup_key(self):
        return {
            'AK': 'AK',
            'HI': 'HI',
            'GUAM': 'GUAM',
            'VIRGIN_ISLANDS': 'VIRGIN_ISLANDS'
        }.get(self.state_or_territory, 'DEFAULT')

    def standard_deduction(self):
        scale = self.deductions_data['standard_deduction'][self.state_lookup_key()][2020]

        if (0 < self.household_size < 7):
            return scale[self.household_size]
        elif (7 <= self.household_size):
            # The FNS documents refer to Household Size "6+"; the standard
            # deduction does not increase beyond household size of 6. Source:
            # https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf
            return scale[6]
