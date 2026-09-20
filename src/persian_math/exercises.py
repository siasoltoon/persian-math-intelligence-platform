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


def _linear(index: int, difficulty: Difficulty) -> Exercise:
    a = index + 2
    b = index + 3
    answer = sp.Rational(-b, a)
    return Exercise(f"{a}x + {b} = 0", difficulty, "algebra", answer)


def generate(spec: ExerciseSpec) -> tuple[Exercise, ...]:
    if spec.count < 1 or spec.count > 100:
        raise ValueError("count out of allowed range")
    if spec.domain != "algebra":
        raise ValueError("unsupported exercise domain")
    return tuple(_linear(spec.seed + i, spec.difficulty) for i in range(spec.count))


def validate_exercise(exercise: Exercise) -> bool:
    if exercise.domain == "algebra" and "=" in exercise.prompt:
        lhs, rhs = exercise.prompt.split("=", 1)
        x = sp.Symbol("x")
        expr = sp.sympify(lhs.replace("x", "*x")) - sp.sympify(rhs)
        return bool(sp.simplify(expr.subs(x, exercise.answer) == 0))
    return False
