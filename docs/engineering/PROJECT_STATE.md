## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasoltoon/persian-math-intelligence-platform
- Current execution date: 2026-09-21
- Current target: Windows VPS runtime integration + Telegram interface execution
- Status: Runtime integration implemented on feature branch; verification pending CI and live Telegram/VPS evidence

## Current work
- Integrated the operational architecture of `siasoltoon/vps` into this repository through a safe, secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing application service.
- Added photo OCR handling with image validation and confidence gating.
- Kept Core/application code independent of Telegram transport.

## Verification
- Runtime unit coverage added; fresh CI is required on this branch.
- Live Telegram/VPS execution is not yet claimed as verified.
- The source VPS workflow's committed credential was intentionally not copied; GitHub Secrets are required instead.

## External evidence still required
- Live Windows workflow execution and RDP/Tailscale reachability
- Live Telegram `/start`, `/help`, text-problem and photo acceptance tests
- Real labeled OCR benchmark corpus
- Distributed worker/concurrency/load evidence
- Full security/dependency audit
- Production backup/restore/rollback evidence
- Comprehensive real mathematical benchmark

## Next action
Run the full CI suite on the integration branch. After CI is green, execute the Windows runtime with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`, then record live Telegram/VPS evidence before marking runtime work VERIFIED.
