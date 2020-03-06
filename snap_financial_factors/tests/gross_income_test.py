from snap_financial_factors.input_data.input_data import InputData
from snap_financial_factors.tests.test_result import TestResult


class GrossIncomeTest:
    def __init__(self,
                 input_data: InputData,
                 gross_income: bool,
                 income_limits,
                 gross_income_limit_factor) -> None:
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data.state_or_territory
        self.household_size = input_data.household_size
        self.household_includes_elderly_or_disabled = input_data.household_includes_elderly_or_disabled
        self.resources = input_data.resources
        self.gross_income = gross_income
        self.income_limits = income_limits
        self.gross_income_limit_factor = gross_income_limit_factor

    def calculate(self) -> TestResult:
        if self.household_includes_elderly_or_disabled:
            return TestResult(
                name='Gross Income Test',
                result=True,
                explanation=[
                    'Households with an elderly or disabled member do not need to meet the gross income test.'
                ],
                sort_order=2,
            )

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

        # Result:
        below_gross_income_limit = (gross_monthly_income_limit > self.gross_income)

        result_to_words = {
            True: 'passes',
            False: 'does not meet'
        }
        result_in_words = result_to_words[below_gross_income_limit]
        result_explanation = (
            f"Since the household gross income is ${self.gross_income}, " +
            f"this household <strong>{result_in_words}</strong> the gross income test."
        )
        explanation.append(result_explanation)

        return TestResult(
            name='Gross Income Test',
            result=below_gross_income_limit,
            explanation=explanation,
            sort_order=2,
        )
