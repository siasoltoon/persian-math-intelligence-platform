from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from collections.abc import Callable
from typing import TypeVar


@dataclass(frozen=True)
class FailurePolicy:
    timeout_seconds: float = 30.0
    max_attempts: int = 3


@dataclass(frozen=True)
class TestCase:
    case_id: str
    category: str
    run: Callable[[], bool]


@dataclass(frozen=True)
class TestResult:
    case_id: str
    category: str
    passed: bool


def run_matrix(cases: tuple[TestCase, ...]) -> tuple[TestResult, ...]:
    results = []
    for case in cases:
        try:
            results.append(TestResult(case.case_id, case.category, bool(case.run())))
        except (ArithmeticError, RuntimeError, TypeError, ValueError):
            results.append(TestResult(case.case_id, case.category, False))
    return tuple(results)


def pass_rate(results: tuple[TestResult, ...]) -> float:
    return sum(item.passed for item in results) / len(results) if results else 0.0


T = TypeVar("T")


def retry(operation: Callable[[], T], policy: FailurePolicy) -> T:
    if policy.max_attempts < 1 or policy.timeout_seconds <= 0:
        raise ValueError("invalid failure policy")
    started = monotonic()
    last: Exception | None = None
    for _ in range(policy.max_attempts):
        if monotonic() - started > policy.timeout_seconds:
            break
        try:
            return operation()
        except (ArithmeticError, RuntimeError, TypeError, ValueError) as exc:
            last = exc
    if last is not None:
        raise last
    raise TimeoutError("operation timeout")
