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


def test_natural_language_expression_pipeline_verifies_result():
    result = process("حاصل عبارت زیر را به دست آورید: 18 + 7 × 3 - 10")
    assert result.problem.representation is not None
    assert result.problem.representation.expression == "18 + 7 * 3 - 10"
    assert result.solver.success
    assert result.solver.value == 29
    assert result.verification is not None and result.verification.verified


def test_natural_language_equation_pipeline_verifies_solution_set():
    result = process("اگر 3x + 7 = 22 باشد، مقدار x را به دست آورید.")
    assert result.problem.representation is not None
    assert result.problem.representation.expression == "3x + 7 = 22"
    assert result.solver.success
    assert result.solver.value == (5,)
    assert result.verification is not None and result.verification.verified
