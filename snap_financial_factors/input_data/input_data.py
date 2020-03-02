from typing import Dict


class InputData:
    '''
    Holds input data to API.
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
