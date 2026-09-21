## VPS / Telegram runtime integration

### VPS-T01 — Windows runtime integration
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: bring the operational behavior of `siasoltoon/vps` into the math repository without propagating its committed credential.
- Acceptance: Windows runner provisions RDP/Tailscale, installs Python/Tesseract, validates secrets and starts the Telegram process.
- Tests: runtime configuration tests; CI #278 green.
- Live evidence: pending.

### VPS-T02 — Telegram execution adapter
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: run the existing ApplicationService through a real Telegram polling adapter.
- Acceptance: /start, /help, text problems and validated photo OCR reach the application service and return Persian responses without raw exceptions.
- Tests: runtime configuration and regression suite; CI #278 green.
- Live evidence: pending.

### TUI-T01 — Interactive Telegram UI
- Status: COMPLETED / VERIFICATION PENDING
- Phase: 23 — UX POLISH
- Objective: provide a production-oriented Persian-first Telegram interaction surface over the existing application service.
- Implemented: persistent main keyboard; solve flow; exercise domain/difficulty flow; profile/educational level; history; settings; help; /menu; callback routing; safe user-facing failures.
- Tests: dedicated `tests/test_telegram_ui.py`.
- Live validation: pending Telegram/mobile visual and interaction evidence.

### FILE-T01 — Secure document intelligence
- Status: IMPLEMENTED / VERIFICATION PENDING
- Phase: 21/22/24
- Objective: extend the Telegram input layer from plain text/photos to bounded PDF and document processing without unsafe execution.
- Implemented: PDF signature validation, encrypted-PDF rejection, byte/page/pixel/text limits, adaptive page rendering, per-page text preservation, automatic OCR for sparse/scanned pages, page-level source selection, scanner-watermark handling, image-file handling, unified document result model, configurable Tesseract language.
- OCR hardening: multi-pass image variants, line/region reconstruction, confidence gating and consensus rejection; disagreement is rejected rather than guessed.
- Mathematical hardening: bounded/safe parser input and stronger independent verification.
- Tests: `tests/test_file_intelligence.py`, `tests/test_canonical.py`, `tests/test_solver_verification.py` plus existing OCR/consensus regression suites.
- CI: #278 / run ID 35634158094 green on Python 3.11/3.12 with Ruff and mypy.
- Pending: live multi-page PDF, scanned-PDF, mixed text/image PDF, difficult handwriting corpus and malformed/adversarial external evidence.

## Phase 19–25 hardening batch
- P19–P24: IMPLEMENTED / VERIFICATION PENDING
- P25: IMPLEMENTED / BLOCKED by required external evidence
