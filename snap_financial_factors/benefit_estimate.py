from typing import Dict
from snap_financial_factors.input_data.input_data import InputData

import yaml

from snap_financial_factors.income.net_income import NetIncome
from snap_financial_factors.income.gross_income import GrossIncome

from snap_financial_factors.tests.asset_test import AssetTest
from snap_financial_factors.tests.gross_income_test import GrossIncomeTest
from snap_financial_factors.tests.net_income_test import NetIncomeTest

from snap_financial_factors.calculations.benefit_amount_estimate import BenefitAmountEstimate
from snap_financial_factors.calculations.benefit_amount_result import BenefitAmountResult

from snap_financial_factors.program_data_api.fetch_income_limits import FetchIncomeLimits


class BenefitEstimate:
    def __init__(self, parsed_input_data: InputData):
        self.input_data = parsed_input_data
        self.state_or_territory = self.input_data.state_or_territory
        self.monthly_job_income = self.input_data.monthly_job_income
        self.monthly_non_job_income = self.input_data.monthly_non_job_income
        self.household_size = self.input_data.household_size
        self.household_includes_elderly_or_disabled = self.input_data.household_includes_elderly_or_disabled
        self.resources = self.input_data.resources
        self.dependent_care_costs = self.input_data.dependent_care_costs

        # Load SNAP program data as YAML
        self.state_options_data = yaml.safe_load(open('./program_data/state_options.yaml', 'r'))
        self.income_limit_data = yaml.safe_load(open('./program_data/income_limits.yaml', 'r'))
        self.deductions_data = yaml.safe_load(open('./program_data/deductions.yaml', 'r'))
        self.max_allotments = yaml.safe_load(open('./program_data/max_allotments.yaml', 'r'))
        self.min_allotments = yaml.safe_load(open('./program_data/min_allotments.yaml', 'r'))

    def calculate(self) -> Dict:
        """
        Only public method for this class. Returns eligibility information,
        estimated monthly benefits, and reasons behind the output.
        """

        eligibility_calculation = self.__eligibility_calculation()
        is_eligible = eligibility_calculation['eligible']
        eligibility_factors = eligibility_calculation['eligibility_factors']
        net_income = eligibility_calculation['net_income']

        estimated_benefit = self.__estimated_monthly_benefit(is_eligible, net_income)
        estimated_benefit_amount = estimated_benefit.amount
        eligibility_factors.append(estimated_benefit.__dict__)

        state_website = self.state_options_data[self.state_or_territory][2020]['website']

        return {
            'eligible': is_eligible,
            'estimated_monthly_benefit': estimated_benefit_amount,
            'eligibility_factors': eligibility_factors,
            'state_website': state_website
            }

    def __eligibility_calculation(self):
        """Private method. Returns estimated SNAP eligibility plus reasons
        behind the calculation.

        Mostly responsible for reading in parameters that differ by U.S. state,
        or passing in default federal parameters in some cases.
        """

        state_options = self.state_options_data[self.state_or_territory][2020]

        # Validation for state options data on child support payments treatment
        child_support_payments_treatment = state_options['child_support_payments_treatment']
        if child_support_payments_treatment not in ['DEDUCT', 'EXCLUDE']:
            raise ValueError('Unknown value for child_support_payments_treatment.')

        state_uses_bbce = state_options['uses_bbce']

        if state_uses_bbce:
            return self.__eligibility_calculation_with_params(
                state_options['gross_income_limit_factor'],
                state_options['resource_limit_elderly_or_disabled'],
                state_options['resource_limit_elderly_or_disabled_income_twice_fpl'],
                state_options['resource_limit_non_elderly_or_disabled'],
                child_support_payments_treatment
            )
        else:
            # SNAP federal policy defaults
            return self.__eligibility_calculation_with_params(
                gross_income_limit_factor=1.3,
                resource_limit_elderly_or_disabled=3500,
                resource_limit_elderly_or_disabled_income_twice_fpl=3500,
                resource_limit_non_elderly_or_disabled=2250,
                child_support_payments_treatment=child_support_payments_treatment
            )

    def __eligibility_calculation_with_params(self,
                                              gross_income_limit_factor,
                                              resource_limit_elderly_or_disabled,
                                              resource_limit_elderly_or_disabled_income_twice_fpl,
                                              resource_limit_non_elderly_or_disabled,
                                              child_support_payments_treatment):
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

        gross_income_calculator = GrossIncome(input_data,
                                              child_support_payments_treatment)

        gross_income_calculation = gross_income_calculator.calculate()
        gross_income = gross_income_calculation.result

        net_income_calculator = NetIncome(input_data,
                                          gross_income,
                                          deductions_data,
                                          child_support_payments_treatment)

        net_income_calculation = net_income_calculator.calculate()
        net_income = net_income_calculation.result

        income_limits = FetchIncomeLimits(state_or_territory, household_size, income_limit_data)
        net_income_test = NetIncomeTest(net_income, income_limits)

        asset_test = AssetTest(input_data,
                               resource_limit_elderly_or_disabled,
                               resource_limit_non_elderly_or_disabled)

        gross_income_test = GrossIncomeTest(input_data,
                                            gross_income,
                                            income_limits,
                                            gross_income_limit_factor)

        tests = [net_income_test, asset_test, gross_income_test]

        test_calculations = [test.calculate() for test in tests]
        test_results = [calculation.result for calculation in test_calculations]
        overall_eligibility = all(test_results)

        eligibility_factor_classes = (
            test_calculations + [gross_income_calculation, net_income_calculation]
        )

        eligibility_factors = [
            factor.__dict__ for factor in eligibility_factor_classes
        ]

        return {
            'eligible': overall_eligibility,
            'eligibility_factors': eligibility_factors,
            'net_income': net_income,
        }

    def __estimated_monthly_benefit(self,
                                    is_eligible: bool,
                                    net_income: int) -> BenefitAmountResult:
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
