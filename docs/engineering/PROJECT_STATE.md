# Project State

## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasoltoon/persian-math-intelligence-platform
- Default branch: main
- Current version: 0.3.0-dev
- State authority: repository reality + engineering state
- Last state update: 2026-09-21

## Current execution
- Current Phase: Phase 0 — PROJECT FOUNDATION
- Current Task: P0-T02 — Repository/tooling foundation
- Status: IN_PROGRESS
- Last VERIFIED Task: P0-T01 — Repository and engineering state foundation
- Completed Phases: none

## Implementation track
The repository now contains a deployment-agnostic Python mathematical core covering the Phase 1–4 architectural foundations:
- Phase 1 domain entities and typed value objects.
- Phase 2 canonical normalization/parsing for expressions, equations, inequalities, systems and matrices.
- Phase 3 symbolic/numerical solver primitives plus a deterministic SolverRouter.
- Phase 4 independent verification, substitution, domain safety, solution-set checking and method agreement.
- An integrated core processing pipeline connects understanding → representation → solving → verification.

These phases are **NOT VERIFIED yet**. Verification requires green CI plus phase acceptance review.

## Architecture
- Core is deployment-agnostic and interface-independent.
- Telegram remains an interface layer and is not part of the Core.
- Mathematical computation is delegated to specialized symbolic/numerical primitives.
- Independent verification is mandatory for important results.
- No unnecessary agent/microservice architecture is in scope.

## Testing
- Baseline unit, solver and verification tests exist.
- Canonical structure tests and integrated pipeline tests exist.
- CI validates Python 3.11 and 3.12 with Ruff, formatting, mypy and pytest.
- Current latest CI validation is still running.

## Risks / blockers
- Current implementation is broader than the original foundation but Phase 0–4 cannot be marked VERIFIED until the current CI pipeline is green and review/acceptance evidence is recorded.
- Full production breadth of later phases (OCR, Telegram, jobs, security hardening, observability, benchmarks) remains intentionally unimplemented.

## Next action
Monitor the latest CI run. If green, perform Phase 0–4 acceptance review, update all engineering state to VERIFIED where criteria are actually satisfied, and then begin Phase 5.

## Continuation contract
At the beginning of a future session:
1. Read PROJECT_STATE.md, PHASE_STATE.md, TASK_STATE.md and TEST_STATE.md.
2. Confirm repository reality if state conflicts with code.
3. Read ARCHITECTURE_MAP.md / DECISIONS.md / CHANGELOG_ENGINEERING.md only as needed.
4. Locate the current task and last VERIFIED task.
5. Continue from the saved Next action.
6. Do not restart completed work or perform a full repository scan unless state is stale, contradictory or insufficient.
