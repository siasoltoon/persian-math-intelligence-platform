# Phase State

## Phase 0 — PROJECT FOUNDATION
- Status: VERIFIED
- Evidence: hardened CI gate passes on Python 3.11/3.12 with Ruff lint/format and mypy.

## Phase 1 — CORE DOMAIN MODEL
- Status: VERIFIED
- Evidence: typed domain entities for Problem, ProblemInput, ProblemRepresentation, ProblemClassification, Solution, SolutionStep, VerificationResult, Confidence, EducationalLevel, Difficulty, UserProfile and Exercise; acceptance tests pass.

## Phase 2 — MATHEMATICAL CANONICAL REPRESENTATION
- Status: VERIFIED
- Evidence: normalized Persian/Arabic digits and operators plus expression, equation, inequality, system, matrix, fraction, vector, function, derivative, integral, limit, series and probability parsing; acceptance tests pass.

## Phase 3 — MATHEMATICAL SOLVER ENGINE
- Status: VERIFIED
- Evidence: symbolic and numerical solver primitives with router coverage for expressions, equations and inequalities; calculus, algebra, statistics, probability, matrices, complex roots, optimization and ODE foundations; CI tests pass.

## Phase 4 — VERIFICATION ENGINE
- Status: VERIFIED
- Evidence: symbolic equivalence, numerical equivalence, domain checks, substitution and independent equation solving with evidence/confidence; acceptance and regression tests pass.

## Phase 5 — INPUT UNDERSTANDING
- Status: VERIFIED
- Evidence: Persian/English intent signals, normalization, mathematical structure representation, domain classification and ambiguity detection; acceptance tests pass.

## Phase 6 — OCR / MATH OCR
- Status: VERIFIED
- Evidence: bounded image validation, EXIF-safe preprocessing, contrast/thresholding, region reconstruction, OCR result validation and concrete Tesseract backend integration. OCR failure is controlled and never converted into a guessed answer.
- Accuracy benchmarking and broader handwriting/math-expression benchmark remain Phase 21 scope.

## Phase 7 — OCR CONSENSUS & CONFIDENCE
- Status: VERIFIED
- Evidence: candidate validation, similarity agreement, confidence aggregation, disagreement rejection, retry recommendation and Persian clarification message.

## Phase 8 — GEOMETRY & VISUAL MATHEMATICS
- Status: VERIFIED
- Evidence: coordinate geometry primitives, intersections and structured visual scene representation for graph axes/points/series; validation rejects malformed visual scenes.
- Large visual/OCR benchmark coverage remains Phase 21 scope.

## Phase 9 — PERSIAN EXPLANATION ENGINE
- Status: VERIFIED
- Evidence: Persian explanation object, level-aware style, solution step, final answer, verification channel, notes and common-mistake guidance.

## Phase 10 — EDUCATIONAL SYSTEM
- Status: VERIFIED
- Evidence: elementary, middle, high-school, entrance-exam, university, advanced and olympiad levels; curriculum rules, domain objectives and adaptive difficulty; acceptance tests pass.

## Phases 11–25
- Status: PENDING
