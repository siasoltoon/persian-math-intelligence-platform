from __future__ import annotations

import re
from dataclasses import dataclass

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
SUPERSCRIPT_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)
_LOCALS = {
    "pi": sp.pi,
    "e": sp.E,
    "sqrt": sp.sqrt,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "log": sp.log,
    "ln": sp.log,
    "exp": sp.exp,
    "abs": sp.Abs,
}
_SAFE_GLOBALS = {
    "__builtins__": {},
    "Integer": sp.Integer,
    "Float": sp.Float,
    "Rational": sp.Rational,
    "Symbol": sp.Symbol,
    "Add": sp.Add,
    "Mul": sp.Mul,
    "Pow": sp.Pow,
    "Function": sp.Function,
    "pi": sp.pi,
    "E": sp.E,
}
_MAX_MATH_INPUT_CHARS = 10_000
_ALLOWED_MATH_CHARS = re.compile(r"^[A-Za-z0-9_+\-*/^().,\[\]{}<>=|:;\s]*$")


@dataclass(frozen=True)
class CanonicalExpression:
    original: str
    normalized: str
    expression: sp.Expr


def normalize_math_text(text: str) -> str:
    if len(text) > _MAX_MATH_INPUT_CHARS:
        raise ValueError("mathematical input is too long")
    value = text.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)
    value = re.sub(
        r"([A-Za-z0-9_)]+)([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)",
        lambda match: match.group(1) + "**" + match.group(2).translate(SUPERSCRIPT_DIGITS),
        value,
    )
    replacements = {
        "×": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "—": "-",
        "√": "sqrt",
        "π": "pi",
        "∞": "oo",
        "∑": "sum",
        "∫": "integral",
        "≤": "<=",
        "≥": ">=",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    value = value.replace("٫", ".").replace("،", ",")
    value = re.sub(r"[^\S\n]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    return value.strip()


_MATH_CANDIDATE_RE = re.compile(
    r"[A-Za-z0-9_+\\-*/^().,\\[\\]{}<>=|:;\\s×÷−–—√π⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+"
)


def extract_math_payload(text: str) -> str:
    """Extract a bounded mathematical fragment from a natural-language wrapper.

    This is deliberately lexical rather than semantic: only characters already
    accepted by the safe math parser may be promoted to a solver input.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("empty mathematical input")
    normalized_source = text.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)
    candidates: list[str] = []
    for match in _MATH_CANDIDATE_RE.finditer(normalized_source):
        candidate = match.group(0).strip().strip(",:;")
        if not candidate:
            continue
        if not (any(ch.isdigit() for ch in candidate) or any(op in candidate for op in "=<>+-*/^√")):
            continue
        try:
            normalized = normalize_math_text(candidate)
            _validate_parse_source(normalized)
        except ValueError:
            continue
        candidates.append(normalized)
    if not candidates:
        raise ValueError("no mathematical expression found")
    equations = [item for item in candidates if item.count("=") == 1]
    return max(equations or candidates, key=len)


def _validate_parse_source(text: str) -> None:
    if not text:
        raise ValueError("empty mathematical expression")
    if len(text) > _MAX_MATH_INPUT_CHARS:
        raise ValueError("mathematical input is too long")
    if not _ALLOWED_MATH_CHARS.fullmatch(text):
        raise ValueError("unsupported mathematical characters")
    if "__" in text or "lambda" in text.lower():
        raise ValueError("unsafe mathematical expression")


def _parse(text: str) -> sp.Expr:
    _validate_parse_source(text)
    try:
        return parse_expr(
            text,
            local_dict=_LOCALS,
            global_dict=_SAFE_GLOBALS,
            transformations=_TRANSFORMATIONS,
            evaluate=True,
        )
    except (sp.SympifyError, SyntaxError, TypeError, ValueError) as exc:
        raise ValueError("invalid mathematical expression") from exc


def parse_expression(text: str) -> CanonicalExpression:
    normalized = normalize_math_text(text)
    if not normalized:
        raise ValueError("empty mathematical expression")
    return CanonicalExpression(text, normalized, _parse(normalized))


def parse_equation(text: str) -> tuple[sp.Expr, sp.Expr]:
    normalized = normalize_math_text(text)
    parts = normalized.split("=")
    if len(parts) != 2 or not all(part.strip() for part in parts):
        raise ValueError("an equation must contain exactly one '='")
    return _parse(parts[0]), _parse(parts[1])


def parse_inequality(text: str) -> tuple[sp.Expr, str, sp.Expr]:
    normalized = normalize_math_text(text)
    matches = list(re.finditer(r"(<=|>=|<|>)", normalized))
    if len(matches) != 1:
        raise ValueError("an inequality must contain exactly one comparison operator")
    match = matches[0]
    return _parse(normalized[: match.start()]), match.group(), _parse(normalized[match.end() :])


def parse_system(text: str) -> tuple[tuple[sp.Expr, sp.Expr], ...]:
    equations = tuple(
        line.strip() for line in re.split(r"[\n;]+", normalize_math_text(text)) if line.strip()
    )
    if not equations or any(line.count("=") != 1 for line in equations):
        raise ValueError("a system must contain one equation per line")
    return tuple(parse_equation(line) for line in equations)


def parse_matrix(text: str) -> sp.MatrixBase:
    normalized = normalize_math_text(text).strip()
    if not (normalized.startswith("[") and normalized.endswith("]")):
        raise ValueError("matrix must use bracket notation")
    rows = normalized[1:-1].replace("], [", "];[").split(";")
    try:
        return sp.Matrix([[_parse(item) for item in row.strip(" []").split(",")] for row in rows])
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid matrix") from exc


def parse_fraction(text: str) -> sp.Expr:
    normalized = normalize_math_text(text)
    parts = normalized.split("/")
    if len(parts) != 2:
        raise ValueError("fraction must contain exactly one '/'")
    return sp.cancel(_parse(parts[0]) / _parse(parts[1]))


def parse_function(text: str) -> sp.Expr:
    return parse_expression(text).expression


def parse_vector(text: str) -> tuple[sp.Expr, ...]:
    normalized = normalize_math_text(text).strip()
    if not (normalized.startswith("[") and normalized.endswith("]")):
        raise ValueError("vector must use bracket notation")
    items = [item.strip() for item in normalized[1:-1].split(",")]
    if not items or any(not item for item in items):
        raise ValueError("invalid vector")
    return tuple(_parse(item) for item in items)


def parse_derivative(text: str, symbol: str = "x") -> sp.Expr:
    return sp.diff(parse_expression(text).expression, sp.Symbol(symbol))


def parse_integral(text: str, symbol: str = "x") -> sp.Expr:
    return sp.integrate(parse_expression(text).expression, sp.Symbol(symbol))


def parse_limit(text: str, symbol: str = "x", point: object = 0) -> sp.Expr:
    return sp.limit(parse_expression(text).expression, sp.Symbol(symbol), point)


def parse_series(text: str, symbol: str = "x", point: object = 0, order: int = 6) -> sp.Expr:
    if order < 1:
        raise ValueError("series order must be positive")
    return sp.series(parse_expression(text).expression, sp.Symbol(symbol), point, order)


def parse_probability(successes: int, trials: int) -> sp.Rational:
    if trials <= 0 or successes < 0 or successes > trials:
        raise ValueError("invalid probability counts")
    return sp.Rational(successes, trials)
