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
            source_expression=str(expression),
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
        return _ok(
            value,
            "definite_integral" if lower is not None and upper is not None else "integral",
            symbol=str(symbol),
            definite=lower is not None,
            lower=lower,
            upper=upper,
            source_expression=str(expression),
        )
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
            direction=direction,
            source_expression=str(expression),
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
            source_expression=str(expression),
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


def _normalize_problem_digits(text: str) -> str:
    value = text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")).translate(
        str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    )
    subscript = "₀₁₂₃₄₅₆₇₈₉"
    superscript = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    sub_map = str.maketrans(subscript, "0123456789")
    super_map = str.maketrans(superscript, "0123456789")
    value = re.sub(
        r"∫\s*([₀₁₂₃₄₅₆₇₈₉0-9]+)\s*([⁰¹²³⁴⁵⁶⁷⁸⁹0-9]+)",
        lambda match: (
            "∫" + match.group(1).translate(sub_map) + " " + match.group(2).translate(super_map)
        ),
        value,
    )
    return value


def _function_definition(text: str) -> tuple[sp.Expr, sp.Symbol] | None:
    match = re.search(r"f\s*\(\s*x\s*\)\s*=\s*([^،\n]+)", text)
    if not match:
        return None
    expression = parse_expression(match.group(1).strip()).expression
    return expression, sp.Symbol("x")


def _solve_function_analysis(expression: sp.Expr, symbol: sp.Symbol) -> dict[str, Any]:
    first = sp.simplify(sp.diff(expression, symbol))
    second = sp.simplify(sp.diff(expression, symbol, 2))
    critical = tuple(sp.solve(first, symbol))
    critical_points = []
    for point in critical:
        second_value = sp.simplify(second.subs(symbol, point))
        classification = (
            "max" if second_value < 0 else "min" if second_value > 0 else "inconclusive"
        )
        critical_points.append((point, sp.simplify(expression.subs(symbol, point)), classification))
    increasing = sp.solve_univariate_inequality(first > 0, symbol)
    decreasing = sp.solve_univariate_inequality(first < 0, symbol)
    inflection_x = tuple(sp.solve(second, symbol))
    inflection_points = tuple(
        (point, sp.simplify(expression.subs(symbol, point))) for point in inflection_x
    )
    return {
        "critical_points": tuple(critical_points),
        "increasing": increasing,
        "decreasing": decreasing,
        "inflection_points": inflection_points,
    }


