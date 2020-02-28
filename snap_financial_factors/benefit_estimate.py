import yaml
from snap_financial_factors.calculations.net_income import NetIncome
from snap_financial_factors.calculations.benefit_amount_estimate import BenefitAmountEstimate
from snap_financial_factors.tests.asset_test import AssetTest
from snap_financial_factors.tests.gross_income_test import GrossIncomeTest
from snap_financial_factors.tests.net_income_test import NetIncomeTest
from snap_financial_factors.program_data_api.fetch_income_limits import FetchIncomeLimits
from snap_financial_factors.parse_input_data import ParseInputData


class BenefitEstimate:
    def __init__(self, input_data):
        # Load and parse user input data
        parsed_input_data = ParseInputData(input_data).parse()

        self.input_data = parsed_input_data
        self.state_or_territory = self.input_data['state_or_territory']
        self.monthly_job_income = self.input_data['monthly_job_income']
        self.monthly_non_job_income = self.input_data['monthly_non_job_income']
        self.household_size = self.input_data['household_size']
        self.household_includes_elderly_or_disabled = self.input_data['household_includes_elderly_or_disabled']
        self.resources = self.input_data['resources']
        self.dependent_care_costs = self.input_data['dependent_care_costs']

        # Load SNAP program data as YAML
        self.bbce_data = yaml.safe_load(open('./program_data/bbce.yaml', 'r'))
        self.income_limit_data = yaml.safe_load(open('./program_data/income_limits.yaml', 'r'))
        self.deductions_data = yaml.safe_load(open('./program_data/deductions.yaml', 'r'))
        self.max_allotments = yaml.safe_load(open('./program_data/max_allotments.yaml', 'r'))
        self.min_allotments = yaml.safe_load(open('./program_data/min_allotments.yaml', 'r'))
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

        net_income_calculation = NetIncome(input_data, deductions_data).calculate()
        net_income = net_income_calculation['result']
        net_income_reason = net_income_calculation['reason']

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
        reasons.append(net_income_reason)
        overall_eligibility = all(test_results)

        sorted_reasons = sorted(reasons, key=lambda reason: reason.get('sort_order', 10))

        return {
            'eligible': overall_eligibility,
            'reasons': sorted_reasons,
            'net_income': net_income,
        }

    def __estimated_monthly_benefit(self, is_eligible, net_income):
        """
        Returns estimate of monthly benefit, plus reasons behind its decision.

        Delegates to BenefitAmountEstimate class.
        """

        amount_estimate = BenefitAmountEstimate(self.state_or_territory,
                                                self.household_size,
                                                self.max_allotments,
                                                self.min_allotments,
                                                is_eligible,
                                                net_income)

        return amount_estimate.calculate()
