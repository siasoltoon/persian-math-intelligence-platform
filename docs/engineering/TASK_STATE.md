## VPS / Telegram runtime integration

### VPS-T01 — Windows runtime integration
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: bring the operational behavior of `siasoltoon/vps` into the math repository without propagating its committed credential.
- Acceptance: Windows runner provisions RDP/Tailscale, installs Python/Tesseract, validates secrets and starts the Telegram process.
- Tests: runtime configuration tests; CI run 202 green.
- Live evidence: pending.

### VPS-T02 — Telegram execution adapter
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: run the existing ApplicationService through a real Telegram polling adapter.
- Acceptance: /start, /help, text problems and validated photo OCR reach the application service and return Persian responses without raw exceptions.
- Tests: runtime configuration and regression suite; CI run 202 green.
- Live evidence: pending.

### TUI-T01 — Interactive Telegram UI
- Status: COMPLETED / VERIFICATION PENDING
- Phase: 23 — UX POLISH
- Objective: provide a production-oriented Persian-first Telegram interaction surface over the existing application service.
- Implemented: persistent main keyboard; solve flow; exercise domain/difficulty flow; profile; educational-level selection; history; settings; help; /menu; callback routing; safe user-facing failures.
- Tests: dedicated `tests/test_telegram_ui.py`; full CI run 202 green across Ruff lint/format, mypy, Python 3.11 and Python 3.12.
- Live validation: pending Telegram/mobile visual and interaction evidence.

## Phase 19–25 hardening batch
- P19–P24: IMPLEMENTED / VERIFICATION PENDING
- P25: IMPLEMENTED / BLOCKED by required external evidence
