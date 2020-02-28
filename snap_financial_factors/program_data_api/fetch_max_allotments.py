class FetchMaxAllotments:
    '''
    Uses a state or territory and a household size to fetch the max allotment,
    using arithmetic to add an additional amount to the allotment for each
    household member beyond eight.
    '''

    def __init__(self, state_or_territory, household_size, max_allotments):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.max_allotments = max_allotments

    def state_lookup_key(self):
        return {
            'AK_URBAN': 'AK_URBAN',      # TODO (ARS): Figure this out.
            'AK_RURAL_1': 'AK_RURAL_1',  # TODO (ARS): Figure this out.
            'AK_RURAL_2': 'AK_RURAL_2',  # TODO (ARS): Figure this out.
            'HI': 'HI',
            'GUAM': 'GUAM',
            'VIRGIN_ISLANDS': 'VIRGIN_ISLANDS'
        }.get(self.state_or_territory, 'DEFAULT')

    def calculate(self):
        scale = self.max_allotments[self.state_lookup_key()][2020]

        if (0 < self.household_size < 9):
            return scale[self.household_size]
        elif (9 <= self.household_size):
            return scale[8] + ((self.household_size - 8) * (scale['each_additional']))
        elif (self.household_size <= 0):
            raise ValueError('Household size out of bounds (at or below zero).')
