# Architecture Map

## Verified Phase 1–10 architecture
- domain.py — typed mathematical/problem/education contracts
- canonical.py — controlled normalization and canonical parsing
- understanding.py / input_understanding.py — intent, domain and ambiguity
- solver.py — specialized SymPy-backed solver primitives and router
- verification.py — independent verification and evidence
- engine.py — integrated request pipeline
- ocr.py / ocr_consensus.py — bounded OCR pipeline and consensus
- geometry.py / visual_math.py — geometry and visual-scene contracts
- explanation.py / education.py — Persian explanation and adaptive education

## Phase 11–20 architecture
- tutoring.py — stateful tutor session, hints, checking and re-explanation
- exercises.py — deterministic multi-domain exercise generation and validation
- learning_profile.py — minimal learner records, accuracy and weak-topic analysis
- telegram_adapter.py — transport-neutral Telegram-facing contracts
- application.py — command/session/application orchestration independent of Telegram SDK
- file_pipeline.py — bounded PDF validation and question indexing
- jobs.py — bounded queue/job lifecycle primitives
- security.py — text/file/URL security validation
- observability.py — metrics and timing spans
- benchmark.py — benchmark case/result execution and pass-rate measurement

## Required boundaries
- Core mathematical modules MUST NOT depend on Telegram.
- Mathematical correctness MUST NOT depend on presentation formatting.
- Verification MUST be independently callable from the primary solver.
- File/image handling MUST treat input as untrusted.
- Deployment adapters MUST remain replaceable.
- User-facing error mapping MUST be separated from internal exceptions/logging.

## Verified critical flow
Input → understanding/OCR → canonical representation → classification → solver router → specialized solver → independent verification → Persian explanation → educational adaptation → tutor/application/job/observability contracts.

## Known integration boundaries
- Telegram SDK/webhook deployment
- Real PDF renderer/OCR extraction
- Distributed worker backend
- Production metrics/exporter
- Full benchmark corpus
