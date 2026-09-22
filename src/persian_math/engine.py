from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .canonical import parse_equation, parse_expression
from .domain import (
    ConfidenceLevel,
    Problem,
    ProblemInput,
    ProblemRepresentation,
    VerificationResult,
)
from .solver import SolverResult, solve, solve_word_problem
from .understanding import classify_problem, represent_problem
from .verification import (
    verify_antiderivative_result,
    verify_derivative_result,
    verify_equation_independently,
    verify_expression_result,
    verify_limit_result,
    verify_system_result,
)


@dataclass(frozen=True)
class EngineResult:
    problem: Problem
    solver: SolverResult
    verification: VerificationResult | None


def process(text: str, *, symbol_name: str = "x") -> EngineResult:
    problem_input = ProblemInput(text)
    word_result, word_expression, word_kind = solve_word_problem(text)
    if word_result.success and word_kind == "expression" and word_expression is not None:
        representation = ProblemRepresentation("expression", str(word_expression), text)
    elif word_result.success and word_kind is not None:
        representation = ProblemRepresentation(word_kind, word_expression, text)
    else:
        representation = represent_problem(problem_input)
    classification = classify_problem(problem_input)
    problem = Problem(problem_input, representation, classification)
    if word_result.success:
        solver_result = word_result
    elif representation.kind == "concept":
        solver_result = SolverResult(
            False,
            None,
            "understanding",
            "mathematical expression required",
        )
    else:
        solver_result = solve(representation.expression, symbol_name=symbol_name)

    verification: VerificationResult | None = None
    if not solver_result.success:
        return EngineResult(problem, solver_result, verification)

    if solver_result.method == "derivative":
        metadata = solver_result.metadata or {}
        expression = parse_expression(str(metadata["source_expression"])).expression
        verification = verify_derivative_result(
            expression, sp.Symbol(str(metadata["symbol"])), solver_result.value
        )
    elif solver_result.method == "integral":
        metadata = solver_result.metadata or {}
        expression = parse_expression(str(metadata["source_expression"])).expression
        verification = verify_antiderivative_result(
            expression, sp.Symbol(str(metadata["symbol"])), solver_result.value
        )
    elif solver_result.method == "definite_integral":
        metadata = solver_result.metadata or {}
        expression = parse_expression(str(metadata["source_expression"])).expression
        verification = verify_expression_result(
            sp.integrate(
                expression,
                (
                    sp.Symbol(str(metadata["symbol"])),
                    metadata["lower"],
                    metadata["upper"],
                ),
            ),
            solver_result.value,
        )
    elif solver_result.method == "limit":
        metadata = solver_result.metadata or {}
        expression = parse_expression(str(metadata["source_expression"])).expression
        verification = verify_limit_result(
            expression,
            sp.Symbol(str(metadata["symbol"])),
            metadata["point"],
            solver_result.value,
        )
    elif solver_result.method == "symbolic_system":
        metadata = solver_result.metadata or {}
        verification = verify_system_result(
            metadata["equations"],
            metadata["symbols"],
            solver_result.value,
        )
    elif solver_result.method == "function_analysis":
        metadata = solver_result.metadata or {}
        expression = parse_expression(str(metadata["source_expression"])).expression
        symbol = sp.Symbol(str(metadata["symbol"]))
        derivative = sp.diff(expression, symbol)
        second = sp.diff(expression, symbol, 2)
        critical = tuple(sp.solve(derivative, symbol))
        expected = []
        for point in critical:
            second_value = sp.simplify(second.subs(symbol, point))
            extremum_type = (
                "max" if second_value < 0 else "min" if second_value > 0 else "inconclusive"
            )
            expected.append((point, sp.simplify(expression.subs(symbol, point)), extremum_type))
        expected_value = {
            "critical_points": tuple(expected),
            "increasing": sp.solve_univariate_inequality(derivative > 0, symbol),
            "decreasing": sp.solve_univariate_inequality(derivative < 0, symbol),
            "inflection_points": tuple(
                (point, sp.simplify(expression.subs(symbol, point)))
                for point in sp.solve(second, symbol)
            ),
        }
        if solver_result.value != expected_value:
            verification = VerificationResult(
                False,
                ConfidenceLevel.HIGH,
                ("function_analysis_mismatch",),
                (expected_value, solver_result.value),
            )
        else:
            verification = VerificationResult(
                True,
                ConfidenceLevel.HIGH,
                ("independent_calculus_recheck", "critical_point_recheck"),
                (expected_value,),
            )
    elif representation.kind == "expression":
        expression = parse_expression(representation.expression).expression
        verification = verify_expression_result(expression, solver_result.value)
    elif representation.kind == "equation":
        lhs, rhs = parse_equation(representation.expression)
        if isinstance(solver_result.value, tuple):
            verification = verify_equation_independently(
                lhs, rhs, sp.Symbol(symbol_name), solver_result.value
            )
        else:
            verification = VerificationResult(
                False,
                ConfidenceLevel.LOW,
                ("invalid_solver_output",),
                (solver_result.value,),
            )

    return EngineResult(problem, solver_result, verification)
