from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

from .canonical import normalize_math_text
from .domain import ProblemClassification, ProblemInput, ProblemRepresentation
from .understanding import classify_problem, represent_problem


@dataclass(frozen=True)
class IntentSignal:
    intent: str
    confidence: Decimal
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class UnderstandingResult:
    normalized_text: str
    classification: ProblemClassification
    representation: ProblemRepresentation
    intent: IntentSignal
    ambiguity: tuple[str, ...] = ()


_EXPLAIN = ("توضیح", "شرح", "چرا", "چگونه", "explain", "why", "how")
_SOLVE = ("حل", "حساب", "جواب", "solve", "calculate", "answer")
_QUESTION_WORDS = ("چقدر", "چند", "what", "how much", "how many")


def detect_intent(text: str) -> IntentSignal:
    normalized = normalize_math_text(text).lower()
    solve_hits = tuple(token for token in _SOLVE if token in normalized)
    explain_hits = tuple(token for token in _EXPLAIN if token in normalized)
    if solve_hits and explain_hits:
        return IntentSignal("solve_and_explain", Decimal("0.85"), solve_hits + explain_hits)
    if solve_hits or any(ch.isdigit() for ch in normalized) or "=" in normalized:
        return IntentSignal("solve", Decimal("0.90"), solve_hits or ("mathematical_structure",))
    if explain_hits or any(token in normalized for token in _QUESTION_WORDS):
        return IntentSignal("explain", Decimal("0.80"), explain_hits or _QUESTION_WORDS)
    return IntentSignal("clarify", Decimal("0.55"), ("insufficient_intent_signal",))


def detect_ambiguity(text: str) -> tuple[str, ...]:
    normalized = normalize_math_text(text)
    issues: list[str] = []
    if not normalized:
        issues.append("empty_input")
    if normalized.count("=") > 1 and "\n" not in normalized:
        issues.append("multiple_equations_without_structure")
    if normalized.count("(") != normalized.count(")"):
        issues.append("unbalanced_parentheses")
    if re.search(r"[×÷*/+\-]{2,}", normalized):
        issues.append("adjacent_operators")
    return tuple(issues)


def understand(problem: ProblemInput) -> UnderstandingResult:
    classification = classify_problem(problem)
    representation = represent_problem(problem)
    intent = detect_intent(problem.text)
    return UnderstandingResult(
        normalize_math_text(problem.text),
        classification,
        representation,
        intent,
        detect_ambiguity(problem.text),
    )
