from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OcrBenchmarkCase:
    case_id: str
    category: str
    expected_text: str
    expected_structure: tuple[str, ...]


@dataclass(frozen=True)
class OcrBenchmarkResult:
    case_id: str
    character_accuracy: float
    expression_accuracy: float
    structure_accuracy: float


def _accuracy(expected: str, actual: str) -> float:
    if not expected:
        return 1.0 if not actual else 0.0
    matches = sum(a == b for a, b in zip(expected, actual))
    return matches / max(len(expected), len(actual), 1)


def score_case(
    case: OcrBenchmarkCase, actual_text: str, actual_structure: tuple[str, ...]
) -> OcrBenchmarkResult:
    return OcrBenchmarkResult(
        case.case_id,
        _accuracy(case.expected_text, actual_text),
        1.0 if case.expected_text == actual_text else 0.0,
        1.0 if case.expected_structure == actual_structure else 0.0,
    )


def aggregate(results: tuple[OcrBenchmarkResult, ...]) -> dict[str, float]:
    if not results:
        return {"character_accuracy": 0.0, "expression_accuracy": 0.0, "structure_accuracy": 0.0}
    n = len(results)
    return {
        "character_accuracy": sum(r.character_accuracy for r in results) / n,
        "expression_accuracy": sum(r.expression_accuracy for r in results) / n,
        "structure_accuracy": sum(r.structure_accuracy for r in results) / n,
    }
