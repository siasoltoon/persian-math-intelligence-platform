from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .ocr import ImageMetadata, OcrBackend, OcrResult


class HandwritingRecognitionBackend(Protocol):
    """Optional handwriting/math recognizer.

    Implementations may wrap a local or remote recognizer. The core never
    assumes that an unavailable backend produced a guess.
    """

    def recognize_handwriting(self, image: bytes, metadata: ImageMetadata) -> OcrResult: ...


@dataclass(frozen=True)
class BackendResult:
    name: str
    result: OcrResult


class CompositeOcrBackend:
    """Run heterogeneous OCR backends and accept only corroborated output."""

    def __init__(
        self,
        primary: OcrBackend,
        handwriting: HandwritingRecognitionBackend | None = None,
    ) -> None:
        self.primary = primary
        self.handwriting = handwriting

    def recognize(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        primary = self.primary.recognize(image, metadata)
        if self.handwriting is None:
            return primary
        secondary = self.handwriting.recognize_handwriting(image, metadata)
        if not secondary.text.strip():
            return primary
        if not primary.text.strip():
            return OcrResult(
                secondary.text,
                secondary.confidence,
                secondary.regions,
                (*secondary.warnings, "handwriting_backend_only"),
            )
        from .ocr_consensus import RecognitionCandidate, consensus

        agreement = consensus((
            RecognitionCandidate(primary.text, primary.confidence, "primary"),
            RecognitionCandidate(secondary.text, secondary.confidence, "handwriting"),
        ), threshold=0.78)
        if not agreement.accepted:
            return OcrResult(
                "",
                agreement.confidence,
                (),
                ("ocr_backend_disagreement", "ocr_low_confidence"),
            )
        return OcrResult(
            agreement.text,
            agreement.confidence,
            primary.regions or secondary.regions,
            tuple(dict.fromkeys((*primary.warnings, *secondary.warnings))),
        )
