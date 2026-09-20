# Task State

## P0-T01 — Repository and engineering state foundation
- Phase: 0
- Status: VERIFIED
- Priority: P0
- Objective: Establish durable project specification, roadmap and engineering-state contract.
- Validation: PASS — engineering documents were read back from main after the foundation commit.
- Next action: P0-T02.

## P0-T02 — Repository/tooling foundation
- Phase: 0
- Status: IN_PROGRESS
- Priority: P0
- Objective: Establish implementation structure and quality gates.
- Acceptance Criteria: package structure, configuration boundaries, formatting/lint/typecheck/test commands and CI baseline exist and validate.
- Files Changed: pyproject.toml, Makefile, .gitignore, .env.example, src/persian_math/*, tests/*, .github/workflows/ci.yml.
- Tests: Ruff lint/format, mypy, pytest through CI on Python 3.11 and 3.12.
- Validation: pending final green CI.
- Known Issues: no verified production claim until CI and review pass.
- Dependencies: P0-T01.
- Next action: confirm green CI, then close Phase 0 and verify Phases 1–4.

## P1-T01 — Typed core domain
- Phase: 1
- Status: COMPLETED / VERIFICATION PENDING
- Objective: implement the fixed Phase 1 domain model.
- Acceptance Criteria: all roadmap domain objects represented with typed, immutable core structures.
- Files Changed: src/persian_math/domain.py.
- Tests: integrated through understanding and solver/verification suites.
- Validation: pending phase acceptance.

## P2-T01 — Canonical mathematical representation
- Phase: 2
- Status: COMPLETED / VERIFICATION PENDING
- Objective: normalize and parse core mathematical structures safely.
- Acceptance Criteria: Persian/Arabic input normalization plus expressions, equations, inequalities, systems and matrices.
- Files Changed: src/persian_math/canonical.py, tests/test_canonical.py.
- Validation: pending phase acceptance.

## P3-T01 — Solver engine and router
- Phase: 3
- Status: COMPLETED / VERIFICATION PENDING
- Objective: provide specialized symbolic/numerical solver primitives and deterministic routing.
- Files Changed: src/persian_math/solver.py, tests/test_solver_verification.py.
- Validation: pending phase acceptance.

## P4-T01 — Independent verification
- Phase: 4
- Status: COMPLETED / VERIFICATION PENDING
- Objective: verify important results independently.
- Acceptance Criteria: symbolic/numerical equivalence, substitution, domain safety, residual and solution-set checks, method agreement.
- Files Changed: src/persian_math/verification.py, src/persian_math/engine.py, tests/test_engine.py.
- Validation: pending final CI and review.

## Status rules
PENDING | IN_PROGRESS | BLOCKED | COMPLETED | VERIFIED | FAILED | SUPERSEDED
