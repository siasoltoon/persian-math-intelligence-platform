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


## GitHub-hosted heavy OCR worker — 2026-09-21
- Heavy OCR runtime execution is temporarily assigned to GitHub Actions rather than requiring the future PC worker.
- Added isolated requirements-heavy-ocr.txt with Transformers, Accelerate, SentencePiece and pix2tex; CPU-only PyTorch is installed explicitly by workflow from the official PyTorch wheel index.
- Added .github/workflows/heavy-ocr-worker.yml with Tesseract installation, Hugging Face caching, TrOCR model prefetch, specialized backend smoke checks and full regression tests.
- PR #10 merged to main as e69b71dab0a05848b46f8f798d1604abd85775c8.
- Heavy OCR workflow run 35649732688 passed all steps, including model loading and backend smoke checks.
- Main CI run 35649997963 passed Ruff, format, mypy, Python 3.11/3.12 pytest and the Heavy OCR runtime job.
- This proves runtime readiness only; real OCR accuracy remains evidence-gated by a labeled benchmark corpus.


## Plain-text Telegram math input hardening — 2026-09-22
- Root cause identified: the Telegram application passed the entire Persian natural-language prompt directly into the restricted mathematical parser. The parser correctly rejected Persian prose as unsupported mathematical syntax, so valid questions were reported as insufficiently reliable.
- Implemented a bounded lexical math-fragment extractor that promotes only parser-allowed mathematical characters from natural-language wrappers; parser safety boundaries and confidence/verification gates remain intact.
- Updated problem representation, solver routing and verification to operate on the extracted canonical mathematical payload.
- Added regression coverage for Persian natural-language arithmetic and equation prompts.
- Verification status: implementation complete; repository CI/live Telegram re-test pending.


## Plain-text Telegram math input hardening — 2026-09-22
- Root cause identified: the Telegram application passed the entire Persian natural-language prompt directly into the restricted mathematical parser.
- Implemented a bounded lexical math-fragment extractor that accepts whitespace around safe mathematical tokens, prefers valid equations, and preserves the parser's restricted grammar.
- Problem understanding now represents concept-only prompts without fabricating a mathematical payload; the engine returns a structured non-mathematical-input failure instead of raising an internal exception.
- Added regression coverage for Persian natural-language arithmetic/equation prompts, spaced Persian-digit expressions, and concept-only prompts.
- Verification: PR #11 CI run 35656388276 passed Ruff lint, Ruff format, mypy, pytest on Python 3.11/3.12, and Heavy OCR runtime; PR #11 was merged to main as `9fea0f1764a12ed52f70fbdf2b8d2ebae8822406`.
- Live Telegram re-test remains pending; production accuracy claims remain evidence-gated.


## Structured Persian word-problem hardening — 2026-09-22
- Live Telegram testing exposed three parser-routing gaps: geometry wording lost semantic context and returned a raw numeric token; function-evaluation wording was misclassified as an equation; arithmetic-sequence wording was not supported.
- Added bounded structured handlers for rectangle area, function evaluation and arithmetic-sequence sums.
- Structured results are converted to canonical mathematical expressions before independent verification, preserving the existing no-guess/verification gates.
- Equation solution tuples are rendered as mathematical solution sets rather than Python tuple syntax.
- CI run 35659054757 passed Ruff lint, Ruff format, mypy, pytest Python 3.11/3.12 and Heavy OCR runtime.
- Live Telegram re-test after this fix remains pending; no claim of production-wide natural-language coverage is made.


## Advanced mathematical routing hardening — 2026-09-22
- Live Telegram testing exposed additional domain-routing failures after the initial Persian word-problem fixes: derivative, indefinite/definite integral, limit, linear-system and multi-part calculus-analysis prompts.
- Implemented bounded structured handlers for these classes and dedicated independent verification paths rather than weakening the restricted generic parser.
- Added user-facing rendering for structured system solutions and function-analysis results.
- Regression coverage now exercises the exact reported advanced cases.
- CI run 35700711582 passed Ruff lint, Ruff format, mypy, pytest Python 3.11/3.12 and Heavy OCR runtime.
- Current status: repository/CI integration verified; live Telegram re-test pending. The platform is being expanded domain-by-domain and no universal mathematical coverage claim is made until benchmark evidence supports it.
