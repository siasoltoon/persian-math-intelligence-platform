from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Any, Protocol

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageOps

from .canonical import normalize_math_text
from .ocr_consensus import RecognitionCandidate, consensus


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


def estimate_image_quality(image: bytes) -> ImageQuality:
    """Classify source quality from measurable sharpness/contrast signals."""
    validate_image_bytes(image)
    with Image.open(BytesIO(image)) as decoded:
        gray = np.asarray(ImageOps.exif_transpose(decoded).convert("L"), dtype=np.uint8)
    variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    contrast = float(gray.std())
    if variance < 45 or contrast < 18:
        return ImageQuality.POOR
    if variance < 110 or contrast < 28:
        return ImageQuality.ACCEPTABLE
    return ImageQuality.GOOD


def preprocess_plan(metadata: ImageMetadata) -> tuple[str, ...]:
    validate_image_metadata(metadata)
    plan = [
        "decode",
        "orientation_check",
        "deskew",
        "scale_up",
        "contrast_normalization",
        "border_cleanup",
    ]
    if metadata.quality in (ImageQuality.POOR, ImageQuality.UNKNOWN):
        plan.extend(("denoise", "adaptive_threshold"))
    plan.extend(
        (
            "multi_pass_ocr",
            "line_reconstruction",
            "math_text_segmentation",
            "fraction_detection",
            "superscript_subscript_detection",
            "matrix_layout_detection",
            "consensus",
        )
    )
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


def _deskew(gray: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]:
    mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    points = cv2.findNonZero(mask)
    if points is None or len(points) < 20:
        return gray
    angle = cv2.minAreaRect(points)[-1]
    if angle < -45:
        angle = 90 + angle
    if abs(angle) < 0.7:
        return gray
    h, w = gray.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(
        gray, matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )


def _crop_content(gray: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]:
    mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    coords = cv2.findNonZero(mask)
    if coords is None:
        return gray
    x, y, w, h = cv2.boundingRect(coords)
    pad = max(12, int(0.025 * max(w, h)))
    return gray[
        max(0, y - pad) : min(gray.shape[0], y + h + pad),
        max(0, x - pad) : min(gray.shape[1], x + w + pad),
    ]


def _variants(decoded: Image.Image) -> tuple[Image.Image, ...]:
    gray = np.asarray(ImageOps.exif_transpose(decoded).convert("L"), dtype=np.uint8)
    if max(gray.shape) < 1800:
        scale = min(3.0, 2200 / max(gray.shape))
        gray = np.asarray(
            cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC),
            dtype=np.uint8,
        )
    gray = _crop_content(_deskew(gray))
    denoised = cv2.fastNlMeansDenoising(gray, None, 7, 7, 21)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8)).apply(denoised)
    normalized = np.asarray(
        cv2.normalize(clahe, None, 0, 255, cv2.NORM_MINMAX),  # type: ignore[call-overload]
        dtype=np.uint8,
    )
    smooth = cv2.GaussianBlur(normalized, (3, 3), 0)
    unsharp = cv2.addWeighted(normalized, 1.65, smooth, -0.65, 0)
    adaptive = cv2.adaptiveThreshold(
        unsharp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 9
    )
    otsu = cv2.threshold(unsharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closed = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel, iterations=1)
    return tuple(
        Image.fromarray(item) for item in (gray, normalized, unsharp, adaptive, closed, otsu)
    )


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


