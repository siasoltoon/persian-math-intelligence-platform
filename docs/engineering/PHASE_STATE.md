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
- Added: character/expression/structure metrics, bounded page rendering, sparse/scanned-page OCR fallback, page-level source selection, extreme-degradation preprocessing, expanded preprocessing variants/PSM coverage, and structural math OCR analysis.
- Added structural recognition for fractions, superscripts/subscripts and matrix/table-like layouts.
- Added pluggable handwriting recognition contract with strict cross-backend corroboration.
- Pending: real labeled image/handwriting corpus and a concrete handwriting-specific recognition backend.

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

## Phase 21 — Specialized visual recognition extension
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added concrete optional TrOCR handwriting recognition with line segmentation.
- Added concrete optional pix2tex formula-to-LaTeX recognition.
- Added safe LaTeX output validation and multi-backend formula consensus.
- CI run #315 passed all jobs.
- Pending: deploy/cache model artifacts, run real handwriting/formula corpus, record character/expression/structural metrics, and perform live Telegram validation.


## Phase 21 — GitHub-hosted heavy OCR execution
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added isolated heavyweight OCR dependency manifest and a GitHub-hosted worker workflow.
- Workflow provisions Tesseract, PyTorch/Transformers, TrOCR model cache and pix2tex support, then runs regression and runtime smoke checks.
- Pending: successful workflow run evidence and real labeled OCR/handwriting benchmark evidence.


## Phase 21 — GitHub-hosted heavy OCR execution
- Status: IMPLEMENTED / VERIFICATION PENDING
- Added isolated heavyweight OCR dependency manifest and a GitHub-hosted worker workflow.
- Heavy OCR workflow run 35649732688 passed all steps.
- Main CI run 35649997963 passed all jobs, including the Heavy OCR runtime.
- Pending: real labeled OCR/handwriting/formula benchmark evidence.


## Phase 19/23/24 — Persian natural-language math input hardening
- Status: VERIFIED for repository/CI integration; live Telegram verification pending.
- Added bounded lexical extraction of safe mathematical payloads from Persian natural-language prompts, including whitespace handling and equation preference.
- Added concept-only representation fallback and structured engine failure for prompts without a mathematical payload.
- PR #11 CI run 35656388276 passed all required jobs, including both Python versions and Heavy OCR runtime.
- Remaining evidence: live Telegram text-input validation and broader real-user corpus coverage.


## Phase 19/20/23/24 — Structured Persian word-problem routing
- Status: VERIFIED for repository/CI integration; live re-test pending.
- Added deterministic structured routing for common geometry, function-evaluation and arithmetic-sequence natural-language prompts.
- Added independent verification through the existing canonical verification path and safe user-facing solution rendering.
- CI run 35659054757 passed all required jobs, including Heavy OCR runtime.
- Remaining evidence: live Telegram re-test and broader real mathematical benchmark.


## Phase 19/20/23/24 — Advanced mathematical routing extension
- Status: VERIFIED for repository/CI integration; live Telegram verification pending.
- Added structured routing and verification for derivatives, indefinite/definite integrals, limits, linear systems and multi-part function analysis.
- Added regression tests for the exact advanced failures observed during live Telegram testing.
- CI run 35700711582 passed all required jobs, including Heavy OCR runtime.
- Remaining evidence: live Telegram re-test and broader labeled mathematical benchmark coverage. Universal mathematical mastery is not claimed from this extension alone.
