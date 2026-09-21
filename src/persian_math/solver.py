from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import sympy as sp

from .canonical import parse_equation, parse_expression, parse_inequality


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
    return SolverResult(
        False,
        None,
        method,
        "unable to solve the mathematical input",
        {"error_type": type(exc).__name__},
    )


def solve_expression(expression: sp.Expr) -> SolverResult:
    try:
        return _ok(sp.simplify(expression), "symbolic_simplification")
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_simplification", exc)


def solve_equation(lhs: sp.Expr, rhs: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        return _ok(
            tuple(sp.solve(sp.Eq(lhs, rhs), symbol, dict=False)),
            "symbolic_equation",
            symbol=str(symbol),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_equation", exc)


def solve_inequality(lhs: sp.Expr, operator: str, rhs: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        relation = {"<": sp.Lt, "<=": sp.Le, ">": sp.Gt, ">=": sp.Ge}[operator](lhs, rhs)
        return _ok(
            sp.solve_univariate_inequality(relation, symbol),
            "symbolic_inequality",
            symbol=str(symbol),
        )
    except (KeyError, TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_inequality", exc)


def solve_system(
    equations: tuple[tuple[sp.Expr, sp.Expr], ...], symbols: tuple[sp.Symbol, ...]
) -> SolverResult:
    try:
        eqs = [sp.Eq(lhs, rhs) for lhs, rhs in equations]
        return _ok(
            sp.solve(eqs, symbols, dict=True),
            "symbolic_system",
            symbols=tuple(map(str, symbols)),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_system", exc)


def solve_polynomial(expression: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        return _ok(
            tuple(sp.solve(sp.Poly(expression, symbol), symbol)),
            "polynomial",
            symbol=str(symbol),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("polynomial", exc)


def differentiate(expression: sp.Expr, symbol: sp.Symbol, order: int = 1) -> SolverResult:
    if order < 1:
        return _fail("derivative", ValueError("order must be positive"))
    try:
        return _ok(
            sp.diff(expression, symbol, order),
            "derivative",
            symbol=str(symbol),
            order=order,
        )
    except (TypeError, ValueError) as exc:
        return _fail("derivative", exc)


def integrate(
    expression: sp.Expr,
    symbol: sp.Symbol,
    lower: Any | None = None,
    upper: Any | None = None,
) -> SolverResult:
    try:
        value = (
            sp.integrate(expression, (symbol, lower, upper))
            if lower is not None and upper is not None
            else sp.integrate(expression, symbol)
        )
        return _ok(value, "integral", symbol=str(symbol), definite=lower is not None)
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("integral", exc)


def limit(
    expression: sp.Expr, symbol: sp.Symbol, point: Any, direction: str = "+-"
) -> SolverResult:
    try:
        return _ok(
            sp.limit(expression, symbol, point, dir=direction),
            "limit",
            symbol=str(symbol),
            point=str(point),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("limit", exc)


def solve_trigonometric(expression: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        return _ok(
            tuple(sp.solveset(expression, symbol, domain=sp.S.Reals)),
            "trigonometric",
            symbol=str(symbol),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("trigonometric", exc)


def solve_numeric(expression: sp.Expr, symbol: sp.Symbol, guess: float = 0.0) -> SolverResult:
    try:
        return _ok(sp.nsolve(expression, symbol, guess), "numerical_root", symbol=str(symbol))
    except (TypeError, ValueError, sp.SympifyError) as exc:
        return _fail("numerical_root", exc)


def solve_complex(expression: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        return _ok(
            tuple(sp.solveset(expression, symbol, domain=sp.S.Complexes)),
            "complex_solution",
            symbol=str(symbol),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("complex_solution", exc)


def solve_number_theory(expression: sp.Expr) -> SolverResult:
    try:
        value = sp.factorint(int(expression))
        return _ok(value, "integer_factorization")
    except (TypeError, ValueError, sp.SympifyError) as exc:
        return _fail("integer_factorization", exc)


def optimize(expression: sp.Expr, symbol: sp.Symbol) -> SolverResult:
    try:
        derivative = sp.diff(expression, symbol)
        critical = tuple(sp.solve(derivative, symbol))
        return _ok(
            {
                "critical_points": critical,
                "second_derivative": sp.diff(expression, symbol, 2),
            },
            "symbolic_optimization",
            symbol=str(symbol),
        )
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("symbolic_optimization", exc)


def solve_ode(expression: sp.Eq, function: sp.FunctionClass) -> SolverResult:
    try:
        return _ok(sp.dsolve(expression, function), "differential_equation")
    except (TypeError, ValueError, NotImplementedError) as exc:
        return _fail("differential_equation", exc)


def solve_statistics(values: list[Any]) -> SolverResult:
    try:
        data = [sp.sympify(value) for value in values]
        if not data:
            raise ValueError("empty dataset")
        ordered = sorted(data, key=lambda item: float(item))
        middle = len(ordered) // 2
        median = (
            ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2
        )
        mean = sp.Rational(sum(data), len(data))
        variance = sp.Rational(sum((item - mean) ** 2 for item in data), len(data))
        return _ok({"mean": mean, "median": median, "variance": variance}, "statistics")
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        return _fail("statistics", exc)


def solve_probability(successes: int, trials: int) -> SolverResult:
    if trials <= 0 or successes < 0 or successes > trials:
        return _fail("probability", ValueError("invalid probability counts"))
    return _ok(sp.Rational(successes, trials), "empirical_probability")


def solve_matrix(matrix: sp.MatrixBase, operation: str) -> SolverResult:
    try:
        operations = {
            "det": matrix.det,
            "inv": matrix.inv,
            "rank": matrix.rank,
            "transpose": lambda: matrix.T,
        }
        if operation not in operations:
            raise ValueError("unsupported matrix operation")
        return _ok(operations[operation](), f"matrix_{operation}")
    except (TypeError, ValueError, sp.NonInvertibleMatrixError) as exc:
        return _fail("matrix", exc)



def solve_word_problem(text: str) -> tuple[SolverResult, sp.Expr | None, str | None]:
    normalized = text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")).translate(
        str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    )
    rectangle = re.search(
        r"مساحت.*?مستطیل.*?طول\s*([0-9]+(?:\.\d+)?)\s*(?:سانتی.?متر|متر)?.*?"
        r"عرض\s*([0-9]+(?:\.\d+)?)",
        normalized,
        re.DOTALL,
    )
    if rectangle:
        length, width = map(sp.Rational, rectangle.groups())
        expression = length * width
        return _ok(expression, "geometry_rectangle_area", length=length, width=width), expression, "rectangle_area"
    function = re.search(
        r"f\s*\(\s*x\s*\)\s*=\s*([^،,.\n]+?).*?f\s*\(\s*([-+]?\d+(?:\.\d+)?)\s*\)",
        normalized,
        re.DOTALL,
    )
    if function:
        definition, point_text = function.groups()
        point = sp.Rational(point_text)
        try:
            parsed = parse_expression(definition).expression
            value = sp.simplify(parsed.subs(sp.Symbol("x"), point))
            return _ok(value, "function_evaluation", point=point), value, "function_evaluation"
        except (TypeError, ValueError):
            pass
    arithmetic = re.search(
        r"مجموع\s+(\d+)\s+جمله.*?دنباله\s+حسابی.*?([0-9]+(?:\.\d+)?)\s*,\s*"
        r"([0-9]+(?:\.\d+)?)\s*,\s*([0-9]+(?:\.\d+)?)",
        normalized,
        re.DOTALL,
    )
    if arithmetic:
        n, a1, a2, _a3 = map(sp.Rational, arithmetic.groups())
        d = a2 - a1
        expression = sp.simplify(n * (2 * a1 + (n - 1) * d) / 2)
        return _ok(expression, "arithmetic_sequence_sum", n=n, first=a1, difference=d), expression, "arithmetic_sequence"
    return SolverResult(False, None, "word_problem_router", "no supported structured word problem"), None, None

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
            SolverRoute(
                "inequality",
                lambda t: any(op in t for op in ("<", ">", "≤", "≥")),
                solve,
            ),
            SolverRoute("equation", lambda t: t.count("=") == 1, solve),
            SolverRoute("expression", lambda t: True, solve),
        )

    def route(self, text: str) -> SolverResult:
        for route in self._routes:
            if route.predicate(text):
                return route.handler(text)
        return _fail("router", ValueError("no route"))
