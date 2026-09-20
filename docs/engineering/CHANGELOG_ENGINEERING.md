# Engineering Changelog

## 2026-09-21

### Phase 1–10 completion and verification
- Expanded the typed domain with entrance-exam educational level.
- Expanded canonical parsing to fractions, vectors, functions, derivatives, integrals, limits, series and probability.
- Added independent equation verification against an independently executed solver path.
- Added bounded image byte validation and actual image preprocessing.
- Integrated a concrete Tesseract OCR backend with validated regions/confidence.
- Added OCR retry recommendation and Persian clarification contract.
- Expanded geometry with segment intersection.
- Added structured visual mathematics scene representation for graph axes, points and series.
- Expanded Persian explanation output with notes and common-mistake guidance.
- Expanded educational curriculum/objectives across all Phase 10 levels.
- Added phase acceptance/regression tests covering Phases 1–10.
- CI is GREEN on the final source validation workflow.

### CI evidence
- Successful workflow run: 35545050264
- Source commit: a79306d22da0555440c4ad4c5c1c4f0bf87e2a6b
- Gates: Ruff lint, Ruff format, mypy, pytest 3.11 and pytest 3.12 all PASS.
