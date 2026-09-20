from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EducationalLevel(str, Enum):
    ELEMENTARY = "elementary"
    MIDDLE = "middle"
    HIGH_SCHOOL = "high_school"
    ENTRANCE_EXAM = "entrance_exam"
    UNIVERSITY = "university"
    ADVANCED = "advanced"
    OLYMPIAD = "olympiad"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


@dataclass(frozen=True)
class ProblemInput:
    text: str
    language: str = "fa"


@dataclass(frozen=True)
class ProblemRepresentation:
    kind: str
    expression: Any
    source_text: str


@dataclass(frozen=True)
class ProblemClassification:
    intent: str
    domain: str
    confidence: Decimal


@dataclass(frozen=True)
class SolutionStep:
    description_fa: str
    expression: Any | None = None


@dataclass(frozen=True)
class Solution:
    value: Any
    steps: tuple[SolutionStep, ...] = ()
    method: str = "symbolic"


@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    confidence: ConfidenceLevel
    evidence: tuple[str, ...] = ()
    independent_values: tuple[Any, ...] = ()


@dataclass(frozen=True)
class Problem:
    input: ProblemInput
    representation: ProblemRepresentation | None = None
    classification: ProblemClassification | None = None


@dataclass(frozen=True)
class UserProfile:
    user_id: str
    educational_level: EducationalLevel = EducationalLevel.HIGH_SCHOOL
    preferred_language: str = "fa"


@dataclass(frozen=True)
class Exercise:
    prompt: str
    difficulty: Difficulty
    domain: str
    answer: Any
