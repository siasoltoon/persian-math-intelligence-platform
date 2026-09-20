from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


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
    plan = ["decode", "orientation_check", "deskew", "contrast_normalization"]
    if metadata.quality in (ImageQuality.POOR, ImageQuality.UNKNOWN):
        plan.extend(("denoise", "adaptive_threshold"))
    plan.extend(("region_detection", "math_text_segmentation"))
    return tuple(plan)


class UnavailableOcrBackend:
    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        validate_image_metadata(metadata)
        return OcrResult("", 0.0, (), ("ocr_backend_unavailable",))
