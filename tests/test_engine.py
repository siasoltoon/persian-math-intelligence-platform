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


def test_radical_equation_with_real_domain_is_verified():
    result = process("معادله زیر را در اعداد حقیقی حل کنید: √(x + 5) + √(x - 1) = 4")
    assert result.solver.success
    assert result.solver.value == (sp.Rational(41, 16),)
    assert result.verification is not None and result.verification.verified


def test_derivative_word_problem_is_verified():
    result = process("مشتق تابع زیر را به دست آورید: f(x) = (x² + 1)³ / (x - 2)")
    assert result.solver.success
    x = sp.Symbol("x")
    expected = sp.diff((x**2 + 1) ** 3 / (x - 2), x)
    assert sp.simplify(result.solver.value - expected) == 0
    assert result.verification is not None and result.verification.verified


def test_indefinite_integral_word_problem_is_verified():
    result = process("انتگرال زیر را محاسبه کنید: ∫ x² ln(x) dx")
    assert result.solver.success
    x = sp.Symbol("x")
    assert sp.simplify(sp.diff(result.solver.value, x) - x**2 * sp.log(x)) == 0
    assert result.verification is not None and result.verification.verified


def test_definite_integral_word_problem_is_verified():
    result = process("انتگرال زیر را به صورت دقیق محاسبه کنید: ∫₀¹ x² / (1 + x²) dx")
    assert result.solver.success
    assert result.solver.value == 1 - sp.pi / 4
    assert result.verification is not None and result.verification.verified


def test_limit_word_problem_is_verified():
    result = process("حد زیر را محاسبه کنید: lim(x→0) [sin(x) - x + x³/6] / x⁵")
    assert result.solver.success
    assert result.solver.value == sp.Rational(1, 120)
    assert result.verification is not None and result.verification.verified


def test_linear_system_word_problem_is_verified():
    prompt = "دستگاه معادلات زیر را حل کنید:\n\nx + y + z = 6\n2x - y + 3z = 9\n3x + 2y - z = 4"
    result = process(prompt)
    assert result.solver.success
    assert result.solver.value == [{sp.Symbol("x"): 1, sp.Symbol("y"): 2, sp.Symbol("z"): 3}]
    assert result.verification is not None and result.verification.verified


def test_function_analysis_word_problem_is_verified():
    result = process(
        "تابع زیر را در نظر بگیرید:\n\n"
        "f(x) = x³ - 3x² - 9x + 27\n\n"
        "1. تمام نقاط بحرانی تابع را پیدا کنید.\n"
        "2. مشخص کنید هر نقطه ماکزیمم یا مینیمم نسبی است.\n"
        "3. بازه‌های صعود و نزول تابع را تعیین کنید.\n"
        "4. نقاط عطف تابع را پیدا کنید.\n"
        "5. جدول تغییرات تابع را ارائه دهید.\n"
        "6. پاسخ‌ها را با محاسبات مستقل بررسی کنید."
    )
    assert result.solver.success
    value = result.solver.value
    assert value["critical_points"] == ((-1, 32, "max"), (3, 0, "min"))
    assert value["inflection_points"] == ((1, 16),)
    assert result.verification is not None and result.verification.verified


def test_second_derivative_is_verified():
    result = process("مشتق مرتبه 2 تابع f(x) = x^4 - 2x^2 + 1 را به دست آورید.")
    assert result.solver.success
    x = sp.Symbol("x")
    assert sp.simplify(result.solver.value - sp.diff(x**4 - 2 * x**2 + 1, x, 2)) == 0
    assert result.verification is not None and result.verification.verified


def test_taylor_series_is_verified():
    result = process("بسط تیلور f(x) = sin(x) حول x = 0 تا مرتبه 6 را به دست آورید.")
    assert result.solver.success
    x = sp.Symbol("x")
    assert result.solver.value == sp.series(sp.sin(x), x, 0, 6)
    assert result.verification is not None and result.verification.verified


def test_finite_sum_is_verified():
    result = process("مجموع از 1 تا 10: n^2")
    assert result.solver.success
    assert result.solver.value == 385
    assert result.verification is not None and result.verification.verified


def test_matrix_determinant_is_verified():
    result = process("دترمینان ماتریس [[1,2],[3,4]] را محاسبه کنید.")
    assert result.solver.success
    assert result.solver.value == -2
    assert result.verification is not None and result.verification.verified

def test_matrix_determinant_with_spaced_rows_is_verified():
    result = process("دترمینان A را محاسبه کنید: A = [[2, 1], [3, 4]]")
    assert result.solver.success
    assert result.solver.value == 5
    assert result.verification is not None and result.verification.verified


def test_statistics_are_verified():
    result = process("میانگین، میانه و واریانس داده‌های زیر را محاسبه کنید: 1,2,3,4,5")
    assert result.solver.success
    assert result.solver.value["mean"] == 3
    assert result.solver.value["median"] == 3
    assert result.solver.value["variance"] == 2
    assert result.verification is not None and result.verification.verified


def test_combinations_are_verified():
    result = process("تعداد ترکیب 2 از 5 را به دست آورید.")
    assert result.solver.success
    assert result.solver.value == 10
    assert result.verification is not None and result.verification.verified


def test_number_theory_is_verified():
    result = process("تجزیه به عوامل اول عدد 360 را به دست آورید.")
    assert result.solver.success
    assert result.solver.value == {2: 3, 3: 2, 5: 1}
    assert result.verification is not None and result.verification.verified


def test_gcd_and_lcm_are_verified():
    gcd_result = process("ب.م.م 84 و 126 را محاسبه کنید.")
    lcm_result = process("ک.م.م 12 و 18 را محاسبه کنید.")
    assert gcd_result.solver.value == 42
    assert lcm_result.solver.value == 36
    assert gcd_result.verification is not None and gcd_result.verification.verified
    assert lcm_result.verification is not None and lcm_result.verification.verified


def test_circle_geometry_is_verified():
    result = process("مساحت دایره با شعاع 3 را محاسبه کنید.")
    assert result.solver.success
    assert result.solver.value == 9 * sp.pi
    assert result.verification is not None and result.verification.verified


def test_trigonometric_equation_is_verified():
    result = process("معادله مثلثاتی: sin(x) = 0")
    assert result.solver.success
    assert result.verification is not None and result.verification.verified
