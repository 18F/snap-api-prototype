import yaml
from snap_financial_factors.net_income import NetIncome
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
        self.monthly_earned_income = input_data['monthly_earned_income']
        self.monthly_other_income = input_data['monthly_other_income']
        self.monthly_income = self.monthly_earned_income + self.monthly_other_income
        self.household_size = input_data['household_size']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.resources = input_data['resources']

        # Load SNAP program data as YAML
        self.bbce_data = yaml.safe_load(open('./program_data/bbce.yaml', 'r'))
        self.income_limit_data = yaml.safe_load(open('./program_data/income_limits.yaml', 'r'))
        self.deductions_data = yaml.safe_load(open('./program_data/deductions.yaml', 'r'))
        self.allotments_data = yaml.safe_load(open('./program_data/allotments.yaml', 'r'))
        self.state_websites = yaml.safe_load(open('./program_data/state_websites.yaml', 'r'))

    def calculate(self):
        eligibility_calculation = self.__eligibility_calculation()
        eligible = eligibility_calculation['eligible']
        reasons = eligibility_calculation['reasons']

        estimated_monthly_benefit = self.estimated_monthly_benefit(eligible)
        estimated_monthly_benefit_amount = estimated_monthly_benefit['amount']
        estimated_monthly_benefit_reason = estimated_monthly_benefit['reason']

        reasons.append(estimated_monthly_benefit_reason)
        state_website = self.state_websites[self.state_or_territory]

        return {
            'eligible': eligible,
            'estimated_monthly_benefit': estimated_monthly_benefit_amount,
            'reasons': reasons,
            'state_website': state_website
            }

    def __eligibility_calculation(self):
        """Returns estimated SNAP eligibility plus reasons behind the calculation.

        Returns a dictionary shaped like this:
        {
            'eligible': <bool>,
            'reasons': <array of dictionaries>,
        }
        """
        state_bbce_data = self.bbce_data[self.state_or_territory][2020]
        state_uses_bbce = state_bbce_data['uses_bbce']

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

        net_income = NetIncome(self.input_data,
                               self.deductions_data,
                               self.monthly_income,
                               income_limits)

        net_income_test = NetIncomeTest(self.input_data,
                                        self.deductions_data,
                                        self.monthly_income,
                                        income_limits)

        gross_income_test = GrossIncomeTest(self.input_data,
                                            self.monthly_income,
                                            income_limits,
                                            gross_income_limit_factor)

        asset_test = AssetTest(self.input_data,
                               resource_limit_elderly_or_disabled,
                               resource_limit_non_elderly_or_disabled)

        tests = [ net_income_test, asset_test, gross_income_test ]

        test_calculations = [test.calculate() for test in tests]
        test_results = [calculation['result'] for calculation in test_calculations]
        reasons = [calculation['reason'] for calculation in test_calculations]
        overall_eligibility = all(test_results)

        return {
            'eligible': overall_eligibility,
            'reasons': reasons,
        }


    def estimated_monthly_benefit(self, eligible):
        if not eligible:
            return {
                'amount': 0,
                'reason': {
                    'test_name': 'Estimated Benefit Calculation',
                    'description': ['Not Eligible']
                }
            }

        description = []

        max_monthly_allotment = FetchAllotments(self.state_or_territory, self.household_size, self.allotments_data).max_allotment()
        estimated_benefit = max_monthly_allotment - (self.monthly_income * 0.3)

        description.append('Max monthly allotment for state and household size: ${}.'.format(max_monthly_allotment))
        description.append('Subtract 30 percent of monthly income to determine estimated benefit.')
        description.append('Monthly income submitted to API: ${}.'.format(self.monthly_income))

        if 0 > estimated_benefit:
            description.append("Eligibile, but monthly income results in zero benefit.")
            estimated_benefit = 0

        description.append('Estimated monthly benefit: ${}.'.format(estimated_benefit))

        return {
            'amount': estimated_benefit,
            'reason': {
                'test_name': 'Estimated Benefit Calculation',
                'description': description
            }
        }
