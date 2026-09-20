import sympy as sp

from persian_math.canonical import (
    normalize_math_text,
    parse_equation,
    parse_expression,
    parse_inequality,
    parse_matrix,
    parse_system,
)


def test_persian_digits_and_operators_are_normalized():
    assert normalize_math_text("  ۲ × ۳ − ۱  ") == "2 * 3 - 1"


def test_parse_expression():
    result = parse_expression("۲^۳")
    assert result.expression == 8


def test_parse_equation():
    lhs, rhs = parse_equation("x + 2 = 5")
    assert lhs == sp.Symbol("x") + 2
    assert rhs == 5


def test_inequality_and_system_parsing():
    lhs, op, rhs = parse_inequality("x^2 <= 4")
    assert op == "<=" and lhs == sp.Symbol("x")**2 and rhs == 4
    system = parse_system("x + y = 3\n2*x - y = 0")
    assert len(system) == 2


def test_matrix_and_function_normalization():
    matrix = parse_matrix("[[1, 2], [3, 4]]")
    assert matrix.shape == (2, 2)
    assert normalize_math_text("√(x²) + π") == "sqrt(x**2) + pi"
