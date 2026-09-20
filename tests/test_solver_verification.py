import sympy as sp

from persian_math.solver import solve
from persian_math.verification import verify_equation_solution, verify_expression_result


def test_expression_solver():
    result = solve("2 + 3 * 4")
    assert result.success
    assert result.value == 14


def test_equation_solver():
    result = solve("x + 2 = 5")
    assert result.success
    assert result.value == (sp.Integer(3),)


def test_verification_accepts_correct_result():
    result = verify_expression_result(sp.Integer(2) + 3, 5)
    assert result.verified


def test_verification_rejects_wrong_result():
    result = verify_expression_result(sp.Integer(2) + 3, 6)
    assert not result.verified


def test_equation_substitution():
    x = sp.Symbol("x")
    result = verify_equation_solution(x + 2, 5, x, 3)
    assert result.verified
