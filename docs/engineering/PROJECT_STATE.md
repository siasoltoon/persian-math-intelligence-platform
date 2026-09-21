## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasooltoon/persian-math-intelligence-platform
- Current execution date: 2026-09-21
- Current target: secure multi-format Telegram runtime + live end-to-end verification
- Status: Text/photo/PDF document pipeline hardened; repository CI green; live verification pending

## Current work
- Integrated the operational architecture of `siasoltoon/vps` into this repository through a safe, secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing application service.
- Added Persian-first persistent Telegram menus and callback flows for solve, exercise, profile, history, settings and help.
- Added photo OCR handling with image validation, multi-pass preprocessing, consensus gating and confidence rejection.
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
- Telegram UI implementation is covered by regression tests.
- Document validation and scanned-like PDF selection are covered by dedicated regression tests.
- CI run 35634158094 / CI #278 passed Ruff lint, Ruff format, mypy, and pytest on Python 3.11 and 3.12 after the hardening batch.
- The hardening changes were merged to main as `b573f1078edc8f864a7e9371fb4492fd8dbef729`.
- Live Telegram/VPS execution is not yet claimed as verified.
- The source VPS workflow's committed credential was intentionally not copied; GitHub Secrets are required instead.

## External evidence still required
- Live Windows workflow execution and RDP/Tailscale reachability
- Live Telegram /start, /help, menu, callback, text, photo and PDF acceptance tests
- Real labeled OCR benchmark corpus, especially degraded/handwritten mathematical input
- Distributed worker/concurrency/load evidence
- Full security/dependency/license audit
- Production backup/restore/rollback evidence
- Comprehensive real mathematical benchmark

## Next action
Execute the live Windows/Tailscale/Telegram E2E matrix including clear/degraded images, text PDF, scanned multi-page PDF, mixed text/image PDF, image-as-document and malformed/oversized files. Keep Phase 25 blocked until the external evidence is recorded.
