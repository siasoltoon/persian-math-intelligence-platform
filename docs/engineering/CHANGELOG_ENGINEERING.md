# Engineering Changelog

## 2026-09-21 — Extreme degradation OCR hardening
- Added OpenCV-based image recovery before recognition: deskew, content cropping, bounded upscaling, denoising, CLAHE, normalization, unsharp recovery, adaptive/OTSU thresholding and morphology.
- Expanded preprocessing to six variants and widened Tesseract page-segmentation coverage.
- Added poor-source quality signaling and regression coverage for degraded input.
- Preserved confidence/consensus gating so uncertain recognition is rejected rather than guessed.
- Added strict NumPy/OpenCV typing fixes required by mypy.
- CI #290 / run ID 35639811372 passed Ruff lint, Ruff format, mypy and pytest on Python 3.11/3.12.
- Merged PR #7 to main as `dc7d37367fc1d4cb0e3ce7d8a9ff63fa80e72f11`.
- Real labeled handwriting benchmark evidence and a handwriting-specific recognition backend remain pending.

## 2026-09-21 — Production document/OCR and verification hardening
- Replaced deprecated `fitz` document imports with `pymupdf`.
- Added adaptive PDF page rendering constrained by a pixel budget.
- Added encrypted-PDF rejection.
- Added page-level native-text versus OCR source selection for scanned and mixed PDFs.
- Added explicit handling for scanner-watermark-only text such as `Scanned by CamScanner`.
- Added confidence-gated image/document OCR and no-guess rejection behavior.
- Strengthened OCR reconstruction with line ordering and layout-aware superscript handling.
- Defaulted the Telegram OCR language to `fas+eng` with runtime fallback to available Tesseract languages.
- Hardened SymPy parsing with bounded input, a restricted grammar and disabled builtins.
- Strengthened mathematical verification with deterministic numeric re-evaluation and an alternate `solveset` equation path.
- Added regression tests for scanned-like PDFs, low-confidence OCR, parser injection/resource bounds and verification.
- Live OCR corpus, live Telegram/VPS execution, production load and operational evidence remain pending.

## 2026-09-21 — Secure document and OCR hardening
- Added bounded multi-format document inspection for PDF and image documents.
- Preserved native PDF text per page instead of using incorrect global-line indexing.
- Added PDF byte/page/pixel/text resource limits and real PDF regression tests.
- Added multi-pass OCR preprocessing with scaling, contrast, sharpening and threshold variants.
- Added OCR consensus gating so disagreeing recognition passes are rejected instead of guessed.
- Narrowed recoverable per-pass OCR exceptions and fixed static type checking.
- Live OCR/PDF benchmark evidence remains pending.

## 2026-09-21 — Interactive Telegram UI
- Added persistent Persian-first main keyboard.
- Added callback-driven solve, exercise, profile, history, settings and help navigation.
- Added exercise topic and difficulty selection.
- Added educational-level selection.
- Added /menu and safe back navigation.
- Added dedicated application-service regression coverage.
- Live Telegram/mobile verification remains pending.

## 2026-09-21 — Phase 19–25 hardening batch
- Added quality/failure matrix and bounded retry contracts.
- Added OCR benchmark metrics for character/expression/structure accuracy.
- Added adversarial mathematical input coverage.
- Added Persian-first RTL answer rendering policy.
- Added production configuration/resource/recovery contracts.
- Added release-audit gate and production verification runbook.
- Added P19–P25 acceptance tests.
- No external production/OCR/load/security evidence has been fabricated.

## 2026-09-21 — Windows VPS / Telegram runtime integration
- Added `vps/` runtime reference and a secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing ApplicationService.
- Added photo OCR handling with validation and confidence gating.
- Added Telegram runtime dependency and configuration tests.
- Added explicit security and operational limitations to engineering state.
