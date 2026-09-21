from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    telegram_bot_token: str
    max_message_chars: int = 4000
    max_download_bytes: int = 20 * 1024 * 1024
    ocr_language: str = "eng"


def load_runtime_config() -> RuntimeConfig:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")
    language = os.environ.get("TESSERACT_LANG", "eng").strip() or "eng"\n    return RuntimeConfig(telegram_bot_token=token, ocr_language=language)
