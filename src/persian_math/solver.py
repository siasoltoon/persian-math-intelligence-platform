from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import sympy as sp

from .canonical import parse_equation, parse_expression, parse_inequality, parse_matrix, parse_system

@dataclass(frozen=True)
class SolverResult:
    success: bool
    value: Any | None
    method: str
    message: str = ""
    metadata: dict[str, Any] | None = None

def _ok(value: Any, method: str, **metadata: Any) -> SolverResult:
    return SolverResult(True, value, method, metadata=metadata or None)

def _fail(method: str, exc: Exception) -> SolverResult:
    return SolverResult(False, None, method, "unable to solve the mathematical input", {"error_type": type(exc).__name__})

def solve_expression(expression: sp.Expr) -> SolverResult:
    try:
        return _ok(sp.simplify(expression), "symbolic_simplification")
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_simplification", exc)

def solve_equation(lhs: sp.Expr, rhs: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        values = sp.solve(sp.Eq(lhs, rhs), symbol, dict=False)
        return _ok(tuple(values), "symbolic_equation", symbol=str(symbol))
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_equation", exc)

def solve_inequality(lhs: sp.Expr, operator: str, rhs: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        relation = {"<": sp.Lt, "<=": sp.Le, ">": sp.Gt, ">=": sp.Ge}[operator](lhs, rhs)
        return _ok(sp.solve_univariate_inequality(relation, symbol), "symbolic_inequality", symbol=str(symbol))
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_inequality", exc)

def solve_system(equations: tuple[tuple[sp.Expr, sp.Expr], ...], symbols: tuple[sp.Symbol, ...]) -> SolverResult:
    try:
        eqs = [sp.Eq(lhs, rhs) for lhs, rhs in equations]
        return _ok(sp.solve(eqs, symbols, dict=True), "symbolic_system", symbols=tuple(map(str, symbols)))
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_system", exc)

def solve_polynomial(expression: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        return _ok(tuple(sp.solve(sp.Poly(expression, symbol), symbol)), "polynomial", symbol=str(symbol))
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("polynomial", exc)

def differentiate(expression: sp.Expr, symbol: sp.Symbol, order: int = 1) -> SolverResult:
    try:
        return _ok(sp.diff(expression, symbol, order), "derivative", symbol=str(symbol), order=order)
    except (TypeError, ValueError) as exc:
        return _fail("derivative", exc)

def integrate(expression: sp.Expr, symbol: sp.Symbol, lower: Any | None = None, upper: Any | None = None) -> SolverResult:
    try:
        value = sp.integrate(expression, (symbol, lower, upper)) if lower is not None and upper is not None else sp.integrate(expression, symbol)
        return _ok(value, "integral", symbol=str(symbol), definite=lower is not None)
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("integral", exc)

def limit(expression: sp.Expr, symbol: sp.Symbol, point: Any, direction: str = "+-") -> SolverResult:
    try:
        return _ok(sp.limit(expression, symbol, point, dir=direction), "limit", symbol=str(symbol), point=str(point))
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("limit", exc)

def solve_matrix(matrix: sp.MatrixBase, operation: str) -> SolverResult:
    try:
        if operation == "det": return _ok(matrix.det(), "matrix_determinant")
        if operation == "inv": return _ok(matrix.inv(), "matrix_inverse")
        if operation == "rank": return _ok(matrix.rank(), "matrix_rank")
        if operation == "transpose": return _ok(matrix.T, "matrix_transpose")
        raise ValueError("unsupported matrix operation")
    except (TypeError, ValueError, sp.NonInvertibleMatrixError) as exc:
        return _fail("matrix", exc)

def solve(expression_text: str, *, symbol_name: str = "x") -> SolverResult:
    text = expression_text.strip()
    symbol = sp.Symbol(symbol_name)
    try:
        if any(op in text for op in ("<", ">", "≤", "≥")):
            lhs, op, rhs = parse_inequality(text)
            return solve_inequality(lhs, op, rhs, symbol)
        if text.count("=") == 1:
            lhs, rhs = parse_equation(text)
            return solve_equation(lhs, rhs, symbol)
        return solve_expression(parse_expression(text).expression)
    except (TypeError, ValueError) as exc:
        return _fail("router", exc)

@dataclass(frozen=True)
class SolverRoute:
    name: str
    predicate: Callable[[str], bool]
    handler: Callable[[str], SolverResult]

class SolverRouter:
    def __init__(self) -> None:
        self._routes: tuple[SolverRoute, ...] = (
            SolverRoute("inequality", lambda t: any(op in t for op in ("<", ">", "≤", "≥")),
                        lambda t: solve(t)),
            SolverRoute("equation", lambda t: t.count("=") == 1, lambda t: solve(t)),
            SolverRoute("expression", lambda t: True, lambda t: solve(t)),
        )

    def route(self, text: str) -> SolverResult:
        for route in self._routes:
            if route.predicate(text):
                return route.handler(text)
        return _fail("router", ValueError("no route"))
