from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Protocol

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from .canonical import normalize_math_text


class ImageQuality(str, Enum):
    UNKNOWN = "unknown"
    POOR = "poor"
    ACCEPTABLE = "acceptable"
    GOOD = "good"


@dataclass(frozen=True)
class ImageMetadata:
    width: int
    height: int
    channels: int = 1
    quality: ImageQuality = ImageQuality.UNKNOWN


@dataclass(frozen=True)
class OcrRegion:
    text: str
    confidence: float
    bbox: tuple[int, int, int, int]
    kind: str = "math"


@dataclass(frozen=True)
class OcrResult:
    text: str
    confidence: float
    regions: tuple[OcrRegion, ...]
    warnings: tuple[str, ...] = ()


class OcrBackend(Protocol):
    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult: ...


def validate_image_metadata(metadata: ImageMetadata) -> None:
    if metadata.width <= 0 or metadata.height <= 0:
        raise ValueError("invalid image dimensions")
    if metadata.channels not in (1, 3, 4):
        raise ValueError("unsupported image channels")
    if metadata.width * metadata.height > 40_000_000:
        raise ValueError("image exceeds resource limit")


def preprocess_plan(metadata: ImageMetadata) -> tuple[str, ...]:
    validate_image_metadata(metadata)
    plan = [
        "decode",
        "orientation_check",
        "deskew",
        "scale_up",
        "contrast_normalization",
    ]
    if metadata.quality in (ImageQuality.POOR, ImageQuality.UNKNOWN):
        plan.extend(("denoise", "adaptive_threshold"))
    plan.extend(("multi_pass_ocr", "region_detection", "math_text_segmentation", "consensus"))
    return tuple(plan)


class UnavailableOcrBackend:
    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        validate_image_metadata(metadata)
        return OcrResult("", 0.0, (), ("ocr_backend_unavailable",))


MAX_IMAGE_BYTES = 12 * 1024 * 1024


def validate_image_bytes(image: bytes) -> None:
    if not image:
        raise ValueError("empty image")
    if len(image) > MAX_IMAGE_BYTES:
        raise ValueError("image exceeds byte limit")
    try:
        with Image.open(BytesIO(image)) as decoded:
            decoded.verify()
    except Exception as exc:
        raise ValueError("invalid image data") from exc


def _variants(decoded: Image.Image) -> tuple[Image.Image, ...]:
    base = ImageOps.exif_transpose(decoded).convert("L")
    scale = max(1.0, min(2.5, 1800 / max(base.width, base.height)))
    if scale > 1:
        base = base.resize((int(base.width * scale), int(base.height * scale)))
    contrast = ImageEnhance.Contrast(base).enhance(1.8)
    sharp = contrast.filter(ImageFilter.SHARPEN)
    threshold = sharp.point(lambda p: 255 if p > 175 else 0)
    return (base, contrast, sharp, threshold)


def preprocess_image(image: bytes, metadata: ImageMetadata) -> bytes:
    validate_image_metadata(metadata)
    validate_image_bytes(image)
    try:
        with Image.open(BytesIO(image)) as decoded:
            prepared = _variants(decoded)[1]
            output = BytesIO()
            prepared.save(output, format="PNG", optimize=True)
            return output.getvalue()
    except Exception as exc:
        raise ValueError("image preprocessing failed") from exc


def validate_ocr_result(result: OcrResult, metadata: ImageMetadata) -> None:
    validate_image_metadata(metadata)
    if not 0.0 <= result.confidence <= 1.0:
        raise ValueError("invalid OCR confidence")
    for region in result.regions:
        if not 0.0 <= region.confidence <= 1.0:
            raise ValueError("invalid OCR region confidence")
        x, y, width, height = region.bbox
        if x < 0 or y < 0 or width < 0 or height < 0:
            raise ValueError("invalid OCR bounding box")
        if x + width > metadata.width or y + height > metadata.height:
            raise ValueError("OCR bounding box outside image")


def reconstruct_math_text(result: OcrResult, metadata: ImageMetadata) -> str:
    validate_ocr_result(result, metadata)
    ordered = sorted(result.regions, key=lambda r: (r.bbox[1], r.bbox[0]))
    return normalize_math_text("\n".join(r.text.strip() for r in ordered if r.text.strip()))


class TesseractOcrBackend:
    def __init__(self, language: str = "eng") -> None:
        self.language = language

    def _recognize_variant(self, image: Image.Image, psm: int) -> OcrResult:
        data = pytesseract.image_to_data(
            image,
            lang=self.language,
            config=f"--psm {psm}",
            output_type=pytesseract.Output.DICT,
        )
        regions = []
        confidences = []
        for i, raw_text in enumerate(data.get("text", [])):
            text = raw_text.strip()
            try:
                confidence = max(0.0, min(1.0, float(data["conf"][i]) / 100.0))
                bbox = (
                    int(data["left"][i]),
                    int(data["top"][i]),
                    int(data["width"][i]),
                    int(data["height"][i]),
                )
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            if text:
                regions.append(OcrRegion(text, confidence, bbox, "text"))
                confidences.append(confidence)
        return OcrResult(
            " ".join(r.text for r in regions),
            sum(confidences) / len(confidences) if confidences else 0.0,
            tuple(regions),
        )

    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        validate_image_metadata(metadata)
        validate_image_bytes(image)
        try:
            with Image.open(BytesIO(image)) as decoded:
                candidates = []
                for variant in _variants(decoded):
                    for psm in (6, 11, 12):
                        try:
                            candidates.append(self._recognize_variant(variant, psm))
                        except Exception:
                            continue
        except Exception as exc:
            raise RuntimeError("OCR backend unavailable or failed") from exc
        if not candidates:
            return OcrResult("", 0.0, (), ("ocr_no_candidate",))
        candidates.sort(key=lambda r: (r.confidence, len(r.text)), reverse=True)
        best = candidates[0]
        warnings = ("ocr_low_confidence",) if best.confidence < 0.60 else ()
        result = OcrResult(best.text, best.confidence, best.regions, warnings)
        validate_ocr_result(result, metadata)
        return result
