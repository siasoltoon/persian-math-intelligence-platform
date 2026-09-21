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
