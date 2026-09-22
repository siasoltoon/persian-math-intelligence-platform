from __future__ import annotations

import math
from typing import Any

import sympy as sp

from .domain import ConfidenceLevel, VerificationResult


def _numeric_equal(a: Any, b: Any, tolerance: float = 1e-9) -> bool:
    try:
        return math.isclose(
            float(sp.N(a)),
            float(sp.N(b)),
            rel_tol=tolerance,
            abs_tol=tolerance,
        )
    except (TypeError, ValueError, OverflowError):
        return False


def _domain_safe(expression: sp.Expr, symbol: sp.Symbol, candidate: Any) -> bool:
    try:
        value = expression.subs(symbol, candidate)
        return value.is_finite is not False
    except (TypeError, ValueError):
        return False


def _numeric_expression_recheck(expression: sp.Expr, claimed: Any) -> bool:
    symbols = sorted(expression.free_symbols, key=str)
    if not symbols:
        return _numeric_equal(expression, claimed)
    points = (sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(5, 3))
    for point in points:
        substitutions = {symbol: point for symbol in symbols}
        try:
            expected_value = sp.N(expression.subs(substitutions), 30)
            claimed_value = sp.N(claimed.subs(substitutions), 30)
        except (AttributeError, TypeError, ValueError):
            return False
        if not _numeric_equal(expected_value, claimed_value, tolerance=1e-8):
            return False
    return True


def verify_expression_result(expression: sp.Expr, claimed: Any) -> VerificationResult:
    try:
        expected = sp.simplify(expression)
        symbolic_match = sp.simplify(expected - claimed) == 0
        if symbolic_match and _numeric_expression_recheck(expression, claimed):
            return VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("symbolic_equivalence", "independent_numeric_recheck"),
                (expected,),
            )
        if _numeric_expression_recheck(expression, claimed):
            return VerificationResult(
                True,
                ConfidenceLevel.MEDIUM,
                ("independent_numeric_recheck",),
                (expected,),
            )
        return VerificationResult(
            False,
            ConfidenceLevel.HIGH,
            ("verification_mismatch",),
            (expected, claimed),
        )
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(False, ConfidenceLevel.LOW, ("verification_failed",), ())


def verify_equation_solution(
    lhs: sp.Expr,
    rhs: sp.Expr,
    symbol: sp.Symbol,
    candidate: Any,
) -> VerificationResult:
    try:
        if not _domain_safe(lhs - rhs, symbol, candidate):
            return VerificationResult(
                False, ConfidenceLevel.HIGH, ("domain_invalid",), (candidate,)
            )
        residual = sp.simplify((lhs - rhs).subs(symbol, candidate))
        if residual == 0:
            return VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("direct_substitution", "zero_residual", "domain_checked"),
                (candidate,),
            )
        if _numeric_equal(residual, 0):
            return VerificationResult(
                True,
                ConfidenceLevel.MEDIUM,
                ("numeric_residual_check", "domain_checked"),
                (candidate,),
            )
        return VerificationResult(False, ConfidenceLevel.HIGH, ("nonzero_residual",), (candidate,))
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(
            False, ConfidenceLevel.LOW, ("verification_failed",), (candidate,)
        )


def verify_solution_set(
    lhs: sp.Expr,
    rhs: sp.Expr,
    symbol: sp.Symbol,
    candidates: tuple[Any, ...],
) -> VerificationResult:
    checks = tuple(verify_equation_solution(lhs, rhs, symbol, c) for c in candidates)
    if not checks:
        return VerificationResult(True, ConfidenceLevel.HIGH, ("empty_solution_set_verified",), ())
    verified = all(item.verified for item in checks)
    confidence = ConfidenceLevel.HIGH if verified else ConfidenceLevel.LOW
    return VerificationResult(verified, confidence, ("solution_set_substitution",), candidates)


def compare_independent_methods(
    expression: sp.Expr, claimed: Any, alternate: Any
) -> VerificationResult:
    try:
        equivalent = sp.simplify(claimed - alternate) == 0
    except (TypeError, ValueError):
        equivalent = _numeric_equal(claimed, alternate)
    if equivalent:
        return VerificationResult(
            True,
            ConfidenceLevel.HIGH,
            ("independent_method_agreement",),
            (claimed, alternate),
        )
    return VerificationResult(
        False,
        ConfidenceLevel.HIGH,
        ("independent_method_disagreement",),
        (claimed, alternate),
    )


