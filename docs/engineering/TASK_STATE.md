# Task State

## Current batch: Phase 11 through Phase 20

### P11-T01 — Interactive Tutor
- Status: VERIFIED
- Acceptance: stateful teaching session, hints, answer receipt/checking, re-explanation and progressive practice.
- Evidence: tests + CI GREEN.

### P12-T01 — Exercise Generation
- Status: VERIFIED
- Acceptance: deterministic validated exercises across multiple domains with rejection of invalid generation.
- Evidence: tests + CI GREEN.

### P13-T01 — Learning Profile
- Status: VERIFIED
- Acceptance: minimal profile records, accuracy, weak topics, adaptive difficulty and privacy flag.
- Evidence: tests + CI GREEN.

### P14-T01 — Telegram/Application Boundary
- Status: VERIFIED
- Acceptance: transport-neutral message contracts, Persian menu/error mapping, commands and session history.
- Known gap: production Telegram SDK/webhook wiring.

### P15-T01 — PDF/File Pipeline
- Status: VERIFIED
- Acceptance: bounded PDF input and indexed question lookup foundation.
- Known gap: real multi-page PDF extraction/OCR integration.

### P16-T01 — Job System
- Status: VERIFIED
- Acceptance: queue, claim, retry, success/failure and cancellation lifecycle.
- Known gap: distributed worker/load/cancellation validation.

### P17-T01 — Security Baseline
- Status: VERIFIED
- Acceptance: text bounds, filename/path validation and private-IP URL rejection.
- Known gap: DNS rebinding/metadata-address and full dependency/adversarial corpus.

### P18-T01 — Observability
- Status: VERIFIED
- Acceptance: metric collection and success/failure timing span primitives.

### P19-T01 — Quality/Test Foundation
- Status: COMPLETED
- Evidence: acceptance/regression suite and dual-Python CI GREEN.
- Remaining: full E2E, load, security and recovery matrix.

### P20-T01 — Mathematical Benchmark Foundation
- Status: COMPLETED
- Evidence: benchmark runner, result model and pass-rate calculation.
- Remaining: comprehensive real mathematical corpus and solver-family scorecards.

## Verification evidence
- Latest full CI: workflow run 35573378971
- Commit: e0616a742448ddad90af72eeb39b4b792a1905d0
- Gates: Ruff lint PASS, Ruff format PASS, mypy PASS, pytest 3.11 PASS, pytest 3.12 PASS.

## Next task
Complete P19/P20 extended validation, then begin Phase 21.
