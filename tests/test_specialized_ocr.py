from __future__ import annotations

import builtins

from persian_math.ocr import ImageMetadata


def test_environment_backend_defaults_to_local_model():
    from persian_math.specialized_ocr import EnvironmentConfiguredHandwritingBackend

    backend = EnvironmentConfiguredHandwritingBackend.from_environment()
    assert backend.config.model_id == "microsoft/trocr-base-handwritten"
    assert backend.config.local_files_only is True


def test_trocr_backend_missing_dependency_is_safe(monkeypatch):
    real_import = builtins.__import__

    def blocked(name, *args, **kwargs):
        if name == "transformers":
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked)
    from persian_math.specialized_ocr import TrOCRHandwritingBackend

    result = TrOCRHandwritingBackend().recognize_handwriting(
        b"not-an-image", ImageMetadata(100, 100)
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

    result = Pix2TexMathBackend().recognize_math(
        b"not-an-image", ImageMetadata(100, 100)
    )
    assert result.text == ""


def test_specialized_module_has_lazy_backends():
    import persian_math.specialized_ocr as module

    assert hasattr(module, "TrOCRHandwritingBackend")
    assert hasattr(module, "Pix2TexMathBackend")
