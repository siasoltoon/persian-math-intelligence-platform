from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image

import fitz

from persian_math.file_intelligence import FileLimits, inspect_document, validate_file_bytes


def _png() -> bytes:
    stream = BytesIO()
    Image.new("RGB", (64, 64), "white").save(stream, format="PNG")
    return stream.getvalue()


def test_image_document_without_ocr() -> None:
    result = inspect_document(_png(), "question.png")
    assert result.media_type == "image"
    assert result.pages[0].page_number == 1
    assert "ocr_not_requested" in result.warnings


def test_file_limit_rejects_large_payload() -> None:
    with pytest.raises(ValueError):
        validate_file_bytes(b"x" * 101, FileLimits(max_bytes=100))


def test_pdf_signature_is_checked() -> None:
    with pytest.raises(ValueError):
        inspect_document(b"not a pdf", "question.pdf")


def test_empty_file_rejected() -> None:
    with pytest.raises(ValueError):
        validate_file_bytes(b"")


def _pdf() -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "x + 2 = 5")
    data = document.tobytes()
    document.close()
    return data


def test_text_pdf_preserves_page_text() -> None:
    result = inspect_document(_pdf(), "question.pdf")
    assert result.media_type == "application/pdf"
    assert len(result.pages) == 1
    assert "x + 2 = 5" in result.pages[0].text
    assert "x + 2 = 5" in result.extracted_text


def test_pdf_page_limit_is_enforced() -> None:
    document = fitz.open()
    for _ in range(2):
        document.new_page()
    data = document.tobytes()
    document.close()
    with pytest.raises(ValueError, match="page limit"):
        inspect_document(data, "many.pdf", limits=FileLimits(max_pages=1))
