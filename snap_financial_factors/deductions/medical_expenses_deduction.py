from snap_financial_factors.deductions.deduction_result import DeductionResult


class MedicalExpensesDeduction:
    '''
    Calculates medical expenses deduction for households that include a member
    who is over 60 years old, blind, or disabled.
    '''

    def __init__(self,
                 household_includes_elderly_or_disabled: bool,
                 medical_expenses_for_elderly_or_disabled: int) -> None:
        self.household_includes_elderly_or_disabled = household_includes_elderly_or_disabled
        self.medical_expenses_for_elderly_or_disabled = medical_expenses_for_elderly_or_disabled

    def calculate(self):
        explanation = [
            "Next, deduct monthly medical expenses for elderly or disabled household members beyond $35. "
        ]

        if not self.household_includes_elderly_or_disabled:
            explanation.append(
                "In this case, there are no elderly or disabled members of " +
                "the household, so the deduction does not apply. "
            )

            return DeductionResult(
                result=0,
                is_applicable=False,
                explanation=explanation
            )

        if self.medical_expenses_for_elderly_or_disabled == 0:
            explanation.append(
                "In this case, there are no monthly medical expenses to deduct. "
            )

            return DeductionResult(
                result=0,
                is_applicable=False,
                explanation=explanation
            )

        if 35 > self.medical_expenses_for_elderly_or_disabled:
            explanation.append(
                "In this case, medical expenses are below the $35 monthly threshold for deduction. "
            )

            return DeductionResult(
                result=0,
                is_applicable=False,
                explanation=explanation
            )

        medical_expenses_deduction = self.medical_expenses_for_elderly_or_disabled - 35
        explanation.append(
            "The medical expenses deduction is equal to monthly medical expenses " +
            "beyond $35."
        )
        explanation.append('')
        explanation.append(
            f"${self.medical_expenses_for_elderly_or_disabled} - $35 = " +
            f"${medical_expenses_deduction} medical expenses deduction"
        )

        return DeductionResult(
            result=medical_expenses_deduction,
            is_applicable=True,
            explanation=explanation
        )
