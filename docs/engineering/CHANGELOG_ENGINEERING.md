# Engineering Changelog

## 2026-09-21 — Phase 19–25 hardening batch
- Added quality/failure matrix and bounded retry contracts.
- Added OCR benchmark metrics for character/expression/structure accuracy.
- Added adversarial mathematical input coverage.
- Added Persian-first RTL answer rendering policy.
- Added production configuration/resource/recovery contracts.
- Added release-audit gate and production verification runbook.
- Added P19–P25 acceptance tests.
- Fixed Ruff/mypy issues during CI iterations.
- CI evidence currently exists for commit e84744b85941c46298c3221f4288c51d3919ed31: lint/type/tests passed; format failed on that earlier SHA.
- Subsequent formatting fixes and state documentation were committed after that run; a fresh CI run on the final HEAD is required before any VERIFIED claim.
- No external production/OCR/load/security evidence has been fabricated.
