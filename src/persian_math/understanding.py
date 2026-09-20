from __future__ import annotations

from .canonical import normalize_math_text
from .domain import ProblemClassification, ProblemInput, ProblemRepresentation


_DOMAIN_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("calculus", ("مشتق", "انتگرال", "حد", "derivative", "integral", "limit")),
    ("geometry", ("هندسه", "مثلث", "دایره", "زاویه", "geometry", "triangle")),
    ("probability", ("احتمال", "probability")),
    ("statistics", ("آمار", "میانگین", "واریانس", "statistics")),
    ("algebra", ("معادله", "نامعادله", "جبر", "equation", "inequality")),
)


def classify_problem(problem: ProblemInput) -> ProblemClassification:
    text = normalize_math_text(problem.text).lower()
    for domain, patterns in _DOMAIN_PATTERNS:
        if any(pattern in text for pattern in patterns):
            intent = "solve" if "=" in text or any(ch.isdigit() for ch in text) else "explain"
            return ProblemClassification(intent, domain, 0.90)
    intent = "solve" if any(ch.isdigit() for ch in text) else "explain"
    return ProblemClassification(intent, "general_math", 0.55)


def represent_problem(problem: ProblemInput) -> ProblemRepresentation:
    text = normalize_math_text(problem.text)
    kind = "equation" if text.count("=") == 1 else "expression"
    return ProblemRepresentation(kind, text, problem.text)
