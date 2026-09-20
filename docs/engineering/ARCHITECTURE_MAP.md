# Architecture Map

## Current state
Architecture is intentionally skeletal during Phase 0. This document records boundaries before implementation so later code does not accidentally couple Core to Telegram or a deployment vendor.

## Planned logical components
- Interface adapters
- Application/API orchestration
- Problem/domain model
- Canonical mathematical representation
- Input understanding
- OCR/math OCR
- Geometry/visual mathematics
- Solver router and specialized solvers
- Independent verification
- Persian explanation
- Educational system
- Interactive tutor
- Exercise generation
- Learning profile
- File/PDF pipeline
- Job/queue system
- Persistence
- Security
- Observability

## Required boundaries
- Core mathematical modules MUST NOT depend on Telegram.
- Mathematical correctness MUST NOT depend on presentation formatting.
- Verification MUST be independently callable from the primary solver.
- File/image handling MUST treat input as untrusted.
- Deployment adapters MUST remain replaceable.
- User-facing error mapping MUST be separated from internal exceptions/logging.

## Planned critical flows
Input → understanding/OCR → canonical representation → classification → solver router → specialized solver → independent verification → confidence → Persian explanation → educational adaptation → interface response.

Long-running input:
Request → validation → job/queue → worker → solver/OCR → verification → result persistence → interface notification.

## Failure boundaries
Uncertain OCR/parsing → clarification/fallback, not guessing.
Solver failure → controlled failure, not fabricated result.
Verification failure → result remains unverified.
Resource exhaustion → bounded/cancellable job.
Provider/deployment failure → infrastructure-level degraded state without changing Core semantics.
