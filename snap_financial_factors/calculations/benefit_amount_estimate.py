from snap_financial_factors.program_data_api.fetch_max_allotments import FetchMaxAllotments
from snap_financial_factors.program_data_api.fetch_min_allotments import FetchMinAllotments
from snap_financial_factors.calculations.benefit_amount_result import BenefitAmountResult


class BenefitAmountEstimate:
    def __init__(self,
                 state_or_territory,
                 household_size,
                 max_allotments,
                 min_allotments,
                 is_eligible,
                 net_income,
                 use_emergency_allotment: bool):
        self.state_or_territory = state_or_territory
        self.household_size = household_size
        self.max_allotments = max_allotments
        self.min_allotments = min_allotments
        self.is_eligible = is_eligible
        self.net_income = net_income
        self.use_emergency_allotment = use_emergency_allotment

    def calculate(self):
        if not self.is_eligible:
            return BenefitAmountResult(
                name='Estimated Benefit Calculation',
                amount=0,
                explanation=['Likely not eligible for SNAP.'],
                sort_order=5
            )

        if self.use_emergency_allotment:
            return self.calculate_with_emergency_allotment()
        else:
            return self.calculate_without_emergency_allotment()

    def calculate_with_emergency_allotment(self):
        explanation_intro = (
            'Because this state is offering an emergency SNAP benefit amount in response ' +
            'to the current crisis, a household may receive the maximum monthly ' +
            'benefit amount for their household size.'
        )
        explanation = [explanation_intro]

        max_allotment = FetchMaxAllotments(self.state_or_territory,
                                           self.household_size,
                                           self.max_allotments).calculate()

        max_allotment_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf'
        max_allotment_explanation = (
            f"In this case, the estimated benefit amount is ${max_allotment}. " +
            f"<a class='why why-small' href='{max_allotment_pdf_url}' target='_blank'>why?</a>"
        )
        explanation.append(max_allotment_explanation)

        return BenefitAmountResult(
            name='Estimated Benefit Calculation',
            amount=max_allotment,
            explanation=explanation,
            sort_order=5
        )

    def calculate_without_emergency_allotment(self):
        explanation_intro = (
            'To determine the estimated amount of SNAP benefit, we start ' +
            'with the maximum allotment and then subtract 30% of net income ' +
            '(income minus deductions).'
        )
        explanation = [explanation_intro]

        max_allotment = FetchMaxAllotments(self.state_or_territory,
                                           self.household_size,
                                           self.max_allotments).calculate()

        max_allotment_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Maximum-Allotments-Deductions.pdf'
        max_allotment_explanation = (
            f"The maximum allotment for this household is ${max_allotment}. " +
            f"<a class='why why-small' href='{max_allotment_pdf_url}' target='_blank'>why?</a>"
        )
        explanation.append(max_allotment_explanation)

        min_allotment = FetchMinAllotments(self.state_or_territory,
                                           self.household_size,
                                           self.min_allotments).calculate()
        if min_allotment:
            min_allotment_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Minimum-Allotments.pdf'
            min_allotment_explanation = (
                f"There is also a minimum monthly allotmnet for this household of ${min_allotment}. " +
                f"<a class='why why-small' href='{min_allotment_pdf_url}' target='_blank'>why?</a>"
            )
            explanation.append(min_allotment_explanation)

        thirty_percent_net_income = round(self.net_income * 0.3)
        estimated_benefit = max_allotment - thirty_percent_net_income

        calculation_explanation = (
            f"The household net monthly income is ${self.net_income}. " +
            f"Thirty percent of ${self.net_income} is ${thirty_percent_net_income}. " +
            "So to calculate the estimated benefit, take the following:"
        )
        explanation.append(calculation_explanation)
        explanation.append('')
        calcuation_math_explanation = (
            f"${max_allotment} - ${thirty_percent_net_income} = ${estimated_benefit} estimated benefit"
        )
        explanation.append(calcuation_math_explanation)

        if min_allotment and (min_allotment > estimated_benefit):
            estimated_benefit = min_allotment
            min_allotment_applied_explanation = (
                'Since this is below the minimum allotment, apply the minimum ' +
                f"allotment amount of ${min_allotment} instead."
            )
            explanation.append(min_allotment_applied_explanation)

        if 0 > estimated_benefit:
            estimated_benefit = 0
            zero_benefit_explanation = (
                "In this case, although the household is eligible, because of " +
                "their income the calcuation results in zero estimated monthly benefit."
            )
            explanation.append(zero_benefit_explanation)

        final_amount_explanation = (
            f"This gives us an estimated monthly benefit of <strong>${estimated_benefit}</strong>."
        )
        explanation.append(final_amount_explanation)

        return BenefitAmountResult(
            name='Estimated Benefit Calculation',
            amount=estimated_benefit,
            explanation=explanation,
            sort_order=5
        )
