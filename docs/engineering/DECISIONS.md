# Architecture Decisions

## ADR-0001 — Deployment-agnostic Core
- Date: 2026-09-21
- Decision: Keep Core/application contracts deployment-agnostic and isolate deployment adapters.
- Status: ACCEPTED

## ADR-0002 — Telegram is an Interface Layer
- Date: 2026-09-21
- Decision: Telegram calls application interfaces; Core remains Telegram-independent.
- Status: ACCEPTED

## ADR-0003 — Verification is Independent
- Date: 2026-09-21
- Decision: Important mathematical results require an independent verification capability.
- Status: ACCEPTED

## ADR-0004 — Release Evidence Must Be Explicit
- Date: 2026-09-21
- Context: Phases 19–25 require evidence that cannot be obtained from source-level unit tests alone.
- Decision: External evidence such as labeled OCR data, live integration, load tests and backup/restore execution must be recorded separately and may not be inferred from CI.
- Consequence: A phase remains IMPLEMENTED/VERIFICATION PENDING until its actual acceptance evidence exists.
- Status: ACCEPTED

## ADR-0005 — Windows VPS runtime integration
- Date: 2026-09-21
- Decision: Integrate the operational architecture of `siasoltoon/vps` into this repository through a repository-local Windows workflow and a Telegram runtime adapter.
- Security: credentials are supplied only through GitHub Secrets; the source repository's committed administrator credential is not propagated.
- Runtime: RDP + Tailscale + Tesseract + Telegram polling run in the same Windows job.
- Limitation: GitHub-hosted runners are ephemeral and Actions jobs are time-limited, so this is a disposable runtime rather than a permanent VPS.
- Status: ACCEPTED
