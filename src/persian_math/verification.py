from __future__ import annotations

import math
from typing import Any

import sympy as sp

from .domain import ConfidenceLevel, VerificationResult


def _numeric_equal(a: Any, b: Any, tolerance: float = 1e-9) -> bool:
    try:
        return math.isclose(float(sp.N(a)), float(sp.N(b)), rel_tol=tolerance, abs_tol=tolerance)
    except (TypeError, ValueError):
        return False


def verify_expression_result(expression: sp.Expr, claimed: Any) -> VerificationResult:
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
    return VerificationResult(False, ConfidenceLevel.HIGH, ("symbolic_mismatch",), (expected, claimed))


def verify_equation_solution(
    lhs: sp.Expr, rhs: sp.Expr, symbol: sp.Symbol, candidate: Any
) -> VerificationResult:
    try:
        residual = sp.simplify(lhs.subs(symbol, candidate) - rhs.subs(symbol, candidate))
    except (TypeError, ValueError):
        return VerificationResult(False, ConfidenceLevel.HIGH, ("substitution_failed",), ())
    if residual == 0:
        return VerificationResult(
            True, ConfidenceLevel.HIGH, ("direct_substitution", "zero_residual"), (candidate,)
        )
    return VerificationResult(False, ConfidenceLevel.HIGH, ("nonzero_residual",), (candidate,))
