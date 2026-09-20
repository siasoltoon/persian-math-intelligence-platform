from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class SolverResult:
    success: bool
    value: Any | None
    method: str
    message: str = ""


def solve_expression(expression: sp.Expr) -> SolverResult:
    try:
        return SolverResult(True, sp.simplify(expression), "symbolic")
    except (TypeError, ValueError) as exc:
        return SolverResult(False, None, "symbolic", str(exc))


def solve_equation(lhs: sp.Expr, rhs: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        values = sp.solve(sp.Eq(lhs, rhs), symbol, dict=False)
        return SolverResult(True, tuple(values), "symbolic_equation")
    except (TypeError, ValueError, NotImplementedError) as exc:
        return SolverResult(False, None, "symbolic_equation", str(exc))


def solve(expression_text: str, *, symbol_name: str = "x") -> SolverResult:
    from .canonical import parse_equation, parse_expression

    if "=" in expression_text:
        lhs, rhs = parse_equation(expression_text)
        return solve_equation(lhs, rhs, sp.Symbol(symbol_name))
    return solve_expression(parse_expression(expression_text).expression)
