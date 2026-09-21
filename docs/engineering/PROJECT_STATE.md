## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasoltoon/persian-math-intelligence-platform
- Current execution date: 2026-09-21
- Current target: secure multi-format Telegram runtime + live end-to-end verification
- Status: OCR/image preprocessing and structural math OCR strengthened; live verification and real handwriting benchmark remain pending

## Current work
- Integrated the operational architecture of `siasoltoon/vps` into this repository through a safe, secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing application service.
- Added Persian-first persistent Telegram menus and callback flows for solve, exercise, profile, history, settings and help.
- Added photo OCR handling with image validation, multi-pass preprocessing, consensus gating and confidence rejection.
- Strengthened degraded/handwritten-image preprocessing with deskew, content cropping, adaptive upscaling, denoising, CLAHE, normalization, unsharp recovery, adaptive/OTSU thresholding, morphology, bilateral recovery, inversion and multiple OCR passes.
- Added structural mathematical OCR analysis for:
  - line/region reconstruction
  - fraction numerator/denominator relationships
  - superscript/subscript relationships
  - matrix/table-like row/column layouts
  - mixed text/math classification
- Added a pluggable handwriting-recognition backend contract and a composite backend that accepts secondary handwriting output only when independently corroborated by the primary OCR path.
- Strengthened handwriting consensus to a stricter similarity threshold so conflicting mathematical operators are not silently promoted.
- Hardened secure document intelligence for PDF and image documents:
  - bounded download and resource limits
  - PDF signature/page/pixel/text limits
  - encrypted-PDF rejection
  - page rendering with adaptive scale under a pixel budget
  - native PDF text preservation
  - automatic OCR for sparse/scanned pages when an OCR backend is supplied
  - page-level source selection to avoid concatenating watermark/text-layer content with OCR
  - explicit scanner-watermark handling for extraction selection
  - confidence-gated image/document OCR
- Migrated document processing from deprecated `fitz` usage to the supported `pymupdf` import.
- Hardened mathematical parsing with bounded input, a restricted character grammar, disabled Python builtins in the SymPy parser context, and regression coverage against Python-expression injection.
- Strengthened verification by combining symbolic equivalence with deterministic numeric re-evaluation and by using a separate `solveset` verification path for equation solution sets.
- Kept Core/application code independent of Telegram transport.

## Verification
- Math OCR/handwriting-structure PR #8 was merged to main as `d41fe316ab6b94375cd21a87c90272e0a20086d5`.
- PR CI #304 / run ID 35643936787 passed Ruff lint, Ruff format, mypy, and pytest on Python 3.11 and 3.12.
- Main CI #305 / run ID 35644040284 passed all jobs after merge.
- OCR tests now explicitly cover extreme-image preprocessing, structural math detection and strict handwriting-backend corroboration.
- Live Telegram/VPS execution is not yet claimed as verified.
- Real labeled OCR/handwriting benchmark evidence is not yet claimed.

## External evidence still required
- Live Windows workflow execution and RDP/Tailscale reachability
- Live Telegram /start, /help, menu, callback, text, photo and PDF acceptance tests
- Real labeled OCR benchmark corpus, especially degraded/handwritten mathematical input
- A concrete handwriting-specific recognition implementation/model wired into the backend contract and benchmarked on real data
- Distributed worker/concurrency/load evidence
- Full security/dependency/license audit
- Production backup/restore/rollback evidence
- Comprehensive real mathematical benchmark

## Next action
Execute the live Windows/Tailscale/Telegram E2E matrix and build the real labeled handwriting/math OCR benchmark. Do not mark handwriting production accuracy VERIFIED until a concrete recognition backend and real benchmark evidence exist. Keep Phase 25 blocked until required external evidence is recorded.

## Specialized OCR backend hardening — 2026-09-21
- Added a concrete optional handwriting backend: Microsoft TrOCR base handwritten, loaded lazily and configured for local-only model loading by default.
- Added line segmentation before handwriting recognition so the handwriting model receives text-line crops rather than an arbitrary full page.
- Added a concrete optional mathematical formula backend: pix2tex image-to-LaTeX adapter.
- Added LaTeX safety validation for bounded output, balanced braces and blocked unsafe TeX execution commands.
- Added multi-backend formula consensus; conflicting formula predictions are rejected rather than guessed.
- Heavy model dependencies remain outside core packaging; model weights are not committed to the repository.
- Specialized-backend CI: run #315 green across Ruff, format, mypy and pytest on Python 3.11/3.12.
- PR #9 merged as `ef75b36ed0bc5e4259a5aa0e414b3b7185876144`.
- Production accuracy remains evidence-gated until the actual model artifacts are deployed on the compute worker and evaluated against a labeled real-world corpus.


## GitHub-hosted heavy OCR worker — 2026-09-21
- Heavy OCR runtime execution is temporarily assigned to GitHub Actions rather than requiring the future PC worker.
- Added isolated requirements-heavy-ocr.txt containing PyTorch, Transformers, Accelerate, SentencePiece and pix2tex.
- Added .github/workflows/heavy-ocr-worker.yml with Tesseract installation, dependency installation, Hugging Face cache, TrOCR model prefetch, specialized backend smoke checks and full regression tests.
- Heavy model weights remain outside Git and are cached by the workflow.
- This proves runtime readiness only; real OCR accuracy remains evidence-gated by a labeled benchmark corpus.
