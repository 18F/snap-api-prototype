class FetchIncomeLimits:

    def __init__(self, state_or_territory, household_size, income_limit_data):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.income_limit_data = income_limit_data

    def state_lookup_key(self):
        return {
            'AK': 'AK',
            'HI': 'HI'
        }.get(self.state_or_territory, 'DEFAULT')

    def income_limit_lookup(self, income_type):
        scale = self.income_limit_data[income_type][self.state_lookup_key()][2020]

        if (0 < self.household_size < 9):
            return scale[self.household_size]
        elif (9 <= self.household_size):
            return scale[8] + ((self.household_size - 8) * (scale['each_additional']))
        elif (self.household_size <= 0):
            raise ValueError('Household size out of bounds (at or below zero).')

    def gross_monthly_income_limit(self):
        return self.income_limit_lookup('gross_monthly_income_limits')

    def net_monthly_income_limit(self):
        return self.income_limit_lookup('net_monthly_income_limits')
