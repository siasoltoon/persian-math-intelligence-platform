import sympy as sp

from persian_math.solver import (
    differentiate,
    integrate,
    limit,
    optimize,
    solve,
    solve_complex,
    solve_matrix,
    solve_polynomial,
    solve_probability,
    solve_statistics,
)
from persian_math.verification import (
    compare_independent_methods,
    verify_equation_solution,
    verify_expression_result,
    verify_solution_set,
)


def test_expression_solver():
    assert solve("2 + 3 * 4").value == 14


def test_equation_solver():
    assert solve("x + 2 = 5").value == (sp.Integer(3),)


def test_inequality_solver():
    result = solve("x^2 < 4")
    assert result.success
    assert result.value == sp.And(sp.Lt(-2, sp.Symbol("x")), sp.Lt(sp.Symbol("x"), 2))


def test_polynomial_solver():
    result = solve_polynomial(sp.Symbol("x") ** 2 - 1, sp.Symbol("x"))
    assert set(result.value) == {-1, 1}


def test_calculus_solvers():
    x = sp.Symbol("x")
    assert differentiate(x**3, x).value == 3 * x**2
    assert integrate(2 * x, x).value == x**2
    assert limit(sp.sin(x) / x, x, 0).value == 1


def test_matrix_solver():
    result = solve_matrix(sp.Matrix([[1, 2], [3, 4]]), "det")
    assert result.value == -2


def test_probability_and_statistics():
    assert solve_probability(1, 4).value == sp.Rational(1, 4)
    result = solve_statistics([1, 2, 3])
    assert result.success and result.value["mean"] == 2


def test_optimization_and_complex():
    x = sp.Symbol("x")
    assert optimize(x**2, x).success
    assert solve_complex(x**2 + 1, x).success


def test_verification_accepts_correct_result():
    assert verify_expression_result(sp.Integer(2) + 3, 5).verified


def test_verification_rejects_wrong_result():
    assert not verify_expression_result(sp.Integer(2) + 3, 6).verified


def test_equation_substitution():
    x = sp.Symbol("x")
    assert verify_equation_solution(x + 2, 5, x, 3).verified


def test_solution_set_verification():
    x = sp.Symbol("x")
    assert verify_solution_set(x**2, 1, x, (-1, 1)).verified


def test_independent_method_agreement():
    x = sp.Symbol("x")
    assert compare_independent_methods(x + 1, x + 1, 1 + x).verified
