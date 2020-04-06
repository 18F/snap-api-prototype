from typing import Dict


class InputData:
    '''
    Holds input data to API.

    Any new input factors must be handled here and in the ParseInputData class.
    '''

    def __init__(self, input_data: Dict) -> None:
        self.household_size = input_data['household_size']
        self.state_or_territory = input_data['state_or_territory']
        self.household_includes_elderly_or_disabled = input_data['household_includes_elderly_or_disabled']
        self.monthly_job_income = input_data['monthly_job_income']
        self.monthly_non_job_income = input_data['monthly_non_job_income']
        self.resources = input_data['resources']
        self.dependent_care_costs = input_data['dependent_care_costs']
        self.medical_expenses_for_elderly_or_disabled = input_data['medical_expenses_for_elderly_or_disabled']
        self.court_ordered_child_support_payments = input_data['court_ordered_child_support_payments']
        self.rent_or_mortgage = input_data['rent_or_mortgage']
        self.homeowners_insurance_and_taxes = input_data['homeowners_insurance_and_taxes']
        self.utility_costs = input_data['utility_costs']
        self.utility_allowance = input_data['utility_allowance']
        self.use_emergency_allotment = input_data['use_emergency_allotment']