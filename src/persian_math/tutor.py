from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .domain import EducationalLevel, UserProfile


class TutorAction(str, Enum):
    EXPLAIN = "explain"
    HINT = "hint"
    ASK = "ask"
    CHECK = "check"
    SIMPLIFY = "simplify"


@dataclass(frozen=True)
class TutorTurn:
    action: TutorAction
    message_fa: str
    expected_answer: Any | None = None


@dataclass(frozen=True)
class TutorSession:
    user: UserProfile
    level: EducationalLevel
    turns: tuple[TutorTurn, ...] = ()


def start_session(user: UserProfile) -> TutorSession:
    return TutorSession(user=user, level=user.educational_level)


def next_hint(session: TutorSession, topic: str) -> TutorTurn:
    return TutorTurn(
        TutorAction.HINT,
        f"راهنما: ابتدا مفهوم «{topic}» را مشخص کن و داده‌های مسئله را جدا کن.",
    )


def ask_step(session: TutorSession, question: str, expected_answer: Any | None = None) -> TutorTurn:
    return TutorTurn(TutorAction.ASK, question, expected_answer)


def check_answer(session: TutorSession, correct: bool) -> TutorTurn:
    if correct:
        return TutorTurn(TutorAction.CHECK, "درست است. حالا مرحله بعد را انجام بده.")
    return TutorTurn(
        TutorAction.CHECK,
        "این پاسخ با بررسی ریاضی سازگار نیست؛ یک مرحله قبل را دوباره بررسی کن.",
    )
