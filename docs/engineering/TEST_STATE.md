# Test State

## Phase 1–10 established suites
- Canonical representation
- Solver and verification
- Integrated core engine
- Input understanding
- OCR validation, preprocessing and consensus
- Geometry and visual scene contracts
- Persian explanation
- Education, tutor and exercise foundations
- Phase acceptance/regression suite

## CI gates
- Python 3.11
- Python 3.12
- Ruff lint
- Ruff format
- mypy
- pytest

## Current evidence
- Full CI GREEN on workflow run 35545050264.
- Commit under test: a79306d22da0555440c4ad4c5c1c4f0bf87e2a6b.
- Previous full CI GREEN on workflow run 35545046438.
- All current unit, integration and phase-acceptance tests pass on Python 3.11 and 3.12.

## Security validation included
- Image byte-size bounding
- Image dimension/channel bounding
- Decode/verify before OCR
- OCR confidence bounds
- OCR bounding-box bounds
- Controlled backend failure
- No execution of uploaded image contents

## Regression validation included
- Existing Phase 0–10 test suite
- New phase acceptance tests
- Persian input normalization and typed understanding contract
- Independent equation verification

## Future dedicated suites
- Production OCR accuracy benchmark — Phase 21
- Visual/diagram benchmark — Phase 21
- Full E2E — Phase 19
- Dedicated security suite — Phase 19/17
- Performance/load — Phase 19/24
- Mathematical benchmark — Phase 20
- Adversarial/failure corpus — Phase 22
