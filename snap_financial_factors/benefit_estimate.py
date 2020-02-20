import yaml
from snap_financial_factors.tests.asset_test import AssetTest
from snap_financial_factors.tests.gross_income_test import GrossIncomeTest
from snap_financial_factors.tests.net_income_test import NetIncomeTest
from snap_financial_factors.fetch_allotments import FetchAllotments
from snap_financial_factors.fetch_income_limits import FetchIncomeLimits

class BenefitEstimate:
    def __init__(self, input_data):
        # Load user input data
        self.input_data = input_data
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
        net_income_test = NetIncomeTest(self.input_data,
                                        self.deductions_data,
                                        income_limits)

        tests = [ net_income_test ]

        if not self.household_includes_elderly_or_disabled:
            gross_income_test = GrossIncomeTest(self.input_data,
                                                income_limits,
                                                gross_income_limit_factor)
            tests.append(gross_income_test)

        has_asset_test = resource_limit_elderly_or_disabled or \
            resource_limit_elderly_or_disabled_income_twice_fpl or \
            resource_limit_non_elderly_or_disabled

        if has_asset_test:
            asset_test = AssetTest(self.input_data,
                                   resource_limit_elderly_or_disabled,
                                   resource_limit_non_elderly_or_disabled)
            tests.append(asset_test)

        test_results = list(map(self.calculate_test_result, tests))

        overall_eligibility = all(test_results)

        print('')
        print('\033[1mEligible?: {}\033[0m'.format(overall_eligibility))
        print('')

        return overall_eligibility

    @staticmethod
    def calculate_test_result(test):
        return test.calculate()

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
