from decimal import Decimal

from persian_math.domain import ProblemInput
from persian_math.understanding import classify_problem, represent_problem


def test_classifies_persian_equation():
    result = classify_problem(ProblemInput("معادله ۲x + ۱ = ۵ را حل کن"))
    assert result.domain == "algebra"
    assert result.intent == "solve"
    assert result.confidence >= Decimal("0.90")


def test_represents_equation():
    result = represent_problem(ProblemInput("۲ + ۳ = ۵"))
    assert result.kind == "equation"



def test_represents_expression_with_whitespace_and_persian_digits():
    result = represent_problem(ProblemInput("۲ + ۳ × ۴"))
    assert result.kind == "expression"
    assert result.expression == "2 + 3 * 4"


def test_represents_concept_prompt_without_math_payload():
    result = represent_problem(ProblemInput("گراف و ترکیبیات را توضیح بده"))
    assert result.kind == "concept"
    assert result.expression is None
