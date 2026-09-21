from __future__ import annotations

from io import BytesIO

import pymupdf
import pytest
from PIL import Image

from persian_math.file_intelligence import (
    FileLimits,
    best_document_text,
    inspect_document,
    validate_file_bytes,
)
from persian_math.ocr import ImageMetadata, OcrRegion, OcrResult


def _png() -> bytes:
    stream = BytesIO()
    Image.new("RGB", (64, 64), "white").save(stream, format="PNG")
    return stream.getvalue()


class StubOcr:
    def __init__(self, text: str = "2x + 3 = 7", confidence: float = 0.95) -> None:
        self.text = text
        self.confidence = confidence

    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        return OcrResult(
            self.text,
            self.confidence,
            (OcrRegion(self.text, self.confidence, (10, 10, 100, 30), "math"),),
        )


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


def _pdf(text: str = "x + 2 = 5") -> bytes:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    data = document.tobytes()
    document.close()
    return data


def test_text_pdf_preserves_page_text() -> None:
    result = inspect_document(_pdf(), "question.pdf")
    assert result.media_type == "application/pdf"
    assert len(result.pages) == 1
    assert "x + 2 = 5" in result.pages[0].text
    assert result.pages[0].selected_source == "pdf_text"
    assert best_document_text(result) == result.pages[0].text.strip()


def test_scanned_like_pdf_uses_ocr_when_native_layer_is_only_watermark() -> None:
    result = inspect_document(
        _pdf("Scanned by CamScanner"),
        "scan.pdf",
        ocr_backend=StubOcr(),
    )
    assert result.pages[0].selected_source == "ocr"
    assert best_document_text(result) == "2x + 3 = 7"
    assert "Scanned by CamScanner" not in best_document_text(result)


def test_low_confidence_ocr_does_not_become_problem_text() -> None:
    result = inspect_document(
        _pdf("Scanned by CamScanner"),
        "scan.pdf",
        ocr_backend=StubOcr(confidence=0.41),
    )
    assert result.extracted_text == ""
    assert "ocr_low_confidence" in result.warnings


def test_pdf_page_limit_is_enforced() -> None:
    document = pymupdf.open()
    for _ in range(2):
        document.new_page()
    data = document.tobytes()
    document.close()
    with pytest.raises(ValueError, match="page limit"):
        inspect_document(data, "many.pdf", limits=FileLimits(max_pages=1))


def test_pdf_pixel_limit_is_enforced() -> None:
    with pytest.raises(ValueError, match="pixel limit"):
        inspect_document(_pdf(), "large.pdf", limits=FileLimits(max_page_pixels=100))