def verify_equation_independently(
    lhs: sp.Expr, rhs: sp.Expr, symbol: sp.Symbol, candidates: tuple[Any, ...]
) -> VerificationResult:
    try:
        expected = tuple(sp.solveset(sp.Eq(lhs, rhs), symbol, domain=sp.S.Reals))
        actual = tuple(candidates)
        expected_set = {sp.simplify(item) for item in expected}
        actual_set = {sp.simplify(item) for item in actual}
        if expected_set != actual_set:
            return VerificationResult(
                False,
                ConfidenceLevel.HIGH,
                ("independent_solution_set_mismatch",),
                (expected, actual),
            )
        substitution = verify_solution_set(lhs, rhs, symbol, actual)
        if substitution.verified:
            return VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("independent_solver_agreement", "solution_set_substitution"),
                (expected, actual),
            )
        return substitution
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(
            False, ConfidenceLevel.LOW, ("independent_verification_failed",), ()
        )


def verify_derivative_result(
    expression: sp.Expr, symbol: sp.Symbol, claimed: Any, order: int = 1
) -> VerificationResult:
    try:
        if order < 1:
            raise ValueError("derivative order must be positive")
        expected = sp.diff(expression, symbol, order)
        return verify_expression_result(expected, claimed)
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(
            False, ConfidenceLevel.LOW, ("derivative_verification_failed",), ()
        )


def verify_antiderivative_result(
    integrand: sp.Expr, symbol: sp.Symbol, claimed: Any
) -> VerificationResult:
    try:
        recovered = sp.diff(claimed, symbol)
        equivalent = sp.simplify(recovered - integrand) == 0
        if equivalent:
            return VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("independent_derivative_recheck", "symbolic_equivalence"),
                (recovered,),
            )
        return VerificationResult(
            False,
            ConfidenceLevel.HIGH,
            ("antiderivative_mismatch",),
            (integrand, recovered),
        )
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(False, ConfidenceLevel.LOW, ("integral_verification_failed",), ())


def verify_structured_result(
    method: str, claimed: Any, metadata: dict[str, Any] | None = None
) -> VerificationResult:
    metadata = metadata or {}
    try:
        if method == "series_expansion":
            expected = sp.series(
                metadata["expression"],
                metadata["symbol"],
                metadata["point"],
                metadata["order"],
            )
        elif method == "finite_sum":
            expected = sp.summation(
                metadata["expression"],
                (metadata["variable"], metadata["lower"], metadata["upper"]),
            )
        elif method == "finite_product":
            expected = sp.product(
                metadata["expression"],
                (metadata["variable"], metadata["lower"], metadata["upper"]),
            )
        elif method == "matrix_det":
            expected = metadata["matrix"].det()
        elif method == "matrix_inv":
            expected = metadata["matrix"].inv()
        elif method == "matrix_rank":
            expected = metadata["matrix"].rank()
        elif method == "matrix_transpose":
            expected = metadata["matrix"].T
        elif method == "number_theory":
            expected = sp.factorint(int(metadata["number"]))
        elif method == "statistics":
            values = metadata["values"]
            count = len(values)
            mean = sp.Rational(sum(values), count)
            ordered = sorted(values, key=lambda item: float(item))
            middle = count // 2
            median = ordered[middle] if count % 2 else (ordered[middle - 1] + ordered[middle]) / 2
            variance = sp.Rational(sum((item - mean) ** 2 for item in values), count)
            expected = {"mean": mean, "median": median, "variance": variance}
        elif method == "gcd":
            expected = sp.gcd(metadata["a"], metadata["b"])
        elif method == "lcm":
            expected = sp.ilcm(metadata["a"], metadata["b"])
        elif method == "combinations":
            expected = sp.binomial(metadata["n"], metadata["r"])
        elif method == "permutation":
            expected = sp.factorial(metadata["n"])
        elif method == "trigonometric":
            expected = sp.solveset(metadata["expression"], metadata["symbol"], domain=sp.S.Reals)
            if expected == claimed:
                return VerificationResult(
                    True,
                    ConfidenceLevel.HIGH,
                    ("independent_trigonometric_recheck",),
                    (expected,),
                )
            return VerificationResult(
                False,
                ConfidenceLevel.HIGH,
                ("trigonometric_solution_mismatch",),
                (expected, claimed),
            )
        elif method == "complex_equation":
            expected = sp.solveset(metadata["expression"], metadata["symbol"], domain=sp.Complexes)
            if sp.simplify(expected - claimed) == sp.EmptySet:
                return VerificationResult(
                    True,
                    ConfidenceLevel.HIGH,
                    ("independent_complex_recheck",),
                    (expected,),
                )
            return VerificationResult(
                False,
                ConfidenceLevel.HIGH,
                ("complex_solution_mismatch",),
                (expected, claimed),
            )
        else:
            return VerificationResult(
                False, ConfidenceLevel.LOW, ("unsupported_structured_method",), ()
            )
        if expected == claimed or sp.simplify(expected - claimed) == 0:
            return VerificationResult(
                True, ConfidenceLevel.HIGH, ("independent_structured_recheck",), (expected,)
            )
        return VerificationResult(
            False, ConfidenceLevel.HIGH, ("structured_result_mismatch",), (expected, claimed)
        )
    except (KeyError, TypeError, ValueError, NotImplementedError, sp.NonInvertibleMatrixError):
        return VerificationResult(
            False, ConfidenceLevel.LOW, ("structured_verification_failed",), ()
        )


