from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .domain import EducationalLevel, Solution, SolutionStep


@dataclass(frozen=True)
class Explanation:
    title_fa: str
    steps: tuple[SolutionStep, ...]
    final_fa: str
    verification_fa: str | None = None
    notes_fa: tuple[str, ...] = ()
    common_mistakes_fa: tuple[str, ...] = ()


def _format(value: Any) -> str:
    try:
        return str(sp.sstr(value))
    except Exception:
        return str(value)


def explain_solution(
    value: Any,
    *,
    method: str,
    level: EducationalLevel = EducationalLevel.HIGH_SCHOOL,
    verification: str | None = None,
    original: Any | None = None,
) -> Explanation:
    labels = {
        EducationalLevel.ELEMENTARY: "ساده و مرحله‌به‌مرحله",
        EducationalLevel.MIDDLE: "ساده و آموزشی",
        EducationalLevel.HIGH_SCHOOL: "آموزشی و استاندارد",
        EducationalLevel.ENTRANCE_EXAM: "آزمونی و نکته‌محور",
        EducationalLevel.UNIVERSITY: "دقیق و دانشگاهی",
        EducationalLevel.ADVANCED: "فنی و تحلیلی",
        EducationalLevel.OLYMPIAD: "تحلیلی و نکته‌محور",
    }
    steps = [SolutionStep(f"صورت استانداردشده: {_format(original)}.", original)]
    descriptions = {
        "symbolic_simplification": "عبارت را با قواعد جبری و ساده‌سازی نمادین محاسبه می‌کنیم.",
        "symbolic_equation": "معادله را نمادین حل می‌کنیم و همه جواب‌های سازگار را استخراج می‌کنیم.",
        "symbolic_inequality": "نامعادله را نمادین حل می‌کنیم و دامنه و جهت نابرابری را حفظ می‌کنیم.",
        "symbolic_system": "معادلات دستگاه را هم‌زمان حل و جواب‌های سازگار را بررسی می‌کنیم.",
        "derivative": "قواعد مشتق‌گیری را اعمال می‌کنیم.",
        "integral": "انتگرال نمادین را نسبت به متغیر انتخاب‌شده محاسبه می‌کنیم.",
        "limit": "حد را در نقطه موردنظر محاسبه و بررسی می‌کنیم.",
    }
    steps.append(
        SolutionStep(
            descriptions.get(method, f"روش تخصصی «{method}» را اعمال می‌کنیم."),
            value,
        )
    )
    steps.append(SolutionStep(f"سطح توضیح: {labels[level]}."))
    return Explanation(
        "حل مسئله",
        tuple(steps),
        f"پاسخ نهایی: {_format(value)}",
        verification,
        ("نتیجه فقط پس از Verification مستقل، تأییدشده اعلام می‌شود.",),
        ("بی‌دقتی در علامت، پرانتز و دامنه از خطاهای رایج‌اند.",),
    )


def explanation_to_solution(
    explanation: Explanation, value: Any, method: str
) -> Solution:
    return Solution(value=value, steps=explanation.steps, method=method)
