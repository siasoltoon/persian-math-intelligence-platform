import sympy as sp

from persian_math.canonical import normalize_math_text, parse_equation, parse_expression


def test_persian_digits_and_operators_are_normalized():
    assert normalize_math_text("  ۲ × ۳ − ۱  ") == "2 * 3 - 1"


def test_parse_expression():
    result = parse_expression("۲^۳")
    assert result.expression == 8


def test_parse_equation():
    lhs, rhs = parse_equation("x + 2 = 5")
    assert lhs == sp.Symbol("x") + 2
    assert rhs == 5
