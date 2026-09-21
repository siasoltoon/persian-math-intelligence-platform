from __future__ import annotations
from dataclasses import dataclass
import sympy as sp
from .canonical import parse_equation, parse_expression, parse_inequality, parse_system
from .domain import ConfidenceLevel, Problem, ProblemInput, VerificationResult
from .solver import SolverResult, solve, solve_system
from .understanding import classify_problem, represent_problem
from .verification import verify_equation_independently, verify_expression_result

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
    symbol = sp.Symbol(symbol_name)
    try:
        if representation.kind == "system":
            equations = parse_system(text)
            symbols = tuple(sorted(set().union(*(e.free_symbols for pair in equations for e in pair)), key=str))
            solver_result = solve_system(equations, symbols)
            if not solver_result.success:
                return EngineResult(problem, solver_result, None)
            verified = True
            for item in solver_result.value:
                if not isinstance(item, dict) or not all(sp.simplify((lhs-rhs).subs(item)) == 0 for lhs, rhs in equations):
                    verified = False
            verification = VerificationResult(
                verified, ConfidenceLevel.HIGH if verified else ConfidenceLevel.LOW,
                ("system_substitution", "independent_solver"), tuple(solver_result.value),
            )
            return EngineResult(problem, solver_result, verification)
        solver_result = solve(representation.expression, symbol_name=symbol_name)
        verification = None
        if not solver_result.success:
            return EngineResult(problem, solver_result, None)
        if representation.kind == "expression":
            verification = verify_expression_result(parse_expression(text).expression, solver_result.value)
        elif representation.kind == "equation":
            lhs, rhs = parse_equation(text)
            candidates = tuple(solver_result.value) if isinstance(solver_result.value, (tuple, list)) else ()
            verification = verify_equation_independently(lhs, rhs, symbol, candidates)
        elif representation.kind == "inequality":
            lhs, op, rhs = parse_inequality(text)
            relation = {"<": sp.Lt, "<=": sp.Le, ">": sp.Gt, ">=": sp.Ge}[op](lhs, rhs)
            equivalent = sp.simplify(sp.Equivalent(relation, sp.And(solver_result.value, sp.S.true)))
            verification = VerificationResult(bool(equivalent is sp.true), ConfidenceLevel.HIGH if equivalent is sp.true else ConfidenceLevel.LOW, ("inequality_equivalence",), (solver_result.value,))
        return EngineResult(problem, solver_result, verification)
    except (TypeError, ValueError, NotImplementedError, sp.SympifyError):
        failed = SolverResult(False, None, "engine", "unable to solve the mathematical input")
        return EngineResult(problem, failed, VerificationResult(False, ConfidenceLevel.LOW, ("engine_parse_or_verification_failure",), ()))

