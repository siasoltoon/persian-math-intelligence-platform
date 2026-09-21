# Project State

## Identity
- Project: Production-Grade Persian Mathematical Intelligence & Tutoring Platform
- Repository: siasoltoon/persian-math-intelligence-platform
- Current execution date: 2026-09-21
- Current target: Phase 19–25 hardening/release audit
- Status: Repository-level hardening implemented; external-environment evidence remains required for full release verification
- Last CI-tested commit: e84744b85941c46298c3221f4288c51d3919ed31

## Phase 19–25 implementation
- P19 quality matrix, retry/failure contracts and acceptance suite added.
- P20 benchmark result execution and representative corpus tests retained.
- P21 OCR benchmark metrics added for character/expression/structure scoring.
- P22 adversarial mathematical cases added with no-crash behavior tests.
- P23 Persian RTL/UI policy and verified/unverified answer rendering added.
- P24 production configuration, resource limits and recovery-policy contracts added.
- P25 release-audit gate and production verification runbook added.

## Current verification evidence
- CI run 35574264424 reached: Ruff lint PASS, mypy PASS, pytest 3.11 PASS, pytest 3.12 PASS.
- Ruff format failed on the run because two final formatting commits landed after that run's tested SHA.
- Therefore the repository is NOT marked fully VERIFIED yet.

## External evidence still required by the fixed roadmap
- Real labeled OCR image corpus and measured OCR accuracy
- Live Telegram/webhook integration test
- Distributed worker/concurrency/load evidence
- Full SSRF/DNS-rebinding/security/dependency audit
- Production-like performance/load measurements
- Backup/restore and rollback execution evidence
- Comprehensive real mathematical benchmark across every roadmap solver family

No evidence is fabricated. These items require the corresponding runtime environment or labeled data.

## Next action
Run CI on the latest HEAD after the final formatting changes, then close only the evidence-backed P19–25 gates.
