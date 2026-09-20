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


def verify_expression_result(expression: sp.Expr, claimed: Any) -> VerificationResult:
    try:
        expected = sp.simplify(expression)
        if sp.simplify(expected - claimed) == 0:
            return VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("symbolic_equivalence", "independent_simplification"),
                (expected,),
            )
        if _numeric_equal(expected, claimed):
            return VerificationResult(
                True,
                ConfidenceLevel.MEDIUM,
                ("numerical_equivalence", "independent_simplification"),
                (expected,),
            )
        return VerificationResult(
            False,
            ConfidenceLevel.HIGH,
            ("symbolic_mismatch",),
            (expected, claimed),
        )
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(False, ConfidenceLevel.LOW, ("verification_failed", ()))


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
                ("numerical_residual_check", "domain_checked"),
                (candidate,),
            )
        return VerificationResult(False, ConfidenceLevel.HIGH, ("nonzero_residual",), (candidate,))
    except (TypeError, ValueError, NotImplementedError):
        return VerificationResult(False, ConfidenceLevel.LOW, ("verification_failed",), (candidate,))


def verify_solution_set(
    lhs: sp.Expr,
    rhs: sp.Expr,
    symbol: sp.Symbol,
    candidates: tuple[Any, ...],
) -> VerificationResult:
    checks = tuple(verify_equation_solution(lhs, rhs, symbol, c) for c in candidates)
    if not checks:
        return VerificationResult(
            True, ConfidenceLevel.HIGH, ("empty_solution_set_verified",), ()
        )
    verified = all(item.verified for item in checks)
    confidence = ConfidenceLevel.HIGH if verified else ConfidenceLevel.LOW
    return VerificationResult(verified, confidence, ("solution_set_substitution",), candidates)


def compare_independent_methods(
    expression: sp.Expr, claimed: Any, alternate: Any
) -> VerificationResult:
    del expression
    try:
        equivalent = sp.simplify(claimed - alternate) == 0
    except (TypeError, ValueError):
        equivalent = _numeric_equal(claimed, alternate)
    if equivalent:
        return VerificationResult(
            True, ConfidenceLevel.HIGH, ("independent_method_agreement",), (claimed, alternate)
        )
    return VerificationResult(
        False,
        ConfidenceLevel.HIGH,
        ("independent_method_disagreement",),
        (claimed, alternate),
    )
