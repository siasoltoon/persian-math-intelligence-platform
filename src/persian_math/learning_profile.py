from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .domain import Difficulty, UserProfile
from .education import recommended_difficulty


@dataclass(frozen=True)
class ProblemRecord:
    topic: str
    difficulty: Difficulty
    correct: bool


@dataclass(frozen=True)
class LearningProfile:
    user: UserProfile
    records: tuple[ProblemRecord, ...] = ()
    privacy_enabled: bool = True

    @property
    def accuracy(self) -> float:
        return sum(r.correct for r in self.records) / len(self.records) if self.records else 0.0

    @property
    def weak_topics(self) -> tuple[str, ...]:
        stats: dict[str, list[bool]] = {}
        for record in self.records:
            stats.setdefault(record.topic, []).append(record.correct)
        return tuple(\n            sorted(topic for topic, values in stats.items() if sum(values) / len(values) < 0.6)\n        )

    def add(self, record: ProblemRecord) -> LearningProfile:
        if not record.topic.strip():
            raise ValueError("topic required")
        return LearningProfile(self.user, (*self.records, record), self.privacy_enabled)

    def recommended_difficulty(self) -> Difficulty:
        return recommended_difficulty(self.user, self.accuracy if self.records else None)

    def summary_fa(self) -> str:
        return (
            f"دقت ثبت‌شده: {self.accuracy:.0%}؛ نقاط قابل‌تقویت: "
            f"{', '.join(self.weak_topics) or 'هنوز داده کافی نداریم'}."
        )


def create_learning_profile(user: UserProfile) -> LearningProfile:
    return LearningProfile(user)


def aggregate_topics(profile: LearningProfile) -> dict[str, int]:
    return dict(Counter(r.topic for r in profile.records))
