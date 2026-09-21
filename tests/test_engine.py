import sympy as sp

from persian_math.engine import process


def test_expression_pipeline_verifies_result():
    result = process("۲ + ۳ × ۴")
    assert result.solver.success
    assert result.solver.value == 14
    assert result.verification is not None and result.verification.verified


def test_equation_pipeline_verifies_solution_set():
    result = process("x + 2 = 5")
    assert result.solver.success
    assert result.solver.value == (3,)
    assert result.verification is not None and result.verification.verified


def test_quadratic_equation():
    result = process("x^2 - 5*x + 6 = 0")
    assert result.solver.success
    assert set(result.solver.value) == {sp.Integer(2), sp.Integer(3)}
    assert result.verification is not None and result.verification.verified


def test_system_is_solved_and_verified():
    result = process("x + y = 3\n2*x - y = 0")
    assert result.solver.success
    assert result.verification is not None and result.verification.verified


def test_persian_operators_and_superscripts():
    result = process("۲x² + ۱")
    assert result.solver.success
    assert result.solver.value == 2 * sp.Symbol("x") ** 2 + 1
    assert result.problem.classification is not None
    assert result.problem.classification.confidence >= 0.78


def test_trigonometric_expression_is_handled_symbolically():
    result = process("sin(x)**2 + cos(x)**2")
    assert result.solver.success
    assert sp.simplify(result.solver.value - 1) == 0
    assert result.verification is not None and result.verification.verified