def solve_word_problem(
    text: str,
) -> tuple[SolverResult, Any | None, str | None]:
    normalized = _normalize_problem_digits(text)

    rectangle = re.search(
        r"مساحت.*?مستطیل.*?طول\s*([0-9]+(?:\.\d+)?)\s*(?:سانتی.?متر|متر)?.*?"
        r"عرض\s*([0-9]+(?:\.\d+)?)",
        normalized,
        re.DOTALL,
    )
    if rectangle:
        length, width = map(sp.Rational, rectangle.groups())
        expression = length * width
        return (
            _ok(expression, "geometry_rectangle_area", length=length, width=width),
            expression,
            "expression",
        )

    function = re.search(
        r"f\s*\(\s*x\s*\)\s*=\s*([^،\n]+?)\s*باشد.*?"
        r"f\s*\(\s*([-+]?\d+(?:\.\d+)?)\s*\)",
        normalized,
        re.DOTALL,
    )
    if function:
        definition, point_text = function.groups()
        point = sp.Rational(point_text)
        try:
            parsed = parse_expression(definition).expression
            value = sp.simplify(parsed.subs(sp.Symbol("x"), point))
            return _ok(value, "function_evaluation", point=point), value, "expression"
        except (TypeError, ValueError):
            pass

    if any(
        token in normalized
        for token in (
            "نقاط بحرانی",
            "ماکزیمم",
            "مینیمم",
            "بازه‌های صعود",
            "بازه های صعود",
            "نقاط عطف",
        )
    ):
        try:
            definition = _function_definition(normalized)
            if definition:
                expression, symbol = definition
                value = _solve_function_analysis(expression, symbol)
                return (
                    _ok(
                        value,
                        "function_analysis",
                        source_expression=str(expression),
                        symbol=str(symbol),
                    ),
                    None,
                    "function_analysis",
                )
        except (TypeError, ValueError, NotImplementedError):
            pass

    derivative_match = re.search(
        r"(?:مشتق).*?f\s*\(\s*x\s*\)\s*=\s*([^،\n]+?)(?:\s*باشد|\s*$)",
        normalized,
        re.DOTALL,
    )
    if derivative_match:
        try:
            expression = parse_expression(derivative_match.group(1).strip()).expression
            symbol = sp.Symbol("x")
            result = differentiate(expression, symbol)
            if result.success:
                return result, result.value, "expression"
        except (TypeError, ValueError):
            pass

    definite_integral = re.search(
        r"∫\s*([0-9]+(?:\.\d+)?)\s*([0-9]+(?:\.\d+)?)\s*(.*?)\s*d\s*x",
        normalized,
        re.DOTALL,
    )
    if definite_integral:
        lower_text, upper_text, integrand_text = definite_integral.groups()
        try:
            lower = sp.Rational(lower_text)
            upper = sp.Rational(upper_text)
            expression = parse_expression(integrand_text.strip()).expression
            result = integrate(expression, sp.Symbol("x"), lower, upper)
            if result.success:
                return result, result.value, "expression"
        except (TypeError, ValueError):
            pass

    textual_definite = re.search(
        r"انتگرال.*?از\s*([0-9]+(?:\.\d+)?)\s*تا\s*([0-9]+(?:\.\d+)?).*?:?\s*(.*?)\s*d\s*x",
        normalized,
        re.DOTALL,
    )
    if textual_definite:
        lower_text, upper_text, integrand_text = textual_definite.groups()
        try:
            lower = sp.Rational(lower_text)
            upper = sp.Rational(upper_text)
            expression = parse_expression(integrand_text.strip()).expression
            result = integrate(expression, sp.Symbol("x"), lower, upper)
            if result.success:
                return result, result.value, "expression"
        except (TypeError, ValueError):
            pass

    indefinite_integral = re.search(
        r"∫\s*(.*?)\s*d\s*x",
        normalized,
        re.DOTALL,
    )
    if indefinite_integral:
        try:
            integrand = indefinite_integral.group(1).strip()
            expression = parse_expression(integrand).expression
            result = integrate(expression, sp.Symbol("x"))
            if result.success:
                return result, result.value, "expression"
        except (TypeError, ValueError):
            pass

    limit_match = re.search(
        r"lim\s*\(\s*x\s*(?:→|->)\s*([-+]?\d+(?:\.\d+)?)\s*\)\s*(.+)$",
        normalized,
        re.DOTALL,
    )
    if limit_match:
        point_text, expression_text = limit_match.groups()
        try:
            point = sp.Rational(point_text)
            expression_text = expression_text.replace("[", "(").replace("]", ")")
            expression = parse_expression(expression_text.strip()).expression
            result = limit(expression, sp.Symbol("x"), point)
            if result.success:
                return result, result.value, "expression"
        except (IndexError, TypeError, ValueError, NotImplementedError):
            pass

    system_lines = []
    for line in normalized.splitlines():
        if line.count("=") == 1 and any(ch.isalpha() for ch in line):
            system_lines.append(line.strip())
    if len(system_lines) >= 2 and ("دستگاه" in normalized or "معادلات" in normalized):
        try:
            equations = tuple(parse_equation(line) for line in system_lines)
            symbols = tuple(
                sorted(
                    set().union(*(lhs.free_symbols | rhs.free_symbols for lhs, rhs in equations)),
                    key=str,
                )
            )
            if len(symbols) >= 2:
                result = solve_system(equations, symbols)
                if result.success:
                    return (
                        SolverResult(
                            True,
                            result.value,
                            result.method,
                            metadata={
                                **(result.metadata or {}),
                                "equations": equations,
                                "symbols": symbols,
                            },
                        ),
                        None,
                        "system",
                    )
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
        return (
            _ok(expression, "arithmetic_sequence_sum", n=n, first=a1, difference=d),
            expression,
            "expression",
        )

    return (
        SolverResult(False, None, "word_problem_router", "no supported structured word problem"),
        None,
        None,
    )


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
