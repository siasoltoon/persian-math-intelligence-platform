import sympy as sp

from persian_math.canonical import parse_expression
from persian_math.verification import verify_equation_independently, verify_expression_result


def test_expression_verification_has_numeric_recheck() -> None:
    expression = parse_expression("x^2 + 2*x + 1").expression
    result = verify_expression_result(expression, (sp.Symbol("x") + 1) ** 2)
    assert result.verified
    assert "independent_numeric_recheck" in result.evidence


def test_equation_verification_uses_alternate_solver_path() -> None:
    x = sp.Symbol("x")
    result = verify_equation_independently(2 * x + 3, 7, x, (sp.Integer(2),))
    assert result.verified
    assert "independent_solver_agreement" in result.evidence
