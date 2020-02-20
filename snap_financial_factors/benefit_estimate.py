import yaml
from snap_financial_factors.fetch_income_limits import FetchIncomeLimits
from snap_financial_factors.fetch_deductions import FetchDeductions
from snap_financial_factors.fetch_allotments import FetchAllotments

class BenefitEstimate:
    def __init__(self, input_data):
        # Load user input data
        self.state_or_territory = input_data['state_or_territory']
        self.monthly_income = input_data['monthly_income']
        self.household_size = input_data['household_size']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']

        # Load SNAP program data as YAML
        self.bbce_data = yaml.safe_load(open('./program_data/bbce.yaml', 'r'))
        self.income_limit_data = yaml.safe_load(open('./program_data/income_limits.yaml', 'r'))
        self.deductions_data = yaml.safe_load(open('./program_data/deductions.yaml', 'r'))
        self.allotments_data = yaml.safe_load(open('./program_data/allotments.yaml', 'r'))

    def calculate(self):
        eligible = self.eligible() # bool
        estimated_monthly_benefit = self.estimated_monthly_benefit(eligible) # dollar amount int

        return {
            'eligible': eligible,
            'estimated_monthly_benefit': estimated_monthly_benefit
            }

    def eligible(self):
        print('')
        print('\033[1m💻 Estimating SNAP eligibility and benefit, please hold... \033[0m')

        state_bbce_data = self.bbce_data[self.state_or_territory][2020]
        state_uses_bbce = state_bbce_data['uses_bbce']

        print('State: {}'.format(self.state_or_territory))
        print('Uses BBCE in 2020?: {}'.format(state_uses_bbce))

        if state_uses_bbce:
            return self.calculate_eligibility(
                state_bbce_data['gross_income_limit_factor'],
                state_bbce_data['resource_limit_elderly_or_disabled'],
                state_bbce_data['resource_limit_elderly_or_disabled_income_twice_fpl'],
                state_bbce_data['resource_limit_non_elderly_or_disabled'],
            )
        else:
            # SNAP federal policy defaults
            return self.calculate_eligibility(
                gross_income_limit_factor=1.3,
                resource_limit_elderly_or_disabled=3500,
                resource_limit_elderly_or_disabled_income_twice_fpl=3500,
                resource_limit_non_elderly_or_disabled=2250,
            )

    def calculate_eligibility(self,
            gross_income_limit_factor,
            resource_limit_elderly_or_disabled,
            resource_limit_elderly_or_disabled_income_twice_fpl,
            resource_limit_non_elderly_or_disabled):
        income_limits = FetchIncomeLimits(self.state_or_territory, self.household_size, self.income_limit_data)

        # TODO (ARS): Confirm we can remove the gross monthly income table
        # and replace it with 1.3 (or the state multiplier) of the net
        # income table.
        gross_monthly_income_limit = gross_income_limit_factor * income_limits.net_monthly_income_limit()
        below_gross_income_limit = (gross_monthly_income_limit > self.monthly_income)

        print('\033[1mGross monthly income limit: \033[0m')
        print('Gross monthly income limit for state and household size: ${}'.format(gross_monthly_income_limit))
        print('Monthly income submitted to API: ${}'.format(self.monthly_income))
        print('Eligibility factor -- Is household monthly income below gross monthly income limit? {}.'.format(below_gross_income_limit))
        print('')

        # TODO (ARS): Deductions beyond the standard deduction.

        deductions = FetchDeductions(self.state_or_territory, self.household_size, self.deductions_data)
        standard_deduction = deductions.standard_deduction()
        net_monthly_income_limit = income_limits.net_monthly_income_limit()
        below_net_income_limit = (net_monthly_income_limit) > (self.monthly_income - standard_deduction)

        print('\033[1mNet monthly income limit: \033[0m')
        print('Net monthly income limit for state and household size: ${}'.format(net_monthly_income_limit))
        print('Standard deduction for state and household size: ${}'.format(standard_deduction))
        print('Monthly income submitted to API: ${}'.format(self.monthly_income))
        print('Eligibility factor -- Is household income (minus deductions) below net monthly income limit? {}.'.format(below_net_income_limit))
        print('')

        # TODO (ARS): Handle resource_limit_elderly_or_disabled_income_twice_fpl.
        print('\033[1mResources: \033[0m')
        if self.household_includes_elderly_or_disabled:
            resource_limit = resource_limit_elderly_or_disabled
            print('Since the household includes an elderly or disabled member, the resource limit is ${}'.format(resource_limit))
        else:
            resource_limit = resource_limit_non_elderly_or_disabled
            print('Since the household does not include an elderly or disabled member, the resource limit is ${}.'.format(resource_limit))

        if resource_limit:
            below_resource_limit = (self.resources <= resource_limit)
            print('Eligibility factor -- Are household resources below the asset limit? {}'.format(below_resource_limit))
            print('')
        else:
            print('No asset test / resource limit because of state BBCE.')
            below_resource_limit = True # Hack for now

        print('\033[1mOverall: \033[0m')
        if self.household_includes_elderly_or_disabled:
            print('Since the household includes an elderly or disabled member, overall eligibility is determined by: net income limit + resource limit, depending on the state.')
            overall_eligibility = below_net_income_limit and below_resource_limit
        else:
            print('Since the household does not include an elderly or disabled member, overall eligibility is determined by: net income limit + gross income limit + resource limit, depending on the state.')
            overall_eligibility = below_net_income_limit and below_gross_income_limit and below_resource_limit

        print('')
        print('\033[1mEligible?: {}\033[0m'.format(overall_eligibility))
        print('')
        return overall_eligibility

    def estimated_monthly_benefit(self, eligible):
        if not eligible:
            return 0

        print('\033[1m💻 Estimating monthly benefit... \033[0m')

        max_monthly_allotment = FetchAllotments(self.state_or_territory, self.household_size, self.allotments_data).max_allotment()
        estimated_benefit = max_monthly_allotment - (self.monthly_income * 0.3)

        print('Max monthly allotment for state and household size: ${}.'.format(max_monthly_allotment))
        print('Subtract 30 percent of monthly income to determine estimated benefit.')
        print('Monthly income submitted to API: ${}.'.format(self.monthly_income))
        print('')

        if 0 > estimated_benefit:
            print("\033[1mEligibile, but monthly income results in zero benefit.\033[0m")
            estimated_benefit = 0

        print('\033[1mEstimated monthly benefit: ${}. \033[0m'.format(estimated_benefit))
        print('')

        return estimated_benefit
