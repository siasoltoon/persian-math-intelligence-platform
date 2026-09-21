## VPS / Telegram runtime integration

### VPS-T01 — Windows runtime integration
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: bring the operational behavior of `siasoltoon/vps` into the math repository without propagating its committed credential.
- Acceptance: Windows runner provisions RDP/Tailscale, installs Python/Tesseract, validates secrets and starts the Telegram process.
- Tests: runtime configuration tests added; CI pending.

### VPS-T02 — Telegram execution adapter
- Status: IMPLEMENTED / VERIFICATION PENDING
- Objective: run the existing ApplicationService through a real Telegram polling adapter.
- Acceptance: `/start`, `/help`, text problems and validated photo OCR reach the application service and return Persian responses without raw exceptions.
- Tests: runtime configuration tests added; live Telegram evidence pending.

## Phase 19–25 hardening batch
- P19–P24: IMPLEMENTED / VERIFICATION PENDING
- P25: IMPLEMENTED / BLOCKED by required external evidence
