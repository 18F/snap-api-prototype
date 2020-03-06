from snap_financial_factors.tests.test_result import TestResult


class NetIncomeTest:
    '''
    Evaluates net income against the appropriate net income threshold.
    '''

    def __init__(self, net_income, income_limits):
        self.net_income = net_income
        self.income_limits = income_limits

    def calculate(self) -> TestResult:
        net_income = self.net_income
        net_monthly_income_limit = self.income_limits.net_monthly_income_limit()
        below_net_income_limit = net_monthly_income_limit > net_income

        explanation = []
        explanation_intro = (
            "To be eligible for SNAP, a household's net income needs to be below " +
            "the net monthly income limit."
        )
        explanation.append(explanation_intro)

        income_limits_pdf_url = 'https://fns-prod.azureedge.net/sites/default/files/media/file/FY20-Income-Eligibility-Standards.pdf'
        net_monthly_income_limit_explanation = (
            f"The net monthly income limit is ${net_monthly_income_limit}. " +
            f"<a class='why why-small' href='{income_limits_pdf_url}' target='_blank'>why?</a>"
        )
        explanation.append(net_monthly_income_limit_explanation)

        result_to_words = {
            True: 'passes',
            False: 'does not meet'
        }
        result_in_words = result_to_words[below_net_income_limit]
        result_explanation = (
            f"Since the household net income is ${net_income}, " +
            f"this household <strong>{result_in_words}</strong> the net income test."
        )
        explanation.append(result_explanation)

        return TestResult(
            name='Net Income Test',
            result=below_net_income_limit,
            explanation=explanation,
            sort_order=3,
        )