def _reconstruct_regions(regions: tuple[OcrRegion, ...]) -> str:
    ordered = sorted(regions, key=lambda r: (r.bbox[1], r.bbox[0]))
    if not ordered:
        return ""

    lines: list[list[OcrRegion]] = []
    for region in ordered:
        _, y, _, height = region.bbox
        center = y + height / 2
        target: list[OcrRegion] | None = None
        for line in reversed(lines[-3:]):
            ref = line[-1]
            ref_center = ref.bbox[1] + ref.bbox[3] / 2
            ref_height = max(1, ref.bbox[3])
            if abs(center - ref_center) <= max(height, ref_height) * 0.60:
                target = line
                break
        if target is None:
            lines.append([region])
        else:
            target.append(region)

    rendered: list[str] = []
    for line in lines:
        line.sort(key=lambda r: r.bbox[0])
        tokens: list[str] = []
        baseline = max(r.bbox[1] + r.bbox[3] for r in line)
        median_height = sorted(max(1, r.bbox[3]) for r in line)[len(line) // 2]
        previous_right: int | None = None
        for region in line:
            token = region.text.strip()
            if not token:
                continue
            top = region.bbox[1]
            if top + region.bbox[3] < baseline - 0.35 * median_height and tokens:
                tokens[-1] = f"{tokens[-1]}**{token}"
            elif previous_right is not None and region.bbox[0] > previous_right + 8:
                tokens.append(" " + token)
            else:
                tokens.append(token)
            previous_right = region.bbox[0] + region.bbox[2]
        rendered.append("".join(tokens).strip())
    return "\n".join(rendered)


def reconstruct_math_text(result: OcrResult, metadata: ImageMetadata) -> str:
    validate_ocr_result(result, metadata)
    if result.confidence < 0.60 or not result.regions:
        return ""
    return normalize_math_text(_reconstruct_regions(result.regions))


class TesseractOcrBackend:
    def __init__(self, language: str = "fas+eng") -> None:
        self.language = language.strip() or "fas+eng"

    def _language(self) -> str:
        try:
            available = set(pytesseract.get_languages(config=""))
        except (RuntimeError, OSError):
            return self.language
        requested = tuple(part for part in self.language.split("+") if part)
        if requested and all(part in available for part in requested):
            return self.language
        if "eng" in available:
            return "eng"
        return requested[0] if requested and requested[0] in available else "eng"

    def _recognize_variant(self, image: Image.Image, psm: int) -> OcrResult:
        data = pytesseract.image_to_data(
            image,
            lang=self._language(),
            config=f"--oem 1 --psm {psm}",
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
            if text and confidence > 0.05:
                regions.append(OcrRegion(text, confidence, bbox, "text"))
                confidences.append(confidence)
        regions_tuple = tuple(regions)
        return OcrResult(
            _reconstruct_regions(regions_tuple),
            sum(confidences) / len(confidences) if confidences else 0.0,
            regions_tuple,
        )

    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        validate_image_metadata(metadata)
        validate_image_bytes(image)
        try:
            with Image.open(BytesIO(image)) as decoded:
                candidates: list[OcrResult] = []
                for variant in _variants(decoded):
                    for psm in (3, 4, 6, 11, 12, 13):
                        try:
                            candidates.append(self._recognize_variant(variant, psm))
                        except (RuntimeError, ValueError, TypeError, OSError):
                            continue
        except Exception as exc:
            raise RuntimeError("OCR backend unavailable or failed") from exc
        if not candidates:
            return OcrResult("", 0.0, (), ("ocr_no_candidate",))

        ranked = sorted(candidates, key=lambda r: (r.confidence, len(r.text)), reverse=True)
        source_quality = estimate_image_quality(image)
        quality_warning = (
            ("source_image_poor_quality",) if source_quality == ImageQuality.POOR else ()
        )
        candidate_set = tuple(
            RecognitionCandidate(item.text, item.confidence, f"pass-{index}")
            for index, item in enumerate(ranked)
        )
        agreement = consensus(candidate_set)
        best = ranked[0]
        if agreement.accepted:
            confidence = min(1.0, max(best.confidence, agreement.confidence))
            warnings: tuple[str, ...] = (
                ("ocr_low_confidence",) if confidence < 0.60 else ()
            ) + quality_warning
        else:
            confidence = min(best.confidence, agreement.confidence)
            warnings = ("ocr_disagreement", "ocr_low_confidence") + quality_warning
        result = OcrResult(
            agreement.text if agreement.accepted else "",
            confidence,
            best.regions,
            warnings,
        )
        validate_ocr_result(result, metadata)
        return result
