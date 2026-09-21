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
\n\ndef test_natural_language_expression_pipeline_verifies_result():\n    result = process("حاصل عبارت زیر را به دست آورید: 18 + 7 × 3 - 10")\n    assert result.problem.representation is not None\n    assert result.problem.representation.expression == "18 + 7 * 3 - 10"\n    assert result.solver.success\n    assert result.solver.value == 29\n    assert result.verification is not None and result.verification.verified\n\n\ndef test_natural_language_equation_pipeline_verifies_solution_set():\n    result = process("اگر 3x + 7 = 22 باشد، مقدار x را به دست آورید.")\n    assert result.problem.representation is not None\n    assert result.problem.representation.expression == "3x + 7 = 22"\n    assert result.solver.success\n    assert result.solver.value == (5,)\n    assert result.verification is not None and result.verification.verified\n