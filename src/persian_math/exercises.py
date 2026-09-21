from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .domain import Difficulty, Exercise


@dataclass(frozen=True)
class ExerciseSpec:
    domain: str
    difficulty: Difficulty
    count: int = 1
    seed: int = 0
    target: str | None = None


def _linear(index: int, difficulty: Difficulty) -> Exercise:
    a = index + 2
    b = index + 3
    answer = sp.Rational(-b, a)
    return Exercise(f"{a}x + {b} = 0", difficulty, "algebra", answer)


def _quadratic(index: int, difficulty: Difficulty) -> Exercise:
    root = index + 2
    expression = sp.expand((sp.Symbol("x") - root) ** 2)
    return Exercise(f"{expression} = 0", difficulty, "algebra", sp.Integer(root))


def _arithmetic(index: int, difficulty: Difficulty) -> Exercise:
    a, b = index + 4, index + 7
    return Exercise(f"{a} + {b}", difficulty, "arithmetic", sp.Integer(a + b))


def _calculus(index: int, difficulty: Difficulty) -> Exercise:
    x = sp.Symbol("x")
    power = index + 2
    return Exercise(
        f"d/dx x^{power}", difficulty, "calculus", power * x ** (power - 1)
    )


def generate(spec: ExerciseSpec) -> tuple[Exercise, ...]:
    if not 1 <= spec.count <= 100:
        raise ValueError("count out of allowed range")
    generators = {
        "algebra": (
            _linear
            if spec.difficulty in {Difficulty.EASY, Difficulty.MEDIUM}
            else _quadratic
        ),
        "arithmetic": _arithmetic,
        "calculus": _calculus,
    }
    if spec.domain not in generators:
        raise ValueError("unsupported exercise domain")
    return tuple(
        generators[spec.domain](spec.seed + i, spec.difficulty)
        for i in range(spec.count)
    )


def validate_exercise(exercise: Exercise) -> bool:
    try:
        x = sp.Symbol("x")
        if exercise.domain == "arithmetic":
            return bool(sp.simplify(sp.sympify(exercise.prompt) - exercise.answer) == 0)
        if exercise.domain == "calculus":
            power = exercise.prompt.split("^")[-1]
            expected = sp.diff(x ** int(power), x)
            return bool(sp.simplify(expected - exercise.answer) == 0)
        if exercise.domain == "algebra" and "=" in exercise.prompt:
            lhs, rhs = exercise.prompt.split("=", 1)
            expr = sp.sympify(lhs.replace("x", "*x")) - sp.sympify(rhs)
            return bool(sp.simplify(expr.subs(x, exercise.answer)) == 0)
    except (TypeError, ValueError, SyntaxError, sp.SympifyError):
        return False
    return False
