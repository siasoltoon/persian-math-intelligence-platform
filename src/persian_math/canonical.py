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
_LOCALS = {"pi": sp.pi, "e": sp.E, "sqrt": sp.sqrt}
_SAFE_GLOBALS = {
    "Integer": sp.Integer,
    "Float": sp.Float,
    "Rational": sp.Rational,
    "Symbol": sp.Symbol,
    "Add": sp.Add,
    "Mul": sp.Mul,
    "Pow": sp.Pow,
    "pi": sp.pi,
    "E": sp.E,
}


def normalize_math_text(text: str) -> str:
    value = text.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)
    value = value.replace("×", "*").replace("÷", "/").replace("−", "-")
    value = value.replace("٫", ".").replace("،", ",")
    return re.sub(r"\s+", " ", value).strip()


@dataclass(frozen=True)
class CanonicalExpression:
    original: str
    normalized: str
    expression: sp.Expr


def _parse(text: str) -> sp.Expr:
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
