from persian_math.domain import ProblemInput
from persian_math.understanding import classify_problem, represent_problem


def test_classifies_persian_equation():
    result = classify_problem(ProblemInput("معادله ۲x + ۱ = ۵ را حل کن"))
    assert result.domain == "algebra"
    assert result.intent == "solve"
    assert result.confidence >= 0.9


def test_represents_equation():
    result = represent_problem(ProblemInput("۲ + ۳ = ۵"))
    assert result.kind == "equation"
