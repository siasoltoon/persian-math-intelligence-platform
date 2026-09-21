from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import os
from typing import Any

import cv2
import numpy as np
from PIL import Image

from .ocr import ImageMetadata, OcrResult, validate_image_bytes, validate_image_metadata


@dataclass(frozen=True)
class RecognitionConfig:
    model_id: str
    device: str = "auto"
    local_files_only: bool = True
    max_new_tokens: int = 256


def _line_images(image: bytes) -> tuple[Image.Image, ...]:
    validate_image_bytes(image)
    with Image.open(BytesIO(image)) as source:
        gray = np.asarray(source.convert("L"), dtype=np.uint8)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    horizontal = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (max(15, gray.shape[1] // 30), 3)),
    )
    contours, _ = cv2.findContours(horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    height = gray.shape[0]
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w >= max(24, gray.shape[1] // 25) and h >= 8:
            boxes.append((x, y, w, h))
    if not boxes:
        return (Image.fromarray(gray).convert("RGB"),)
    boxes.sort(key=lambda box: box[1])
    crops: list[Image.Image] = []
    for x, y, w, h in boxes:
        pad_x = max(8, w // 50)
        pad_y = max(8, h // 3)
        crop = gray[
            max(0, y - pad_y) : min(height, y + h + pad_y),
            max(0, x - pad_x) : min(gray.shape[1], x + w + pad_x),
        ]
        crops.append(Image.fromarray(crop).convert("RGB"))
    return tuple(crops)


class TrOCRHandwritingBackend:
    """Optional concrete handwriting backend using Microsoft's handwritten TrOCR."""

    def __init__(
        self,
        model_id: str = "microsoft/trocr-base-handwritten",
        device: str = "auto",
        local_files_only: bool = True,
    ) -> None:
        self.config = RecognitionConfig(model_id, device, local_files_only)
        self._processor: Any | None = None
        self._model: Any | None = None

    def _load(self) -> tuple[Any, Any]:
        if self._processor is not None and self._model is not None:
            return self._processor, self._model
        try:
            from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        except ImportError as exc:
            raise RuntimeError("handwriting OCR dependencies are not installed") from exc
        processor = TrOCRProcessor.from_pretrained(
            self.config.model_id, local_files_only=self.config.local_files_only
        )
        model = VisionEncoderDecoderModel.from_pretrained(
            self.config.model_id, local_files_only=self.config.local_files_only
        )
        if self.config.device != "auto":
            model = model.to(self.config.device)
        model.eval()
        self._processor, self._model = processor, model
        return processor, model

    def recognize_handwriting(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        validate_image_metadata(metadata)
        validate_image_bytes(image)
        try:
            processor, model = self._load()
            import torch

            lines = _line_images(image)
            texts: list[str] = []
            for line in lines:
                pixel_values = processor(images=line, return_tensors="pt").pixel_values
                if self.config.device != "auto":
                    pixel_values = pixel_values.to(self.config.device)
                with torch.inference_mode():
                    ids = model.generate(pixel_values, max_new_tokens=self.config.max_new_tokens)
                text = processor.batch_decode(ids, skip_special_tokens=True)[0].strip()
                if text:
                    texts.append(text)
        except (RuntimeError, OSError, ValueError, TypeError) as exc:
            return OcrResult("", 0.0, (), ("handwriting_backend_unavailable", str(exc)))
        if not texts:
            return OcrResult("", 0.0, (), ("handwriting_no_text",))
        return OcrResult("\n".join(texts), 0.70, (), ("handwriting_model_trocr",))


class Pix2TexMathBackend:
    """Optional concrete formula-image backend returning LaTeX from pix2tex."""

    def __init__(self) -> None:
        self._recognizer: Any | None = None

    def _load(self) -> Any:
        if self._recognizer is not None:
            return self._recognizer
        try:
            from pix2tex.cli import LatexOCR
        except ImportError as exc:
            raise RuntimeError("pix2tex is not installed") from exc
        self._recognizer = LatexOCR()
        return self._recognizer

    def recognize_math(self, image: bytes, metadata: ImageMetadata) -> OcrResult:
        validate_image_metadata(metadata)
        validate_image_bytes(image)
        try:
            with Image.open(BytesIO(image)) as source:
                formula = str(self._load()(source.convert("RGB"))).strip()
        except (RuntimeError, OSError, ValueError, TypeError) as exc:
            return OcrResult("", 0.0, (), ("math_formula_backend_unavailable", str(exc)))
        if not formula:
            return OcrResult("", 0.0, (), ("math_formula_no_text",))
        return OcrResult(formula, 0.78, (), ("math_model_pix2tex",))


class EnvironmentConfiguredHandwritingBackend(TrOCRHandwritingBackend):
    """Construct a TrOCR backend from environment without hard-coded secrets."""

    @classmethod
    def from_environment(cls) -> "EnvironmentConfiguredHandwritingBackend":
        return cls(
            model_id=os.getenv("MATH_HANDWRITING_MODEL", "microsoft/trocr-base-handwritten"),
            device=os.getenv("MATH_HANDWRITING_DEVICE", "auto"),
            local_files_only=os.getenv("MATH_HANDWRITING_LOCAL_ONLY", "1") != "0",
        )