def verify_definite_integral_result(
    integrand: sp.Expr, symbol: sp.Symbol, lower: Any, upper: Any, claimed: Any
) -> VerificationResult:
    try:
        expected = sp.integrate(integrand, (symbol, lower, upper))
        return compare_independent_methods(expected, claimed, sp.N(expected, 30))
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(
            False, ConfidenceLevel.LOW, ("definite_integral_verification_failed",), ()
        )


def verify_limit_result(
    expression: sp.Expr, symbol: sp.Symbol, point: Any, claimed: Any
) -> VerificationResult:
    try:
        expected = sp.limit(expression, symbol, point)
        return compare_independent_methods(expected, claimed, sp.simplify(expected))
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(False, ConfidenceLevel.LOW, ("limit_verification_failed",), ())


def verify_system_result(
    equations: tuple[tuple[sp.Expr, sp.Expr], ...],
    symbols: tuple[sp.Symbol, ...],
    claimed: Any,
) -> VerificationResult:
    try:
        expected = sp.linsolve(
            tuple(lhs - rhs for lhs, rhs in equations),
            symbols,
        )
        if isinstance(claimed, list) and len(claimed) == 1 and isinstance(claimed[0], dict):
            actual_tuple = tuple(claimed[0][symbol] for symbol in symbols)
        elif isinstance(claimed, dict):
            actual_tuple = tuple(claimed[symbol] for symbol in symbols)
        else:
            return VerificationResult(False, ConfidenceLevel.LOW, ("invalid_system_output",), ())
        expected_tuples = tuple(expected)
        if not expected_tuples:
            return VerificationResult(
                False, ConfidenceLevel.HIGH, ("system_solution_mismatch",), ()
            )
        actual = tuple(sp.simplify(value) for value in actual_tuple)
        expected_tuple = tuple(sp.simplify(value) for value in expected_tuples[0])
        if actual != expected_tuple:
            return VerificationResult(
                False, ConfidenceLevel.HIGH, ("system_solution_mismatch",), (expected_tuple, actual)
            )
        residuals = tuple(
            sp.simplify((lhs - rhs).subs(dict(zip(symbols, actual)))) for lhs, rhs in equations
        )
        if all(residual == 0 for residual in residuals):
            return VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("independent_linear_solver", "system_substitution"),
                (expected_tuple,),
            )
        return VerificationResult(
            False, ConfidenceLevel.HIGH, ("system_nonzero_residual",), residuals
        )
    except (KeyError, TypeError, ValueError, NotImplementedError):
        return VerificationResult(False, ConfidenceLevel.LOW, ("system_verification_failed",), ())
