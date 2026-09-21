## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasoltoon/persian-math-intelligence-platform
- Current execution date: 2026-09-21
- Current target: live Windows runtime + Telegram end-to-end verification
- Status: Interactive Telegram UI implemented; CI green; live verification pending

## Current work
- Integrated the operational architecture of `siasoltoon/vps` into this repository through a safe, secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing application service.
- Added Persian-first persistent Telegram menus and callback flows for solve, exercise, profile, history, settings and help.
- Added exercise domain/difficulty selection and educational-level selection.
- Added photo OCR handling with image validation and confidence gating.
- Kept Core/application code independent of Telegram transport.

## Verification
- Telegram UI implementation is covered by regression tests.
- CI run 202 completed successfully on the final UI implementation commit.
- Live Telegram/VPS execution is not yet claimed as verified.
- The source VPS workflow's committed credential was intentionally not copied; GitHub Secrets are required instead.

## External evidence still required
- Live Windows workflow execution and RDP/Tailscale reachability
- Live Telegram /start, /help, menu, callback, text-problem and photo acceptance tests
- Real labeled OCR benchmark corpus
- Distributed worker/concurrency/load evidence
- Full security/dependency audit
- Production backup/restore/rollback evidence
- Comprehensive real mathematical benchmark

## Next action
Execute the Windows runtime with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`; then run the Telegram menu/text/photo E2E matrix and record evidence before marking runtime/UI work VERIFIED.
