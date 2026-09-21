from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UiPolicy:
    direction: str = "rtl"
    language: str = "fa"
    max_message_chars: int = 6000
    formula_direction: str = "ltr"


@dataclass(frozen=True)
class RenderedAnswer:
    title_fa: str
    body_fa: str
    verified: bool
    direction: str = "rtl"


def render_answer(body_fa: str, *, verified: bool, policy: UiPolicy | None = None) -> RenderedAnswer:
    active = policy or UiPolicy()
    if not body_fa.strip() or len(body_fa) > active.max_message_chars:
        raise ValueError("answer exceeds UI bounds")
    if active.direction != "rtl" or active.language != "fa":
        raise ValueError("unsupported default UI policy")
    title = "پاسخ تأییدشده" if verified else "پاسخ نیازمند بررسی"
    return RenderedAnswer(title, body_fa.strip(), verified, active.direction)
