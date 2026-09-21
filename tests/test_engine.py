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


def test_rectangle_area_word_problem_is_verified():
    result = process("مساحت مستطیلی با طول 12 سانتی‌متر و عرض 7 سانتی‌متر را محاسبه کنید.")
    assert result.solver.success
    assert result.solver.value == 84
    assert result.verification is not None and result.verification.verified


def test_function_evaluation_word_problem_is_verified():
    result = process("اگر f(x) = 2x² - 3x + 1 باشد، مقدار f(4) را محاسبه کنید.")
    assert result.solver.success
    assert result.solver.value == 21
    assert result.verification is not None and result.verification.verified


def test_arithmetic_sequence_sum_word_problem_is_verified():
    result = process("مجموع 20 جمله اول دنباله حسابی زیر را به دست آورید: 3, 7, 11, 15, ...")
    assert result.solver.success
    assert result.solver.value == 820
    assert result.verification is not None and result.verification.verified
