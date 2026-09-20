# Architecture Decisions

## ADR-0001 — Deployment-agnostic Core
- Date: 2026-09-21
- Context: The platform must not be tied to Railway or another single provider.
- Decision: Keep Core/application contracts deployment-agnostic and isolate deployment-specific adapters/configuration.
- Alternatives: provider-specific Core; rejected because it creates lock-in and harms local/VPS/Docker operation.
- Reason: portability, reliability and maintainability.
- Consequences: deployment integration is an adapter concern and must be tested independently.
- Status: ACCEPTED

## ADR-0002 — Telegram is an Interface Layer
- Date: 2026-09-21
- Context: Telegram is the initial user interface but must not define the mathematical architecture.
- Decision: Telegram code may call application interfaces but Core modules must not depend on Telegram.
- Alternatives: Telegram-centric architecture; rejected.
- Reason: testability, future interfaces and clean domain boundaries.
- Consequences: interface DTOs/adapters are required.
- Status: ACCEPTED

## ADR-0003 — Verification is Independent
- Date: 2026-09-21
- Context: Important mathematical results must be trustworthy.
- Decision: Verification is a distinct capability and cannot simply echo the primary solver result.
- Alternatives: trust one solver; rejected.
- Reason: detect incorrect, extraneous, domain-invalid or numerically unstable results.
- Consequences: solver APIs must expose enough evidence for verification.
- Status: ACCEPTED
