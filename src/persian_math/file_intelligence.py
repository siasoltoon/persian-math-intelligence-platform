from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
import re
from typing import Any

from PIL import Image

from .ocr import (
    ImageMetadata,
    OcrBackend,
    OcrResult,
    validate_image_bytes,
    validate_image_metadata,
)

MAX_FILE_BYTES = 20 * 1024 * 1024
MAX_PDF_PAGES = 20
MAX_PDF_TEXT_CHARS = 80_000
MAX_PAGE_PIXELS = 30_000_000
MIN_NATIVE_TEXT_CHARS = 12
_SCANNER_WATERMARKS = (
    re.compile(r"^scanned by camscanner$", re.IGNORECASE),
    re.compile(r"^camscanner$", re.IGNORECASE),
)


@dataclass(frozen=True)
class FileLimits:
    max_bytes: int = MAX_FILE_BYTES
    max_pages: int = MAX_PDF_PAGES
    max_text_chars: int = MAX_PDF_TEXT_CHARS
    max_page_pixels: int = MAX_PAGE_PIXELS


@dataclass(frozen=True)
class DocumentPage:
    page_number: int
    text: str
    ocr: OcrResult | None = None
    selected_source: str = "none"
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class DocumentResult:
    media_type: str
    pages: tuple[DocumentPage, ...]
    extracted_text: str
    warnings: tuple[str, ...] = ()


def validate_file_bytes(data: bytes, limits: FileLimits | None = None) -> None:
    limits = limits or FileLimits()
    if not data:
        raise ValueError("empty file")
    if len(data) > limits.max_bytes:
        raise ValueError("file exceeds byte limit")


def _pdf_magic(data: bytes) -> bool:
    return data.startswith(b"%PDF-")


def _render_scale(page: Any, max_pixels: int) -> float:
    rect = page.rect
    base_pixels = max(1.0, float(rect.width) * float(rect.height))
    return min(2.5, max(1.0, (max_pixels / base_pixels) ** 0.5))


def _read_pdf(
    data: bytes, limits: FileLimits
) -> tuple[tuple[str, ...], tuple[bytes, ...]]:
    if not _pdf_magic(data):
        raise ValueError("invalid PDF signature")
    try:
        import pymupdf
        document = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:
        raise ValueError("PDF could not be opened") from exc

    try:
        if document.is_encrypted:
            raise ValueError("encrypted PDFs are not supported")
        if document.page_count < 1:
            raise ValueError("PDF has no pages")
        if document.page_count > limits.max_pages:
            raise ValueError("PDF exceeds page limit")

        texts: list[str] = []
        images: list[bytes] = []
        remaining = limits.max_text_chars

        for index in range(document.page_count):
            page = document.load_page(index)
            page_text = page.get_text("text") or ""
            clipped = page_text[:remaining]
            texts.append(clipped)
            remaining = max(0, remaining - len(clipped))

            scale = _render_scale(page, limits.max_page_pixels)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
            if pix.width * pix.height > limits.max_page_pixels:
                raise ValueError("PDF page exceeds pixel limit")
            images.append(pix.tobytes("png"))

        return tuple(texts), tuple(images)
    finally:
        document.close()


def _image_metadata(image: bytes) -> ImageMetadata:
    validate_image_bytes(image)
    try:
        with Image.open(BytesIO(image)) as decoded:
            metadata = ImageMetadata(decoded.width, decoded.height, len(decoded.getbands()))
    except Exception as exc:
        raise ValueError("image metadata could not be read") from exc
    validate_image_metadata(metadata)
    return metadata


def _strip_known_watermarks(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    kept = [line for line in lines if not any(pattern.fullmatch(line) for pattern in _SCANNER_WATERMARKS)]
    return "\n".join(kept).strip()


def _select_page_text(
    native_text: str, ocr: OcrResult | None
) -> tuple[str, str, tuple[str, ...]]:
    native = native_text.strip()
    content_text = _strip_known_watermarks(native)
    ocr_text = ocr.text.strip() if ocr else ""
    warnings: list[str] = []

    if content_text and len(content_text) >= MIN_NATIVE_TEXT_CHARS:
        return content_text, "pdf_text", tuple(warnings)

    if ocr_text and ocr is not None and ocr.confidence >= 0.60:
        if native:
            warnings.append("native_pdf_text_sparse_or_watermark")
        return ocr_text, "ocr", tuple(warnings)

    if content_text:
        warnings.append("native_pdf_text_sparse")
        if ocr is None:
            warnings.append("ocr_not_requested")
        elif not ocr_text:
            warnings.append("ocr_empty")
        elif ocr.confidence < 0.60:
            warnings.append("ocr_low_confidence")
        return content_text, "pdf_text_low_confidence", tuple(warnings)

    warnings.append("document_text_not_detected")
    if native:
        warnings.append("scanner_watermark_only")
    if ocr is None:
        warnings.append("ocr_not_requested")
    elif not ocr_text:
        warnings.append("ocr_empty")
    elif ocr.confidence < 0.60:
        warnings.append("ocr_low_confidence")
    return "", "none", tuple(warnings)


def inspect_document(
    data: bytes,
    filename: str,
    ocr_backend: OcrBackend | None = None,
    limits: FileLimits | None = None,
) -> DocumentResult:
    limits = limits or FileLimits()
    validate_file_bytes(data, limits)
    suffix = PurePosixPath(filename.lower()).suffix

    if suffix == ".pdf" or _pdf_magic(data):
        page_texts, page_images = _read_pdf(data, limits)
        pages: list[DocumentPage] = []
        warnings: list[str] = []
        selected_chunks: list[str] = []

        for number, image in enumerate(page_images, 1):
            page_text = page_texts[number - 1]
            ocr_result = None
            if ocr_backend is not None:
                metadata = _image_metadata(image)
                ocr_result = ocr_backend.recognize(image, metadata)

            selected, source, page_warnings = _select_page_text(page_text, ocr_result)
            if selected:
                selected_chunks.append(selected)
            pages.append(
                DocumentPage(
                    number,
                    page_text,
                    ocr_result,
                    source,
                    page_warnings,
                )
            )
            warnings.extend(page_warnings)

        extracted_text = "\n".join(selected_chunks)[: limits.max_text_chars].strip()
        if not extracted_text:
            warnings.append("document_text_not_detected")

        return DocumentResult(
            "application/pdf",
            tuple(pages),
            extracted_text,
            tuple(dict.fromkeys(warnings)),
        )

    metadata = _image_metadata(data)
    if ocr_backend is None:
        return DocumentResult(
            "image",
            (DocumentPage(1, "", None, "none", ("ocr_not_requested",)),),
            "",
            ("ocr_not_requested",),
        )

    ocr_result = ocr_backend.recognize(data, metadata)
    text = ocr_result.text.strip() if ocr_result.confidence >= 0.60 else ""
    warnings = ocr_result.warnings if text else (*ocr_result.warnings, "ocr_not_accepted")
    return DocumentResult(
        "image",
        (DocumentPage(1, "", ocr_result, "ocr" if text else "none", warnings),),
        text,
        tuple(dict.fromkeys(warnings)),
    )


def best_document_text(result: DocumentResult) -> str:
    chunks = [
        page.ocr.text.strip()
        if page.selected_source == "ocr" and page.ocr
        else page.text.strip()
        for page in result.pages
    ]
    return "\n".join(chunk for chunk in chunks if chunk)[:MAX_PDF_TEXT_CHARS]
