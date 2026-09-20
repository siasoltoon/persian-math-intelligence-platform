# Architecture Map

## Verified Phase 1–10 architecture

### Core
- domain.py — typed mathematical/problem/education contracts
- canonical.py — controlled normalization and canonical parsing
- understanding.py / input_understanding.py — intent, domain and ambiguity
- solver.py — specialized SymPy-backed solver primitives and router
- verification.py — independent verification and evidence
- engine.py — integrated request pipeline

### OCR / Visual Mathematics
- ocr.py — bounded image validation, preprocessing, OCR protocol, Tesseract backend and structural reconstruction
- ocr_consensus.py — multi-candidate agreement/confidence/retry
- geometry.py — coordinate geometry primitives
- visual_math.py — validated graph/visual scene representation

### Education / Explanation
- explanation.py — Persian explanation object and level-aware presentation
- education.py — curriculum rules, objectives and adaptive difficulty
- tutor.py — tutoring turn primitives
- exercises.py — validated exercise generation foundation

## Required boundaries
- Core mathematical modules MUST NOT depend on Telegram.
- Mathematical correctness MUST NOT depend on presentation formatting.
- Verification MUST be independently callable from the primary solver.
- File/image handling MUST treat input as untrusted.
- Deployment adapters MUST remain replaceable.
- User-facing error mapping MUST be separated from internal exceptions/logging.

## Verified critical flow
Input → understanding/OCR → canonical representation → classification → solver router → specialized solver → independent verification → confidence/evidence → Persian explanation → educational adaptation.

## Failure boundaries
Uncertain OCR/parsing → retry/clarification, not guessing.
Solver failure → controlled failure, not fabricated result.
Verification failure → result remains unverified.
Resource exhaustion → bounded/cancellable input handling.
