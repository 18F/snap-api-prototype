class AssetTest:
    def __init__(self, input_data, resource_limit_elderly_or_disabled,resource_limit_non_elderly_or_disabled):
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data['state_or_territory']
        self.monthly_income = input_data['monthly_income']
        self.household_size = input_data['household_size']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']

        self.resource_limit_elderly_or_disabled = resource_limit_elderly_or_disabled
        self.resource_limit_non_elderly_or_disabled = resource_limit_non_elderly_or_disabled

    def calculate(self):
        # TODO (ARS): Handle resource_limit_elderly_or_disabled_income_twice_fpl.
        print('\033[1mResources: \033[0m')
        if self.household_includes_elderly_or_disabled:
            resource_limit = self.resource_limit_elderly_or_disabled
            print('Since the household includes an elderly or disabled member, the resource limit is ${}'.format(resource_limit))
        else:
            resource_limit = self.resource_limit_non_elderly_or_disabled
            print('Since the household does not include an elderly or disabled member, the resource limit is ${}.'.format(resource_limit))

        if resource_limit:
            below_resource_limit = (self.resources <= resource_limit)
            print('Eligibility factor -- Are household resources below the asset limit? {}'.format(below_resource_limit))
            print('')
        else:
            print('No asset test / resource limit because of state BBCE.')
            below_resource_limit = True # Hack for now

        return below_resource_limit