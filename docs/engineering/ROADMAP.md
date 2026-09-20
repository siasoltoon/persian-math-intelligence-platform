# Phase 0–25 Roadmap

This is the fixed project roadmap referenced by PROJECT_SPECIFICATION.md.

## Phase 0 — PROJECT FOUNDATION
Repository structure, README, engineering docs/state system, Git discipline, environment/config/secrets, CI, formatting/lint/typecheck/basic tests/dependencies/scripts/error handling/logging.

## Phase 1 — CORE DOMAIN MODEL
Problem, ProblemInput, ProblemRepresentation, ProblemClassification, Solution, SolutionStep, VerificationResult, Confidence, EducationalLevel, Difficulty, UserProfile, Exercise.

## Phase 2 — MATHEMATICAL CANONICAL REPRESENTATION
Expressions, equations, inequalities, functions, fractions, powers, roots, systems, matrices, vectors, derivatives, integrals, limits, series, geometry, statistics and probability.

## Phase 3 — MATHEMATICAL SOLVER ENGINE
Arithmetic, algebra, equations, inequalities, polynomials, systems, functions, trigonometry, calculus, derivatives, integrals, limits, linear algebra, probability, statistics, numerical math, number theory, discrete math, complex numbers, optimization and differential equations, with a Solver Router.

## Phase 4 — VERIFICATION ENGINE
Substitution, symbolic equivalence, numerical verification, domain checks, units/dimensions where applicable, independent solving, multi-method comparison, contradiction/extraneous-solution detection, precision checks and evidence-based confidence.

## Phase 5 — INPUT UNDERSTANDING
Persian/English mathematical text, natural language, notation, mixed language, malformed/ambiguous input; intent and mathematical structure extraction.

## Phase 6 — OCR / MATH OCR
Image quality, preprocessing, orientation, deskew, region detection, text/math segmentation, OCR/math OCR, structural reconstruction, canonicalization and validation; printed formulas, fractions, roots, powers, matrices, multiline equations and diagrams; handwriting where feasible.

## Phase 7 — OCR CONSENSUS & CONFIDENCE
Multiple recognition strategies, confidence, disagreement detection, structural validation, ambiguity handling, retry, fallback and user clarification. Never guess.

## Phase 8 — GEOMETRY & VISUAL MATHEMATICS
Figures, points, lines, angles, triangles, circles, coordinate geometry, graphs/charts/axes/labels and visual-to-mathematical representation.

## Phase 9 — PERSIAN EXPLANATION ENGINE
Final answer, solution method, steps, simple/medium/university explanations, notes, common mistakes and verification explanation; all user-facing text Persian.

## Phase 10 — EDUCATIONAL SYSTEM
Elementary, middle school, high school, entrance exam, university, advanced and olympiad levels; adaptive explanation.

## Phase 11 — INTERACTIVE TUTOR
Step-by-step teaching, questions, answer receipt, error detection, hints, re-explanation, simplification and progressive practice.

## Phase 12 — EXERCISE GENERATION
Similar/easier/harder/targeted/topic-specific/level-specific exercises with independent validation before admission.

## Phase 13 — USER LEARNING PROFILE
Solved problems, topics, accuracy, difficulty, mistakes, weak areas, progress and educational recommendations with privacy controls.

## Phase 14 — TELEGRAM BOT
Commands, menus, buttons, text/image/document/PDF, history, settings, education modes, answer checking and exercises with Persian UI.

## Phase 15 — FILE / PDF PIPELINE
PDF and multi-page input, question extraction, page segmentation, math OCR and question indexing, including requests such as “سؤال ۱۵ را حل کن.”

## Phase 16 — PERFORMANCE & JOB SYSTEM
Request → queue → worker → solver → verification → result; timeouts, retries, cancellation, concurrency, rate limiting, prioritization, job status and resource limits.

## Phase 17 — SECURITY
Authentication, authorization, validation, safe file handling, SSRF/injection defenses, resource limits, secrets, dependency security and unsafe execution prevention.

## Phase 18 — OBSERVABILITY
Structured logs, metrics, error tracking, tracing, solver/OCR/verification metrics, latency, queue depth and failure rates.

## Phase 19 — QUALITY / TESTING
Unit, integration, contract, E2E, regression, OCR, solver, verification, security, performance, load and failure-recovery testing.

## Phase 20 — MATHEMATICAL BENCHMARK
Real benchmark across elementary, algebra, geometry, trigonometry, calculus, statistics, probability, linear algebra, discrete math, olympiad, edge and adversarial cases; benchmark each solver.

## Phase 21 — OCR BENCHMARK
Printed, low-quality, rotated, cropped, handwriting, fractions, superscripts/subscripts, nested expressions, matrices and diagrams; character, expression, structural and problem-reconstruction metrics.

## Phase 22 — ADVERSARIAL / FAILURE TESTING
0/0, 1/0, sqrt(-1), log(0), ambiguous minus, nested fractions/radicals, multiple roots, extraneous roots, bad OCR, blurred/rotated images; no crashes and no fabricated answers.

## Phase 23 — UX POLISH
Persian typography, RTL, readability, formulas, buttons, mobile Telegram, long answers, large equations and error/loading/progress states.

## Phase 24 — PRODUCTION HARDENING
Reliability, security, performance, observability, backup/recovery, deployment, config/secrets, CI/CD, rollback and operational documentation.

## Phase 25 — FINAL RELEASE AUDIT
Architecture, code quality, security, reliability, mathematical correctness, OCR, verification, tests, performance, Telegram, UX, documentation, deployment and recovery; no unresolved Critical/High without an explicit decision.
