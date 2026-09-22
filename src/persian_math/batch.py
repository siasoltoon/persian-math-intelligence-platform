from __future__ import annotations

import re
from collections.abc import Iterable

MAX_BATCH_ITEMS = 12
MAX_BATCH_CHARS = 12000

_QUESTION_LABEL = re.compile(
    r"^\s*(?:س(?:ؤال|وال)|مسئله|مساله|question|problem)\s*[0-9۰-۹]*\s*[:.)-]\s*",
    re.IGNORECASE,
)
_NUMBERED_LABEL = re.compile(r"^\s*[0-9۰-۹]+\s*[.)-]\s+")
_MATH_SIGNAL = re.compile(
    r"(?:[0-9۰-۹]|[=+\-*/^×÷√∫∑π≤≥<>]|\b(?:sin|cos|tan|log|ln|lim)\b|"
    r"\b(?:x|y|z|f\s*\()\b|مشتق|انتگرال|حد|معادله|ماتریس|مجموع|مساحت|احتمال|"
    r"میانگین|واریانس|تجزیه|دترمینان|دایره|مثلث|توان|ریشه|تابع)"
)


def _clean_block(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def _math_like(text: str) -> bool:
    return bool(_MATH_SIGNAL.search(text))


def _split_by_label(lines: list[str], pattern: re.Pattern[str]) -> list[str]:
    starts = [index for index, line in enumerate(lines) if pattern.match(line)]
    if len(starts) < 2:
        return []
    chunks: list[str] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = _clean_block("\n".join(lines[start:end]))
        if block:
            chunks.append(pattern.sub("", block, count=1).strip())
    return chunks if len(chunks) >= 2 else []


def _split_numbered(lines: list[str]) -> list[str]:
    starts = [index for index, line in enumerate(lines) if _NUMBERED_LABEL.match(line)]
    if len(starts) < 2:
        return []
    chunks: list[str] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = _clean_block("\n".join(lines[start:end]))
        if block:
            chunks.append(_NUMBERED_LABEL.sub("", block, count=1).strip())
    # Do not split a multi-part single problem (for example function analysis)
    # unless every numbered block independently contains mathematical signal.
    return chunks if len(chunks) >= 2 and all(_math_like(chunk) for chunk in chunks) else []


def _split_blank_blocks(text: str) -> list[str]:
    blocks = [_clean_block(block) for block in re.split(r"\n\s*\n", text) if block.strip()]
    if len(blocks) < 2 or not all(_math_like(block) for block in blocks):
        return []
    # A multiline linear system is one problem, not a batch.
    if sum(1 for block in blocks if "\n" in block and "=" in block) >= 1:
        return []
    return blocks


def split_problem_batch(text: str) -> tuple[str, ...]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return ()
    if len(normalized) > MAX_BATCH_CHARS:
        raise ValueError("batch input exceeds limit")

    lines = normalized.splitlines()
    chunks = _split_by_label(lines, _QUESTION_LABEL)
    if not chunks:
        chunks = _split_numbered(lines)
    if not chunks:
        chunks = _split_blank_blocks(text)
    if not chunks:
        return (normalized,)

    chunks = tuple(_clean_block(chunk) for chunk in chunks if chunk.strip())
    if len(chunks) > MAX_BATCH_ITEMS:
        raise ValueError("too many problems in one batch")
    return chunks


def is_batch_input(text: str) -> bool:
    return len(split_problem_batch(text)) > 1
