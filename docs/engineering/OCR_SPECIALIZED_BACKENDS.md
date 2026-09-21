# Specialized OCR Backends

The visual-input layer now has concrete optional backends for difficult handwriting and mathematical formula images.

## Handwriting

TrOCRHandwritingBackend integrates Microsoft's microsoft/trocr-base-handwritten through Transformers. The adapter segments pages into text-line crops before inference and loads the model lazily.

Production defaults:
- local_files_only=true
- no implicit model download
- bounded image validation
- backend failure returns an explicit unavailable result
- downstream consensus remains mandatory

Environment:
- MATH_HANDWRITING_MODEL
- MATH_HANDWRITING_DEVICE
- MATH_HANDWRITING_LOCAL_ONLY=1

The model is an HTR backend for handwritten text lines, not a guarantee of arbitrary Persian or mathematical handwriting accuracy. Real benchmark evidence is required.

## Mathematical formulas

Pix2TexMathBackend integrates pix2tex for image-to-LaTeX formula recognition. It is optional and lazy-loaded.

Formula output must still pass mathematical parsing and independent verification before solver use.

## Deployment

Keep heavyweight dependencies and model weights outside the core installation and preferably pre-cache them on the dedicated compute worker. The core repository must remain functional when optional backends are absent.

A backend is not production-verified until a labeled benchmark is executed.
