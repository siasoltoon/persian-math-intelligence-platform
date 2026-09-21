# Engineering Changelog

## 2026-09-21 — Interactive Telegram UI
- Added persistent Persian-first main keyboard.
- Added callback-driven solve, exercise, profile, history, settings and help navigation.
- Added exercise topic and difficulty selection.
- Added educational-level selection.
- Added /menu and safe back navigation.
- Added dedicated application-service regression coverage.
- CI #202 passed Ruff lint, Ruff format, mypy, and pytest on Python 3.11 and 3.12.
- Merged as `f17d65f1409f333789066e00c3c775c083483887`.
- Live Telegram/mobile verification remains pending.

## 2026-09-21 — Phase 19–25 hardening batch
- Added quality/failure matrix and bounded retry contracts.
- Added OCR benchmark metrics for character/expression/structure accuracy.
- Added adversarial mathematical input coverage.
- Added Persian-first RTL answer rendering policy.
- Added production configuration/resource/recovery contracts.
- Added release-audit gate and production verification runbook.
- Added P19–P25 acceptance tests.
- Fixed Ruff/mypy issues during CI iterations.
- No external production/OCR/load/security evidence has been fabricated.

## 2026-09-21 — Windows VPS / Telegram runtime integration
- Added `vps/` runtime reference and a secret-backed Windows workflow.
- Added a real Telegram polling entrypoint using the existing ApplicationService.
- Added photo OCR handling with validation and confidence gating.
- Added Telegram runtime dependency and configuration tests.
- Added explicit security and operational limitations to engineering state.
