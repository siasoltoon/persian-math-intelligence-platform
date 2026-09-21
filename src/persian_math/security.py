from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from urllib.parse import urlparse


@dataclass(frozen=True)
class SecurityPolicy:
    max_text_chars: int = 20_000
    max_file_bytes: int = 20 * 1024 * 1024
    allowed_schemes: tuple[str, ...] = ("https",)


def validate_text(text: str, policy: SecurityPolicy = SecurityPolicy()) -> str:
    if not isinstance(text, str) or not text.strip() or len(text) > policy.max_text_chars:
        raise ValueError("invalid text input")
    return text.strip()


def safe_filename(name: str) -> str:
    if not name or name in {".", ".."} or "/" in name or "\\" in name or PurePosixPath(name).name != name:
        raise ValueError("unsafe filename")
    return name


def validate_url(url: str, policy: SecurityPolicy = SecurityPolicy()) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in policy.allowed_schemes or not parsed.hostname:
        raise ValueError("unsupported URL")
    host = parsed.hostname.lower()
    if host in {"localhost", "127.0.0.1", "::1"} or host.startswith("10.") or host.startswith("192.168."):
        raise ValueError("private network URL rejected")
