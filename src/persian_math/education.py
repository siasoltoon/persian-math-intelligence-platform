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
    EducationalLevel.ELEMENTARY: CurriculumRule(EducationalLevel.ELEMENTARY, Difficulty.EASY, "concrete"),
    EducationalLevel.MIDDLE: CurriculumRule(EducationalLevel.MIDDLE, Difficulty.MEDIUM, "guided"),
    EducationalLevel.HIGH_SCHOOL: CurriculumRule(EducationalLevel.HIGH_SCHOOL, Difficulty.MEDIUM, "exam_ready"),
    EducationalLevel.UNIVERSITY: CurriculumRule(EducationalLevel.UNIVERSITY, Difficulty.HARD, "formal"),
    EducationalLevel.ADVANCED: CurriculumRule(EducationalLevel.ADVANCED, Difficulty.EXPERT, "analytical"),
    EducationalLevel.OLYMPIAD: CurriculumRule(EducationalLevel.OLYMPIAD, Difficulty.EXPERT, "proof_oriented"),
}


def curriculum_for(profile: UserProfile) -> CurriculumRule:
    return _RULES[profile.educational_level]


def adapt_explanation_level(profile: UserProfile, requested: EducationalLevel | None = None) -> EducationalLevel:
    return requested or profile.educational_level
