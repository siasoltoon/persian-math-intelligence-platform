# Production-Grade Persian Mathematical Intelligence & Tutoring Platform

## 1. Purpose
A production-grade Persian-first mathematical intelligence and tutoring platform. It must reliably understand mathematical input, represent it canonically, solve it with appropriate mathematical engines, independently verify important results, explain the verified result in Persian, and adapt teaching to the learner.

Core principle:

**تشخیص دقیق → نمایش استاندارد → حل تخصصی → Verification مستقل → اطمینان‌سنجی → توضیح فارسی → آموزش متناسب**

This repository is the engineering source of truth for product scope. Runtime truth is the repository code plus the engineering state files.

## 2. Non-negotiable principles
- Mathematical correctness takes priority over speed or presentation.
- Specialized symbolic, numerical, statistical, geometric and domain solvers are the computational source of truth whenever applicable.
- Important results require independent verification before being presented as verified.
- OCR, parsing, solver or verification uncertainty must never be hidden by guessing.
- Core domain and mathematical engines are independent of Telegram and any single deployment provider.
- The platform must be deployment-agnostic: local machine, Docker, VPS, Railway or another infrastructure must not require Core redesign.
- Persian is the default user-facing language and all UX is RTL-friendly. Mathematical notation remains internationally standard.
- Raw exceptions, stack traces and internal implementation details must never be shown to users.
- Store only the minimum user data needed for product functionality.
- Uploaded files/images are untrusted input and must never be executed.
- Avoid unnecessary dependencies, abstractions, microservices and distributed complexity.
- AI/LLM components, if used, are supporting components rather than the mathematical source of truth and must not bypass verification.
- No autonomous-agent architecture is required by this specification.

## 3. Target architecture
Logical layers:
1. Interface layer: Telegram first, with future interfaces possible.
2. Application/API layer: authentication, request orchestration, sessions, jobs and user-facing policies.
3. Core mathematical domain: canonical representations, classification, solvers and verification.
4. Understanding/input layer: text parsing, Persian/English math understanding, OCR and visual mathematics.
5. Education layer: explanation, tutoring, exercises and learning profile.
6. Infrastructure layer: persistence, queue/jobs, observability, security and deployment adapters.

The core must not import Telegram-specific code. Deployment adapters must be replaceable.

## 4. Quality gate
A task is VERIFIED only after implementation, tests, review, integration, validation and documentation/state update. Sensitive features additionally require security, performance and regression validation.

## 5. Phase roadmap
See `ROADMAP.md` for the complete Phase 0–25 roadmap. Phase IDs and scope in that file are fixed unless an Architecture Decision explicitly supersedes them.

## 6. Engineering state
The continuation contract is defined by:
- PROJECT_STATE.md — current snapshot and next action
- PHASE_STATE.md — phase progress
- TASK_STATE.md — task-level progress
- TEST_STATE.md — test evidence
- ARCHITECTURE_MAP.md — actual architecture
- DECISIONS.md — accepted architectural decisions
- CHANGELOG_ENGINEERING.md — important engineering history

Future sessions must read state first and continue from the last verified point rather than restarting the project or rescanning the repository without cause.

## 7. Security and reliability baseline
Consider authentication, authorization, input/file validation, path traversal, SSRF, injection, resource exhaustion, rate abuse, secrets, dependency vulnerabilities, timeouts, retries, cancellation, failure recovery, unsafe execution and backup/recovery from the beginning.

## 8. Definition of Done
Implementation ✓ Tests ✓ Review ✓ Integration ✓ Validation ✓ Documentation ✓ State Update ✓
For sensitive capabilities: Security ✓ Performance ✓ Regression ✓
