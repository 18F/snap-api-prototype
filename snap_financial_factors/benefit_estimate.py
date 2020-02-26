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
        self.monthly_income = input_data['monthly_income']
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
        """
        Only public method for this class. Returns eligibility information,
        estimated monthly benefits, and reasons behind the output.

        Returns a dictionary shaped like this:
        {
            'eligible': <bool>,
            'estimated_monthly_benefit': <decimal> (U.S. dollar),
            'reasons': <array of dictionaries>,
            'state_webiste': <str> (U.S. state website URL for referral)
        }
        """

        eligibility_calculation = self.__eligibility_calculation()
        is_eligible = eligibility_calculation['eligible']
        reasons = eligibility_calculation['reasons']
        net_income = eligibility_calculation['net_income']

        estimated_benefit = self.__estimated_monthly_benefit(is_eligible, net_income)
        estimated_benefit_amount = estimated_benefit['amount']
        estimated_benefit_reason = estimated_benefit['reason']
        reasons.append(estimated_benefit_reason)

        state_website = self.state_websites[self.state_or_territory]

        return {
            'eligible': is_eligible,
            'estimated_monthly_benefit': estimated_benefit_amount,
            'reasons': reasons,
            'state_website': state_website
            }

    def __eligibility_calculation(self):
        """Private method. Returns estimated SNAP eligibility plus reasons
        behind the calculation.

        Mostly responsible for reading in parameters that differ by U.S. state,
        or passing in default federal parameters in some cases.

        Returns a dictionary shaped like this:
        {
            'eligible': <bool>,
            'reasons': <array of dictionaries>,
        }
        """

        state_bbce_data = self.bbce_data[self.state_or_territory][2020]
        state_uses_bbce = state_bbce_data['uses_bbce']

        if state_uses_bbce:
            return self.__eligibility_calculation_with_params(
                state_bbce_data['gross_income_limit_factor'],
                state_bbce_data['resource_limit_elderly_or_disabled'],
                state_bbce_data['resource_limit_elderly_or_disabled_income_twice_fpl'],
                state_bbce_data['resource_limit_non_elderly_or_disabled'],
            )
        else:
            # SNAP federal policy defaults
            return self.__eligibility_calculation_with_params(
                gross_income_limit_factor=1.3,
                resource_limit_elderly_or_disabled=3500,
                resource_limit_elderly_or_disabled_income_twice_fpl=3500,
                resource_limit_non_elderly_or_disabled=2250,
            )

    def __eligibility_calculation_with_params(self,
                                              gross_income_limit_factor,
                                              resource_limit_elderly_or_disabled,
                                              resource_limit_elderly_or_disabled_income_twice_fpl,
                                              resource_limit_non_elderly_or_disabled):
        """
        Private method. Breaks eligibility determiniation into component
        classes; asks each of those classes to run calculations and return
        reasons.
        """
        input_data = self.input_data
        deductions_data = self.deductions_data
        income_limit_data = self.income_limit_data
        state_or_territory = self.state_or_territory
        household_size = self.household_size

        income_limits = FetchIncomeLimits(state_or_territory, household_size, income_limit_data)

        net_income = NetIncome(input_data, deductions_data).calculate()

        net_income_test = NetIncomeTest(net_income, income_limits)

        asset_test = AssetTest(input_data,
                               resource_limit_elderly_or_disabled,
                               resource_limit_non_elderly_or_disabled)

        gross_income_test = GrossIncomeTest(input_data,
                                            income_limits,
                                            gross_income_limit_factor)

        tests = [net_income_test, asset_test, gross_income_test]

        test_calculations = [test.calculate() for test in tests]
        test_results = [calculation['result'] for calculation in test_calculations]
        reasons = [calculation['reason'] for calculation in test_calculations]
        overall_eligibility = all(test_results)

        return {
            'eligible': overall_eligibility,
            'reasons': reasons,
            'net_income': net_income,
        }

    def __estimated_monthly_benefit(self, is_eligible, net_income):
        """
        Returns estimate of monthly benefit, plus reasons behind its decision.
        """

        if not is_eligible:
            return {
                'amount': 0,
                'reason': {
                    'test_name': 'Estimated Benefit Calculation',
                    'description': ['Not Eligible']
                }
            }

        description = []
        state_or_territory = self.state_or_territory
        household_size = self.household_size
        allotments_data = self.allotments_data

        fetch_allotments = FetchAllotments(state_or_territory,
                                           household_size,
                                           allotments_data)
        max_monthly_allotment = fetch_allotments.max_allotment()

        estimated_benefit = max_monthly_allotment - (net_income * 0.3)

        description.append('Max monthly allotment for state and household size: ${}.'.format(max_monthly_allotment))
        description.append('Subtract 30 percent of net monthly income to determine estimated benefit.')
        description.append('Net monthly income: ${}.'.format(net_income))

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
