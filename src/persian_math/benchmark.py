from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    domain: str
    input_text: str
    expected: str


@dataclass(frozen=True)
class BenchmarkResult:
    case_id: str
    passed: bool
    actual: str
    expected: str


def run_benchmark(
    cases: tuple[BenchmarkCase, ...], runner: Callable[[str], str]
) -> tuple[BenchmarkResult, ...]:
    results = []
    for case in cases:
        try:
            actual = runner(case.input_text)
            results.append(
                BenchmarkResult(case.case_id, actual == case.expected, actual, case.expected)
            )
        except (RuntimeError, TypeError, ValueError):
            results.append(BenchmarkResult(case.case_id, False, "ERROR", case.expected))
    return tuple(results)


def pass_rate(results: tuple[BenchmarkResult, ...]) -> float:
    return sum(item.passed for item in results) / len(results) if results else 0.0
