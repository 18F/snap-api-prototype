class AssetTest:
    def __init__(self, input_data, resource_limit_elderly_or_disabled,resource_limit_non_elderly_or_disabled):
        # Load user input data
        self.input_data = input_data
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']

        self.resource_limit_elderly_or_disabled = resource_limit_elderly_or_disabled
        self.resource_limit_non_elderly_or_disabled = resource_limit_non_elderly_or_disabled

    def calculate(self):
        if (self.resource_limit_elderly_or_disabled is None) and (self.resource_limit_non_elderly_or_disabled is None):
            return {
                'result': True,
                'reason': {
                    'test_name': 'Asset Test',
                    'test_passed?': True,
                    'description': ['State does not have an asset test.']
                }
            }

        has_resource_limit = (self.household_includes_elderly_or_disabled or \
                              self.resource_limit_non_elderly_or_disabled)

        if has_resource_limit:
            if self.household_includes_elderly_or_disabled:
                resource_limit = self.resource_limit_elderly_or_disabled
                description = ['Since the household includes an elderly or disabled member, the resource limit is ${}'.format(resource_limit)]
            else:
                resource_limit = self.resource_limit_non_elderly_or_disabled
                description = ['Since the household does not include an elderly or disabled member, the resource limit is ${}.'.format(resource_limit)]

            below_resource_limit = (self.resources <= resource_limit)
            description.append('Eligibility factor -- Are household resources below the asset limit? {}'.format(below_resource_limit))
        else:
            description = 'This state does not have a resource limit.'
            below_resource_limit = True

        return {
            'result': below_resource_limit,
            'reason': {
                'test_name': 'Asset Test',
                'test_passed?': below_resource_limit,
                'description': description
            },
        }