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
_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)
_LOCALS = {"pi": sp.pi, "e": sp.E, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
           "log": sp.log, "ln": sp.log, "exp": sp.exp, "abs": sp.Abs}
_SAFE_GLOBALS = {
    "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational, "Symbol": sp.Symbol,
    "Add": sp.Add, "Mul": sp.Mul, "Pow": sp.Pow, "Function": sp.Function,
    "pi": sp.pi, "E": sp.E,
}

@dataclass(frozen=True)
class CanonicalExpression:
    original: str
    normalized: str
    expression: sp.Expr

def normalize_math_text(text: str) -> str:
    value = text.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)
    replacements = {"×": "*", "÷": "/", "−": "-", "–": "-", "—": "-", "√": "sqrt",
                    "π": "pi", "∞": "oo", "∑": "sum", "∫": "integral", "≤": "<=", "≥": ">="}
    for source, target in replacements.items():
        value = value.replace(source, target)
    value = value.replace("٫", ".").replace("،", ",")
    return re.sub(r"\s+", " ", value).strip()

def _parse(text: str) -> sp.Expr:
    try:
        return parse_expr(text, local_dict=_LOCALS, global_dict=_SAFE_GLOBALS,
                          transformations=_TRANSFORMATIONS, evaluate=True)
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
    return _parse(normalized[:match.start()]), match.group(), _parse(normalized[match.end():])

def parse_system(text: str) -> tuple[tuple[sp.Expr, sp.Expr], ...]:
    equations = tuple(line.strip() for line in re.split(r"[\n;]+", normalize_math_text(text)) if line.strip())
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
