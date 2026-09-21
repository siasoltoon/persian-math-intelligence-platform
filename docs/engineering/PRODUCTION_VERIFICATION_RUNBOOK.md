# Production Verification Runbook

## Release gate
A release candidate must have:
1. CI green on Python 3.11 and 3.12.
2. Ruff lint and format green.
3. mypy green.
4. Full pytest suite green.
5. Mathematical benchmark report recorded.
6. OCR benchmark report recorded with character/expression/structure metrics.
7. Adversarial matrix green with explicit rejected/unsupported cases.
8. Security review covering input bounds, path traversal, SSRF/private-address handling, unsafe execution and dependency review.
9. Performance/load evidence recorded for the target deployment profile.
10. Backup/restore and rollback evidence recorded.
11. UX/RTL regression evidence recorded.
12. Release audit with no unresolved Critical/High blockers unless explicitly accepted in DECISIONS.md.

## Phase 19 — Quality
Run unit, integration, contract, regression, failure-recovery and load suites. A passing unit suite alone is insufficient.

## Phase 20 — Mathematical benchmark
Benchmark every supported solver family using representative, edge and adversarial cases. Record exact expected outputs and pass rates; do not infer correctness from aggregate scores alone.

## Phase 21 — OCR benchmark
Use labeled samples for printed, degraded, rotated, cropped, handwriting, fractions, powers, nested expressions, matrices and diagrams. Record character, expression and structural accuracy separately. Unsupported recognition must be rejected rather than guessed.

## Phase 22 — Adversarial/failure
Exercise undefined domains, malformed notation, ambiguous OCR, oversized inputs, transient backend failures, cancellation and retry paths. Verify no raw exception reaches users.

## Phase 23 — UX
Verify Persian-first RTL rendering, mathematical LTR notation, long answers, mobile-sized messages, loading/error/progress states and verified/unverified result distinction.

## Phase 24 — Production hardening
Validate environment configuration, resource limits, graceful shutdown, deployment adapter isolation, secrets handling, backups, restore verification, rollback and operational observability.

## Phase 25 — Final release audit
Build the release audit from recorded evidence. The audit is a gate, not a score: missing evidence blocks release.

## Current limitation
Automated repository CI can prove source-level contracts and regression behavior. It cannot prove a live Telegram webhook, a particular production provider, real-world OCR accuracy or infrastructure load without the corresponding environment and labeled datasets. Such evidence must be recorded when that environment is available; it must not be fabricated.
