from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    number: int
    text: str


@dataclass(frozen=True)
class QuestionSlice:
    index: int
    page: int
    text: str


@dataclass(frozen=True)
class DocumentIndex:
    pages: tuple[Page, ...]
    questions: tuple[QuestionSlice, ...]

    def question(self, index: int) -> QuestionSlice:
        for item in self.questions:
            if item.index == index:
                return item
        raise KeyError(index)


def validate_document(data: bytes, max_bytes: int = 20 * 1024 * 1024) -> None:
    if not data or len(data) > max_bytes:
        raise ValueError("document exceeds safe bounds")
    if data[:4] != b"%PDF":
        raise ValueError("unsupported document format")


def index_text_pages(pages: tuple[Page, ...]) -> DocumentIndex:
    if not pages:
        raise ValueError("empty document")
    questions: list[QuestionSlice] = []
    for page in pages:
        for line in page.text.splitlines():
            stripped = line.strip()
            if (\n                len(stripped) >= 3\n                and stripped[0].isdigit()\n                and (stripped[1] == "." or stripped[1] == ")")\n            ):
                questions.append(QuestionSlice(int(stripped[0]), page.number, stripped[2:].strip()))
    return DocumentIndex(pages, tuple(questions))
