from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class MessageKind(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    DOCUMENT = "document"


@dataclass(frozen=True)
class IncomingMessage:
    user_id: str
    kind: MessageKind
    text: str = ""
    payload: bytes | None = None


@dataclass(frozen=True)
class OutgoingMessage:
    text_fa: str
    buttons: tuple[str, ...] = ()


class ApplicationPort(Protocol):
    def handle(self, message: IncomingMessage) -> OutgoingMessage: ...


@dataclass(frozen=True)
class TelegramMenu:
    items: tuple[str, ...] = ("حل مسئله", "راهنما", "تمرین", "پروفایل", "تنظیمات")


def validate_incoming(message: IncomingMessage) -> None:
    if not message.user_id.strip():
        raise ValueError("user id required")
    if message.kind == MessageKind.TEXT and not message.text.strip():
        raise ValueError("text required")
    if message.kind != MessageKind.TEXT and not message.payload:
        raise ValueError("payload required")


def localize_error(code: str) -> OutgoingMessage:
    messages = {
        "invalid_input": "ورودی قابل پردازش نیست. لطفاً صورت مسئله را واضح‌تر ارسال کن.",
        "temporary_failure": "پردازش موقتاً ناموفق بود. لطفاً دوباره تلاش کن.",
        "uncertain": "اطمینان کافی برای پاسخ قطعی وجود ندارد؛ لطفاً ورودی را واضح‌تر ارسال کن.",
    }
    return OutgoingMessage(\n        messages.get(code, "در پردازش مسئله مشکلی پیش آمد؛ لطفاً دوباره تلاش کن.")\n    )
