## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasooltoon/persian-math-intelligence-platform
- Current execution date: 2026-09-21
- Current target: secure multi-format Telegram runtime + live end-to-end verification
- Status: Text/photo/PDF document pipeline implemented; CI/live verification pending

## Current work
- Integrated the operational architecture of `siasoltoon/vps` into this repository through a safe, secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing application service.
- Added Persian-first persistent Telegram menus and callback flows for solve, exercise, profile, history, settings and help.
- Added photo OCR handling with image validation and confidence gating.
- Added secure document intelligence for PDF and image documents: bounded download, PDF signature/page/pixel/text limits, text extraction, page rendering and optional OCR.
- Kept Core/application code independent of Telegram transport.

## Verification
- Telegram UI implementation is covered by regression tests.
- Document validation is covered by dedicated regression tests.
- Previous CI run 202 completed successfully on the pre-document UI implementation.
- Live Telegram/VPS execution is not yet claimed as verified.
- The source VPS workflow's committed credential was intentionally not copied; GitHub Secrets are required instead.

## External evidence still required
- CI for the document-layer commits
- Live Windows workflow execution and RDP/Tailscale reachability
- Live Telegram /start, /help, menu, callback, text, photo and PDF acceptance tests
- Real labeled OCR benchmark corpus
- Distributed worker/concurrency/load evidence
- Full security/dependency/license audit
- Production backup/restore/rollback evidence
- Comprehensive real mathematical benchmark

## Next action
Run CI on the document-layer head, fix every failure before proceeding, then execute the live Windows/Tailscale/Telegram E2E matrix including multi-page PDF and scanned-PDF cases. Keep Phase 25 blocked until the external evidence is recorded.
