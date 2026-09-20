from __future__ import annotations

import re
from dataclasses import dataclass

import sympy as sp


PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def normalize_math_text(text: str) -> str:
    value = text.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)
    value = value.replace("×", "*").replace("÷", "/").replace("−", "-")
    value = value.replace("٫", ".").replace("،", ",")
    value = re.sub(r"\s+", " ", value).strip()
    return value


@dataclass(frozen=True)
class CanonicalExpression:
    original: str
    normalized: str
    expression: sp.Expr


def parse_expression(text: str) -> CanonicalExpression:
    normalized = normalize_math_text(text)
    if not normalized:
        raise ValueError("empty mathematical expression")
    try:
        expr = sp.sympify(normalized, locals={"pi": sp.pi, "e": sp.E, "sqrt": sp.sqrt})
    except (sp.SympifyError, SyntaxError) as exc:
        raise ValueError("invalid mathematical expression") from exc
    return CanonicalExpression(text, normalized, expr)


def parse_equation(text: str) -> tuple[sp.Expr, sp.Expr]:
    normalized = normalize_math_text(text)
    parts = normalized.split("=")
    if len(parts) != 2 or not all(part.strip() for part in parts):
        raise ValueError("an equation must contain exactly one '='")
    try:
        return sp.sympify(parts[0]), sp.sympify(parts[1])
    except (sp.SympifyError, SyntaxError) as exc:
        raise ValueError("invalid equation") from exc
