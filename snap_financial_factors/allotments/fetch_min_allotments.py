class FetchMinAllotments:
    '''
    Uses a state or territory and a household size to fetch the min allotment,
    returning None if the household is not eligible for a minimum allotment.

    In 2020, only one- and two- person households are eligible for a minimum
    allotment amount.
    '''

    def __init__(self, state_or_territory, household_size, min_allotments):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.min_allotments = min_allotments

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
        scale = self.min_allotments[self.state_lookup_key()][2020]

        # Minimum SNAP allotments are only defined for one- or two- person
        # households. A return value of None means no minimum, so the household
        # might receive zero SNAP benefit despite being eligible.
        if (0 < self.household_size < 3):
            return scale[self.household_size]
        else:
            return None
