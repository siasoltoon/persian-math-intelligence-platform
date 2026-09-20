from __future__ import annotations

from dataclasses import dataclass

from .domain import Difficulty, EducationalLevel, UserProfile


@dataclass(frozen=True)
class CurriculumRule:
    level: EducationalLevel
    max_difficulty: Difficulty
    style: str
    prerequisite_domains: tuple[str, ...] = ()


_RULES = {
    EducationalLevel.ELEMENTARY: CurriculumRule(
        EducationalLevel.ELEMENTARY, Difficulty.EASY, "concrete"
    ),
    EducationalLevel.MIDDLE: CurriculumRule(EducationalLevel.MIDDLE, Difficulty.MEDIUM, "guided"),
    EducationalLevel.ENTRANCE_EXAM: CurriculumRule(
        EducationalLevel.ENTRANCE_EXAM, Difficulty.HARD, "exam_ready"
    ),
    EducationalLevel.HIGH_SCHOOL: CurriculumRule(
        EducationalLevel.HIGH_SCHOOL, Difficulty.MEDIUM, "exam_ready"
    ),
    EducationalLevel.UNIVERSITY: CurriculumRule(
        EducationalLevel.UNIVERSITY, Difficulty.HARD, "formal"
    ),
    EducationalLevel.ADVANCED: CurriculumRule(
        EducationalLevel.ADVANCED, Difficulty.EXPERT, "analytical"
    ),
    EducationalLevel.OLYMPIAD: CurriculumRule(
        EducationalLevel.OLYMPIAD, Difficulty.EXPERT, "proof_oriented"
    ),
}


def curriculum_for(profile: UserProfile) -> CurriculumRule:
    return _RULES[profile.educational_level]


def adapt_explanation_level(
    profile: UserProfile, requested: EducationalLevel | None = None
) -> EducationalLevel:
    return requested or profile.educational_level


def recommended_difficulty(
    profile: UserProfile, recent_accuracy: float | None = None
) -> Difficulty:
    base = curriculum_for(profile).max_difficulty
    if recent_accuracy is None:
        return base
    if not 0.0 <= recent_accuracy <= 1.0:
        raise ValueError("accuracy must be between 0 and 1")
    if recent_accuracy < 0.50:
        return Difficulty.EASY
    if recent_accuracy < 0.75:
        return Difficulty.MEDIUM
    return base


def learning_objectives(profile: UserProfile, domain: str) -> tuple[str, ...]:
    style = curriculum_for(profile).style
    objectives = {
        "algebra": ("معادله و نامعادله", "تبدیل و ساده‌سازی عبارت"),
        "geometry": ("استدلال هندسی", "محاسبه طول، مساحت و زاویه"),
        "calculus": ("حد، مشتق و انتگرال", "تفسیر تغییرات"),
        "statistics": ("شاخص‌های آماری", "تفسیر داده"),
        "probability": ("احتمال رویداد", "تحلیل فضای نمونه"),
        "linear_algebra": ("بردار و ماتریس", "حل دستگاه خطی"),
        "number_theory": ("بخش‌پذیری", "ساختار اعداد"),
        "discrete_math": ("منطق و ترکیبیات", "مدل‌سازی ساختارهای گسسته"),
    }.get(domain, ("درک ساختار مسئله", "انتخاب روش مناسب"))
    return (
        *objectives,
        f"ارائه توضیح با سبک {style}",
        "حل یک نمونه و بررسی مستقل پاسخ",
    )
