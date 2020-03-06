from snap_financial_factors.deductions.deduction_result import DeductionResult


class ChildSupportPaymentsDeduction:
    '''
    Calculates deduction for court-ordered (legally owed) child support payments.
    '''

    def __init__(self,
                 child_support_payments_treatment: str,
                 court_ordered_child_support_payments: int) -> None:
        self.child_support_payments_treatment = child_support_payments_treatment
        self.court_ordered_child_support_payments = court_ordered_child_support_payments

    def calculate(self) -> DeductionResult:
        if self.child_support_payments_treatment != 'DEDUCT':
            return DeductionResult(
                result=0,
                explanation=[
                    'Court-ordered child support payments are not deductible in this state.'
                ]
            )

        if self.court_ordered_child_support_payments == 0:
            return DeductionResult(
                result=0,
                explanation=[
                    'This household does not make monthly court-ordered ' +
                    'child support payments, so the child-support payment ' +
                    'deduction does not apply.'
                ]
            )

        return DeductionResult(
            result=(self.court_ordered_child_support_payments),
            explanation=[
                "Next, we deduct the monthly cost of court-ordered " +
                f"child support payments: ${self.court_ordered_child_support_payments}."
            ]
        )
