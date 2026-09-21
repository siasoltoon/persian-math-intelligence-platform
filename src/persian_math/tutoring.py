from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .domain import EducationalLevel, UserProfile
from .solver import solve
from .verification import verify_expression_result


class TutorAction(str, Enum):
    TEACH = "teach"
    ASK = "ask"
    HINT = "hint"
    CHECK = "check"
    REEXPLAIN = "reexplain"
    PRACTICE = "practice"


@dataclass(frozen=True)
class TutorStep:
    index: int
    prompt_fa: str
    expected: Any | None = None
    hint_fa: str | None = None


@dataclass(frozen=True)
class TutorSession:
    session_id: str
    user: UserProfile
    topic: str
    steps: tuple[TutorStep, ...] = ()
    current_index: int = 0
    completed: bool = False


@dataclass(frozen=True)
class TutorResponse:
    action: TutorAction
    message_fa: str
    correct: bool | None = None
    next_index: int | None = None


def start_tutor(session_id: str, user: UserProfile, topic: str, steps: tuple[TutorStep, ...]) -> TutorSession:
    if not session_id.strip() or not topic.strip() or not steps:
        raise ValueError("invalid tutor session")
    return TutorSession(session_id, user, topic, steps)


def current_step(session: TutorSession) -> TutorStep:
    if session.completed or session.current_index >= len(session.steps):
        raise ValueError("tutor session is complete")
    return session.steps[session.current_index]


def hint(session: TutorSession) -> TutorResponse:
    step = current_step(session)
    return TutorResponse(TutorAction.HINT, step.hint_fa or "داده‌های مسئله را جدا کن و روش مناسب را انتخاب کن.", None, session.current_index)


def check(session: TutorSession, answer: Any) -> tuple[TutorSession, TutorResponse]:
    step = current_step(session)
    correct = False
    try:
        if step.expected is not None:
            correct = bool(__import__("sympy").simplify(__import__("sympy").sympify(answer) - __import__("sympy").sympify(step.expected)) == 0)
    except (TypeError, ValueError):
        correct = answer == step.expected
    if not correct:
        return session, TutorResponse(TutorAction.CHECK, "پاسخ با جواب مورد انتظار سازگار نیست. یک مرحله قبل را دوباره بررسی کن.", False, session.current_index)
    nxt = session.current_index + 1
    completed = nxt >= len(session.steps)
    updated = TutorSession(session.session_id, session.user, session.topic, session.steps, nxt, completed)
    msg = "آفرین، درست است." if not completed else "آفرین؛ مسیر آموزشی این تمرین کامل شد."
    return updated, TutorResponse(TutorAction.CHECK, msg, True, None if completed else nxt)


def reexplain(session: TutorSession) -> TutorResponse:
    step = current_step(session)
    style = {EducationalLevel.ELEMENTARY: "خیلی ساده و مرحله‌به‌مرحله", EducationalLevel.UNIVERSITY: "رسمی و دقیق"}.get(session.user.educational_level, "ساده و مرحله‌به‌مرحله")
    return TutorResponse(TutorAction.REEXPLAIN, f"این مرحله را {style} توضیح می‌دهیم: {step.prompt_fa}", None, session.current_index)


def progressive_practice(user: UserProfile, topic: str, count: int = 3) -> tuple[str, ...]:
    if not 1 <= count <= 20:
        raise ValueError("count out of range")
    return tuple(f"تمرین {i + 1}: یک مسئله {topic} در سطح {user.educational_level.value} حل کن." for i in range(count))
