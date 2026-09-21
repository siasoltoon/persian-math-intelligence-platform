from __future__ import annotations

from decimal import Decimal

from .canonical import extract_math_payload, normalize_math_text
from .domain import ProblemClassification, ProblemInput, ProblemRepresentation

_DOMAIN_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("calculus", ("مشتق", "انتگرال", "حد", "derivative", "integral", "limit")),
    ("geometry", ("هندسه", "مثلث", "دایره", "زاویه", "geometry", "triangle")),
    ("probability", ("احتمال", "probability")),
    ("statistics", ("آمار", "میانگین", "واریانس", "statistics")),
    ("algebra", ("معادله", "نامعادله", "جبر", "equation", "inequality", "polynomial")),
    ("linear_algebra", ("ماتریس", "بردار", "matrix", "vector")),
    ("number_theory", ("اعداد اول", "باقی‌مانده", "prime", "modulo")),
    ("discrete_math", ("گراف", "ترکیبیات", "منطق", "combinatorics", "graph theory")),
)


def classify_problem(problem: ProblemInput) -> ProblemClassification:
    text = normalize_math_text(problem.text).lower()
    for domain, patterns in _DOMAIN_PATTERNS:
        if any(pattern in text for pattern in patterns):
            intent = "solve" if "=" in text or any(ch.isdigit() for ch in text) else "explain"
            return ProblemClassification(intent, domain, Decimal("0.90"))
    intent = "solve" if any(ch.isdigit() for ch in text) else "explain"
    return ProblemClassification(intent, "general_math", Decimal("0.55"))


def represent_problem(problem: ProblemInput) -> ProblemRepresentation:
    text = extract_math_payload(problem.text)
    if any(op in text for op in ("<", ">", "<=", ">=")):
        kind = "inequality"
    elif text.count("=") == 1:
        kind = "equation"
    else:
        kind = "expression"
    return ProblemRepresentation(kind, text, problem.text)
