from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .domain import EducationalLevel, Solution, SolutionStep


@dataclass(frozen=True)
class Explanation:
    title_fa: str
    steps: tuple[SolutionStep, ...]
    final_fa: str
    verification_fa: str | None = None


def explain_solution(
    value: Any,
    *,
    method: str,
    level: EducationalLevel = EducationalLevel.HIGH_SCHOOL,
    verification: str | None = None,
) -> Explanation:
    level_text = {
        EducationalLevel.ELEMENTARY: "ساده و مرحله‌به‌مرحله",
        EducationalLevel.MIDDLE: "ساده و آموزشی",
        EducationalLevel.HIGH_SCHOOL: "آموزشی و استاندارد",
        EducationalLevel.ENTRANCE_EXAM: "آزمونی و نکته‌محور",
        EducationalLevel.UNIVERSITY: "دقیق و دانشگاهی",
        EducationalLevel.ADVANCED: "فنی و تحلیلی",
        EducationalLevel.OLYMPIAD: "تحلیلی و نکته‌محور",
    }[level]
    step = SolutionStep(f"روش حل: {method}؛ سطح توضیح: {level_text}.", value)
    final = f"پاسخ نهایی: {value}"
    return Explanation("حل مسئله", (step,), final, verification)


def explanation_to_solution(explanation: Explanation, value: Any, method: str) -> Solution:
    return Solution(value=value, steps=explanation.steps, method=method)
