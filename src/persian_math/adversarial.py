from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class AdversarialCase:
    case_id: str
    expression: str
    expected_success: bool


CASES = (
    AdversarialCase("division_by_zero", "1/0", False),
    AdversarialCase("zero_over_zero", "0/0", False),
    AdversarialCase("negative_root", "sqrt(-1)", True),
    AdversarialCase("log_zero", "log(0)", True),
    AdversarialCase("nested_fraction", "(1/(x+1))/(2/x)", True),
    AdversarialCase("ambiguous_minus", "--2", True),
)


def safe_parse(case: AdversarialCase) -> bool:
    try:
        expression = sp.sympify(case.expression)
        return expression not in (sp.zoo, sp.nan)
    except (TypeError, ValueError, SyntaxError, sp.SympifyError):
        return False


def run_adversarial() -> tuple[tuple[str, bool, bool], ...]:
    return tuple((case.case_id, safe_parse(case), case.expected_success) for case in CASES)
