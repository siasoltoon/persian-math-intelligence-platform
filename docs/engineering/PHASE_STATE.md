# Phase State

## Phase 0–18
- Status: VERIFIED
- Evidence: existing acceptance suites and green CI.

## Phase 19 — QUALITY / TESTING
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added: failure/recovery test matrix, retry policy and acceptance coverage.
- Pending: live E2E, load/performance, security corpus and distributed recovery evidence.

## Phase 20 — MATHEMATICAL BENCHMARK
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added: benchmark execution, result/pass-rate infrastructure and representative regression corpus.
- Pending: comprehensive labeled corpus across all roadmap domains and solver-family scorecards.

## Phase 21 — OCR BENCHMARK
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added: character/expression/structure metrics, benchmark case model, bounded page rendering, sparse/scanned-page OCR fallback, page-level source selection, and extreme-degradation preprocessing.
- OCR hardening now includes deskew, content cropping, adaptive upscaling, denoising, CLAHE, normalization, unsharp recovery, adaptive/OTSU thresholding, morphology and multiple recognition passes.
- Pending: real labeled image corpus covering printed/degraded/rotated/cropped/handwriting/fractions/superscripts/nested expressions/matrices/diagrams.

## Phase 22 — ADVERSARIAL / FAILURE TESTING
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added: adversarial mathematical inputs, safe parser boundaries and no-crash acceptance coverage.
- Pending: broader malformed-OCR, resource-exhaustion, cancellation, retry and backend-failure matrix.

## Phase 23 — UX POLISH
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added: Persian-first RTL policy and verified/unverified answer rendering.
- Pending: real Telegram/mobile visual regression and long-message/formula rendering evidence.

## Phase 24 — PRODUCTION HARDENING
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added: production config/resource/recovery contracts, secure document limits and hardened parser/OCR boundaries.
- Pending: real deployment, backup/restore, rollback, load, dependency and operational evidence.

## Phase 25 — FINAL RELEASE AUDIT
- Status: IMPLEMENTED / BLOCKED BY EVIDENCE
- Added: mandatory release-audit areas and production verification runbook.
- Release must remain blocked while required Critical/High evidence is missing.

## Gate
- No phase is marked VERIFIED solely because source code exists or unit tests pass.