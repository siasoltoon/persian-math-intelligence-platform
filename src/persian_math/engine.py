from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .canonical import parse_equation, parse_expression
from .domain import ConfidenceLevel, Problem, ProblemInput, VerificationResult
from .solver import SolverResult, solve
from .understanding import classify_problem, represent_problem
from .verification import verify_expression_result, verify_solution_set


@dataclass(frozen=True)
class EngineResult:
    problem: Problem
    solver: SolverResult
    verification: VerificationResult | None


def process(text: str, *, symbol_name: str = "x") -> EngineResult:
    problem_input = ProblemInput(text)
    representation = represent_problem(problem_input)
    classification = classify_problem(problem_input)
    problem = Problem(problem_input, representation, classification)
    solver_result = solve(representation.expression, symbol_name=symbol_name)
    verification: VerificationResult | None = None

    if solver_result.success and representation.kind == "expression":
        expression = parse_expression(text).expression
        verification = verify_expression_result(expression, solver_result.value)
    elif solver_result.success and representation.kind == "equation":
        lhs, rhs = parse_equation(text)
        if isinstance(solver_result.value, tuple):
            verification = verify_solution_set(lhs, rhs, sp.Symbol(symbol_name), solver_result.value)
        else:
            verification = VerificationResult(
                False,
                ConfidenceLevel.LOW,
                ("invalid_solver_output",),
                (solver_result.value,),
            )

    return EngineResult(problem, solver_result, verification)
