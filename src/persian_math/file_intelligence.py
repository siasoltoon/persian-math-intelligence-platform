from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath

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


@dataclass(frozen=True)
class DocumentResult:
    media_type: str
    pages: tuple[DocumentPage, ...]
    extracted_text: str
    warnings: tuple[str, ...] = ()


def validate_file_bytes(data: bytes, limits: FileLimits = FileLimits()) -> None:
    if not data:
        raise ValueError("empty file")
    if len(data) > limits.max_bytes:
        raise ValueError("file exceeds byte limit")


def _pdf_magic(data: bytes) -> bool:
    return data.startswith(b"%PDF-")


def _read_pdf(data: bytes, limits: FileLimits) -> tuple[tuple[str, ...], tuple[bytes, ...]]:
    if not _pdf_magic(data):
        raise ValueError("invalid PDF signature")
    try:
        import fitz
        document = fitz.open(stream=data, filetype="pdf")
    except Exception as exc:
        raise ValueError("PDF could not be opened") from exc
    try:
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
            remaining -= len(clipped)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            if pix.width * pix.height > limits.max_page_pixels:
                raise ValueError("PDF page exceeds pixel limit")
            images.append(pix.tobytes("png"))
        return tuple(texts), tuple(images)
    finally:
        document.close()


def inspect_document(
    data: bytes,
    filename: str,
    ocr_backend: OcrBackend | None = None,
    limits: FileLimits = FileLimits(),
) -> DocumentResult:
    validate_file_bytes(data, limits)
    suffix = PurePosixPath(filename.lower()).suffix
    if suffix == ".pdf" or _pdf_magic(data):
        page_texts, page_images = _read_pdf(data, limits)
        pages: list[DocumentPage] = []
        warnings: list[str] = []
        for number, image in enumerate(page_images, 1):
            page_text = page_texts[number - 1]
            ocr_result = None
            if ocr_backend is not None:
                with Image.open(BytesIO(image)) as decoded:
                    metadata = ImageMetadata(decoded.width, decoded.height, len(decoded.getbands()))
                validate_image_bytes(image)
                validate_image_metadata(metadata)
                ocr_result = ocr_backend.recognize(image, metadata)
            pages.append(DocumentPage(number, page_text, ocr_result))
        extracted_text = "\n".join(page_texts)[:limits.max_text_chars].strip()
        if not extracted_text and not any(p.ocr and p.ocr.text.strip() for p in pages):
            warnings.append("document_text_not_detected")
        return DocumentResult("application/pdf", tuple(pages), extracted_text, tuple(warnings))

    validate_image_bytes(data)
    with Image.open(BytesIO(data)) as decoded:
        metadata = ImageMetadata(decoded.width, decoded.height, len(decoded.getbands()))
    validate_image_metadata(metadata)
    if ocr_backend is None:
        return DocumentResult("image", (DocumentPage(1, ""),), "", ("ocr_not_requested",))
    ocr_result = ocr_backend.recognize(data, metadata)
    return DocumentResult("image", (DocumentPage(1, "", ocr_result),), ocr_result.text, ocr_result.warnings)


def best_document_text(result: DocumentResult) -> str:
    chunks: list[str] = []
    if result.extracted_text.strip():
        chunks.append(result.extracted_text.strip())
    for page in result.pages:
        if page.ocr and page.ocr.text.strip():
            chunks.append(page.ocr.text.strip())
    return "\n".join(chunks)[:MAX_PDF_TEXT_CHARS]
