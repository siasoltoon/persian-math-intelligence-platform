from __future__ import annotations

import builtins
from io import BytesIO

from PIL import Image

from persian_math.ocr import ImageMetadata


def test_environment_backend_defaults_to_local_model():
    from persian_math.specialized_ocr import EnvironmentConfiguredHandwritingBackend

    backend = EnvironmentConfiguredHandwritingBackend.from_environment()
    assert backend.config.model_id == "microsoft/trocr-base-handwritten"
    assert backend.config.local_files_only is True


def _image_bytes() -> bytes:
    output = BytesIO()
    Image.new("L", (100, 100), 255).save(output, format="PNG")
    return output.getvalue()


def test_trocr_backend_missing_dependency_is_safe(monkeypatch):
    real_import = builtins.__import__

    def blocked(name, *args, **kwargs):
        if name == "transformers":
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked)
    from persian_math.specialized_ocr import TrOCRHandwritingBackend

    result = TrOCRHandwritingBackend().recognize_handwriting(
        _image_bytes(), ImageMetadata(100, 100)
    )
    assert result.text == ""


def test_pix2tex_backend_missing_dependency_is_safe(monkeypatch):
    real_import = builtins.__import__

    def blocked(name, *args, **kwargs):
        if name == "pix2tex.cli":
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked)
    from persian_math.specialized_ocr import Pix2TexMathBackend

    result = Pix2TexMathBackend().recognize_math(_image_bytes(), ImageMetadata(100, 100))
    assert result.text == ""


def test_specialized_module_has_lazy_backends():
    import persian_math.specialized_ocr as module

    assert hasattr(module, "TrOCRHandwritingBackend")
    assert hasattr(module, "Pix2TexMathBackend")


def test_formula_validator_rejects_unsafe_latex():
    from persian_math.specialized_ocr import validate_latex_formula

    try:
        validate_latex_formula(r"\write18{rm -rf /}")
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe LaTeX command was accepted")


def test_formula_consensus_rejects_conflicting_predictions():
    from persian_math.specialized_ocr import CompositeMathFormulaBackend

    class A:
        def recognize_math(self, image, metadata):
            return type("R", (), {"text": r"x^2+1", "confidence": 0.95})()

    class B:
        def recognize_math(self, image, metadata):
            return type("R", (), {"text": r"x^2-1", "confidence": 0.95})()

    result = CompositeMathFormulaBackend((A(), B())).recognize_math(
        _image_bytes(), ImageMetadata(100, 100)
    )
    assert result.text == ""
    assert "math_formula_disagreement" in result.warnings


def test_formula_consensus_accepts_matching_predictions():
    from persian_math.specialized_ocr import CompositeMathFormulaBackend

    class A:
        def recognize_math(self, image, metadata):
            return type("R", (), {"text": r"\frac{x+1}{2}", "confidence": 0.95})()

    class B:
        def recognize_math(self, image, metadata):
            return type("R", (), {"text": r"\frac{x+1}{2}", "confidence": 0.94})()

    result = CompositeMathFormulaBackend((A(), B())).recognize_math(
        _image_bytes(), ImageMetadata(100, 100)
    )
    assert result.text == r"\frac{x+1}{2}"
