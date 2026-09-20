# Test State

## Baseline
- Date: 2026-09-21
- Unit tests: ESTABLISHED
- Solver tests: ESTABLISHED
- Verification tests: ESTABLISHED
- Canonical representation tests: ESTABLISHED
- Integrated engine tests: ESTABLISHED
- Integration/contract/OCR/security/performance/E2E/regression suites: NOT YET ESTABLISHED

## Current CI
- CI workflow: .github/workflows/ci.yml
- Matrix: Python 3.11 and 3.12
- Gates: Ruff lint, Ruff format check, mypy, pytest
- Latest validation runs are being monitored after iterative fixes.

## Validation rule
A task or phase cannot be VERIFIED from code presence alone. Record actual green CI and acceptance-review evidence before changing status to VERIFIED.
