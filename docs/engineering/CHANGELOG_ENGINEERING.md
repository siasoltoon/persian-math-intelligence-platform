# Engineering Changelog

## 2026-09-21

### CI hardening and Phase 0–10 validation gate
- Repaired malformed test sources containing literal escape sequences that prevented Ruff parsing.
- Corrected canonical system parsing so normalized mathematical text preserves line boundaries.
- Corrected engine verification typing so solver output is validated before independent verification.
- Corrected exercise validation to return a concrete boolean.
- Aligned tests with the typed input-understanding contract and SymPy inequality representation.
- Fixed Ruff import, lint and formatting findings across the Phase 0–10 implementation.
- Reworked GitHub Actions into independent Ruff lint, Ruff format, mypy and Python 3.11/3.12 pytest jobs.
- Added read-only workflow permissions, manual dispatch and per-job timeouts.
- CI is GREEN on commit 7e004c5531f21f8e02d348c01a8806ea87cead25, workflow run 35544271169.
- Phase 0–10 remain explicitly unverified at the phase-acceptance level until the roadmap acceptance review is completed.

### Core expansion through Phase 10
- Expanded canonical representation for inequalities, systems, matrices and superscript exponents.
- Expanded solver primitives across algebra, calculus, matrices, probability, statistics, numerical roots, complex roots, optimization and ODE foundations.
- Added independent verification and integrated processing pipeline.
- Added input-understanding intent and ambiguity detection.
- Added OCR validation, bounded preprocessing planning, backend protocol and controlled unavailable state.
- Added OCR consensus/confidence aggregation with disagreement rejection.
- Added geometry primitives for coordinate mathematics.
- Added Persian-first explanation objects with education-level adaptation.
- Added educational curriculum rules, adaptive difficulty, tutoring session primitives and validated exercise generation.
- Added tests for all newly introduced foundations.
