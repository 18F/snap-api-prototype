from snap_financial_factors.input_data.input_data import InputData


class GrossIncomeTest:
    def __init__(self,
                 input_data: InputData,
                 income_limits,
                 gross_income_limit_factor,
                 child_support_payments_deductible: bool) -> None:
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data.state_or_territory
        self.monthly_job_income = input_data.monthly_job_income
        self.monthly_non_job_income = input_data.monthly_non_job_income
        self.household_size = input_data.household_size
        self.household_includes_elderly_or_disabled = input_data.household_includes_elderly_or_disabled
        self.resources = input_data.resources

        self.income_limits = income_limits
        self.gross_income_limit_factor = gross_income_limit_factor

        # If child support payments are not deductible, they are counted as
        # exclusions from gross income.
        self.child_support_payments_deductible = child_support_payments_deductible
        self.court_ordered_child_support_payments = input_data.court_ordered_child_support_payments

    def calculate(self):
        if self.household_includes_elderly_or_disabled:
            return {
                'result': True,
                'reason': {
                    'test_name': 'Gross Income Test',
                    'test_passed?': True,
                    'description': ['Households with an elderly or disabled member do not need to meet the gross income test.']
                }
            }

        # The gross income limited is calculated as a percentage of the net
        # income limit, which is based on the federal poverty level.
        explanation = ['Next, we check gross income (total income without deductions).']

        net_monthly_income_limit = self.income_limits.net_monthly_income_limit()
        gross_monthly_income_limit = round(self.gross_income_limit_factor * net_monthly_income_limit)

        income_limits_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Income-Eligibility-Standards.pdf'
        gross_monthly_income_limit_explanation = (
            f"The gross monthly income limit is ${gross_monthly_income_limit}. " +
            f"<a class='why why-small' href='{income_limits_pdf_url}' target='_blank'>why?</a>"
        )
        explanation.append(gross_monthly_income_limit_explanation)

        # Calculate monthly income:
        monthly_income = self.monthly_job_income + self.monthly_non_job_income

        # Exclude child support payments depending on state option:
        if (self.court_ordered_child_support_payments > 0
                and not self.child_support_payments_deductible):
            child_support_payments_explanation = (
                'In this state, court-ordered child support payments are ' +
                'counted as a gross income exclusion. The gross income is ' +
                'adjusted to exclude monthly court-ordered child support:'
            )
            explanation.append(child_support_payments_explanation)

            monthly_income_minus_child_support = (
                monthly_income - self.court_ordered_child_support_payments
            )

            child_support_payments_math = (
                f"${monthly_income} - " +
                f"${self.court_ordered_child_support_payments} = " +
                f"${monthly_income_minus_child_support} adjusted gross income"
            )
            explanation.append(child_support_payments_math)

            monthly_income = monthly_income_minus_child_support

        # Result:
        below_gross_income_limit = (gross_monthly_income_limit > monthly_income)

        result_to_words = {
            True: 'passes',
            False: 'does not meet'
        }
        result_in_words = result_to_words[below_gross_income_limit]
        result_explanation = (
            f"Since the household total income is ${monthly_income}, " +
            f"this household <strong>{result_in_words}</strong> the gross income test."
        )
        explanation.append(result_explanation)

        return {
            'result': below_gross_income_limit,
            'reason': {
                'test_name': 'Gross Income Test',
                'test_passed?': below_gross_income_limit,
                'description': explanation,
                'sort_order': 2,
            }
        }
