## VPS / Telegram runtime integration

### VPS-T01 — Windows runtime integration
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: bring the operational behavior of `siasoltoon/vps` into the math repository without propagating its committed credential.
- Acceptance: Windows runner provisions RDP/Tailscale, installs Python/Tesseract, validates secrets and starts the Telegram process.
- Tests: runtime configuration tests; repository CI green.
- Live evidence: pending.

### VPS-T02 — Telegram execution adapter
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: run the existing ApplicationService through a real Telegram polling adapter.
- Acceptance: /start, /help, text problems and validated photo OCR reach the application service and return Persian responses without raw exceptions.
- Tests: runtime configuration and regression suite; repository CI green.
- Live evidence: pending.

### TUI-T01 — Interactive Telegram UI
- Status: COMPLETED / VERIFICATION PENDING
- Phase: 23 — UX POLISH
- Objective: provide a production-oriented Persian-first Telegram interaction surface over the existing application service.
- Implemented: persistent main keyboard; solve flow; exercise domain/difficulty flow; profile/level; history; settings; help; /menu; callback routing; safe user-facing failures.
- Tests: dedicated `tests/test_telegram_ui.py`.
- Live validation: pending Telegram/mobile visual and interaction evidence.

### FILE-T01 — Secure document intelligence
- Status: IMPLEMENTED / VERIFICATION PENDING
- Phase: 21/22/24
- Objective: extend the Telegram input layer from plain text/photos to bounded PDF and document processing without unsafe execution.
- Implemented: PDF signature validation, encrypted-PDF rejection, byte/page/pixel/text limits, adaptive page rendering, per-page text preservation, automatic OCR for sparse/scanned pages, page-level source selection, scanner-watermark handling, image-file handling, unified document result model, configurable Tesseract language.
- OCR hardening: multi-pass image variants, line/region reconstruction, confidence gating and consensus rejection; disagreement is rejected rather than guessed.
- Mathematical hardening: bounded/safe parser input and stronger independent verification.
- Tests: `tests/test_file_intelligence.py`, `tests/test_canonical.py`, `tests/test_solver_verification.py` plus OCR/consensus regression suites.
- Pending: live multi-page PDF, scanned-PDF, mixed text/image PDF, difficult handwriting corpus and malformed/adversarial external evidence.

### OCR-T02 — Extreme degradation and handwriting robustness
- Status: COMPLETED / VERIFICATION PENDING
- Phase: 21/22
- Objective: improve the visual-input path before recognition so degraded and handwritten mathematical input has more recoverable signal while preserving no-guess behavior.
- Implemented: OpenCV preprocessing, deskew, content crop, bounded upscaling, denoising, CLAHE, normalization, unsharp recovery, adaptive/OTSU thresholding, morphology, bilateral and inverted recovery variants, expanded Tesseract PSM coverage, source-quality warning and regression tests.
- Added structural math OCR: fraction relationships, superscript/subscript relationships, matrix/table-like layout detection and mixed text/math classification.
- Added pluggable handwriting-recognition contract and strict composite consensus gate.
- Validation: PR #8 CI #304 / run 35643936787 green on Python 3.11/3.12; main CI #305 / run 35644040284 green.
- Remaining: real labeled handwriting corpus and a concrete handwriting-specific recognition backend are required before claiming production handwriting accuracy.

### OCR-T03 — Structural math OCR and handwriting backend contract
- Status: COMPLETED / VERIFICATION PENDING
- Phase: 21/22
- Objective: strengthen recognition beyond generic OCR by preserving mathematical spatial structure and allowing a specialized handwriting recognizer without weakening no-guess safety.
- Implemented: `math_ocr.py`, `ocr_backends.py`, structural regression suite and expanded image recovery/PSM coverage.
- Acceptance evidence: PR #8 merged; PR CI #304 green; main CI #305 green.
- Remaining: real specialized handwriting recognizer + labeled benchmark corpus + live Telegram evidence.

## Phase 19–25 hardening batch
- P19–P24: IMPLEMENTED / VERIFICATION PENDING
- P25: IMPLEMENTED / BLOCKED by required external evidence

### OCR-T04 — Specialized handwriting and formula recognition backends
- Status: COMPLETED / VERIFICATION PENDING
- Phase: 21/22
- Objective: move beyond generic OCR by providing concrete specialized recognition implementations while preserving strict no-guess behavior.
- Implemented: TrOCR handwritten backend, line segmentation, pix2tex formula backend, safe LaTeX validation, multi-backend formula consensus, lazy model loading and local-only defaults.
- Tests: specialized backend regression suite; CI run #315 green on Python 3.11/3.12.
- Remaining: real model artifact deployment, labeled benchmark corpus, live Telegram E2E and production performance evidence.


### OCR-T05 — GitHub-hosted heavy OCR worker
- Status: IMPLEMENTED / VERIFICATION PENDING
- Phase: 21/24
- Objective: temporarily execute heavyweight OCR/model runtime on GitHub Actions until the future PC worker is introduced.
- Implemented: isolated heavy dependency manifest, Hugging Face model cache, Tesseract provisioning, TrOCR prefetch, pix2tex import smoke test and full regression execution.
- Remaining: successful workflow execution evidence and real labeled model-accuracy benchmark.


### OCR-T05 — GitHub-hosted heavy OCR worker
- Status: VERIFIED for runtime integration / accuracy verification pending
- Phase: 21/24
- Objective: temporarily execute heavyweight OCR/model runtime on GitHub Actions until the future PC worker is introduced.
- Implemented: isolated heavy dependency manifest, CPU-only PyTorch workflow installation, Hugging Face model cache, Tesseract provisioning, TrOCR prefetch, pix2tex backend smoke test and full regression execution.
- Verification: Heavy OCR workflow run 35649732688 passed; main CI run 35649997963 passed.
- Remaining: real labeled model-accuracy benchmark and live Telegram evidence.
