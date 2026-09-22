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


### INPUT-T01 — Persian natural-language text math extraction
- Status: IMPLEMENTED / VERIFICATION PENDING
- Phase: 19/23/24
- Objective: make ordinary Persian text questions reach the existing safe mathematical parser/solver without weakening parser security or verification gates.
- Root cause: full Persian prose was being submitted to the restricted parser; valid math embedded in the prompt was never isolated.
- Implemented: bounded lexical math-fragment extraction, equation preference, sentence-punctuation trimming, solver integration, representation-aware verification, and regression tests for arithmetic/equation prompts.
- Expected examples: Persian arithmetic prompt → 29; Persian linear-equation prompt → x = 5.
- Remaining: green CI evidence and live Telegram re-test.


### INPUT-T01 — Persian natural-language text math extraction
- Status: VERIFIED for repository/CI integration / live verification pending
- Phase: 19/23/24
- Objective: make ordinary Persian text questions reach the existing safe mathematical parser/solver without weakening parser security or verification gates.
- Root cause: full Persian prose was being submitted to the restricted parser; valid math embedded in the prompt was never isolated.
- Implemented: bounded lexical math-fragment extraction, whitespace-safe candidate grammar, equation preference, sentence-punctuation trimming, concept-only representation fallback, structured non-math engine failure, solver integration, and representation-aware verification.
- Regression coverage: Persian arithmetic, Persian linear equations, spaced Persian-digit expressions, and concept-only prompts.
- Verification: PR #11 CI run 35656388276 passed Ruff lint/format, mypy, pytest Python 3.11/3.12, and Heavy OCR runtime; merged to main as `9fea0f1764a12ed52f70fbdf2b8d2ebae8822406`.
- Remaining: live Telegram re-test and real-world corpus evidence.


### INPUT-T02 — Persian structured word-problem routing
- Status: VERIFIED for repository/CI integration / live re-test pending
- Phase: 19/20/23/24
- Objective: correctly solve common Persian natural-language problems that cannot be represented safely as a bare mathematical fragment.
- Live failure classes addressed: rectangle-area wording returned only the first numeric token; function-evaluation wording was misrouted as an equation in the auxiliary function symbol; arithmetic-sequence sum wording was not recognized; equation solution tuples were rendered as raw Python tuples.
- Implemented: bounded structured handlers for rectangle area, function evaluation and arithmetic-sequence sums; independent verification through canonical expression representation; user-facing solution-set rendering; regression coverage.
- CI verification: run 35659054757 passed Ruff lint, Ruff format, mypy, pytest Python 3.11/3.12 and Heavy OCR runtime.
- Remaining: repeat the Telegram live matrix with these exact cases and expand the labeled real-world benchmark.


### INPUT-T03 — Advanced calculus, systems and multi-part analysis routing
- Status: VERIFIED for repository/CI integration / live re-test pending
- Phase: 19/20/23/24
- Objective: expand structured Persian math coverage for calculus, linear systems and multi-part function analysis while preserving independent verification and no-guess behavior.
- Live failure classes addressed: derivative of a composite rational function returned an empty solution set; indefinite integral was misparsed as a generic expression; a three-variable linear system was rejected; a definite integral with Unicode bounds was rejected; a limit with bracketed numerator crashed in the restricted parser; a multi-part function-analysis request was rejected.
- Implemented: bounded handlers for derivatives, indefinite/definite integrals, limits, linear systems and critical-point/monotonicity/inflection analysis; independent verification paths; safe bracket/bound normalization; structured user-facing rendering.
- Regression coverage: all reported advanced cases, including real radical equation preservation, now pass in pytest on Python 3.11/3.12.
- CI verification: run 35700711582 passed Ruff lint, Ruff format, mypy, pytest Python 3.11/3.12 and Heavy OCR runtime.
- Remaining: live Telegram re-test and expansion of the labeled mathematical benchmark across additional domains. This task does not claim universal mathematical coverage.


### CI-T01 — Regression failure isolation and advanced verification fixes
- Status: IN_PROGRESS / CI verification pending
- Phase: 19–25 hardening / CI reliability
- Resolved higher-order derivative verification semantics, Taylor-series verification dispatch/metadata, matrix operation routing, and number-theory verification method alignment.
- Heavy OCR CI now runs OCR/document-focused regression tests instead of duplicating the complete mathematical suite.
- Fresh CI evidence is required before VERIFIED.


### CI-T01 — Regression failure isolation and advanced verification fixes
- Status: VERIFIED
- Phase: 19–25 hardening / CI reliability
- Objective: eliminate deterministic advanced-test failures/timeouts while preserving full regression coverage and independent verification.
- Implementation: higher-order derivative parsing/verification; Taylor-series metadata/verification; matrix routing; number-theory method alignment; finite-sum variable-assumption preservation; periodic trigonometric union verification without infinite set iteration; Heavy OCR suite isolation; per-test pytest timeout.
- Tests: full pytest on Python 3.11 and 3.12; Ruff lint/format; mypy; Heavy OCR runtime.
- Validation: GitHub Actions run 422 (35709968535) fully green.
- Integration: both standard Python suites and Heavy OCR runtime passed.
- Documentation/state: updated after final green verification.
- Known issues: live Telegram and real-world benchmark evidence remain external gates.
- Next Action: proceed to live Telegram/E2E and benchmark evidence; do not infer production-wide mathematical accuracy from CI alone.


### INPUT-T04 — Multi-problem Telegram batch solving
- Status: VERIFIED for repository/CI integration / live Telegram verification pending
- Phase: 19/23/24
- Objective: allow a user to send multiple mathematical problems in one Telegram text message and receive all independently solved/verified results together.
- Acceptance: bounded parsing, no accidental splitting of multiline systems or multi-part analysis, independent per-problem processing, combined Persian response, safe resource limits and Telegram message-length handling.
- Implementation: new batch module; application-level handle_batch; explicit «سؤال N» and numbered delimiters; maximum 12 problems and 12000 input characters; per-problem history recording; ordered response chunking at the Telegram text limit.
- Tests: batch splitting, false-positive prevention, aggregate response, independent history entries and item limits.
- Validation: CI run 431 / 35712792646 fully green; Python 3.11 = 125 passed; Python 3.12 = 125 passed; Ruff lint/format ✓; mypy ✓; Heavy OCR runtime ✓.
- Known issue: live Telegram execution evidence remains pending.
- Next Action: perform live Telegram E2E matrix including one-message multi-problem text, mixed supported domains, one intentionally unsupported problem, and long aggregate responses.
