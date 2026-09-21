# Architecture Map

## Windows VPS + Telegram runtime
- `siasoltoon/vps` operational behavior is integrated through `.github/workflows/windows-math-vps.yml`.
- RDP and Tailscale remain infrastructure concerns; credentials are supplied through GitHub Secrets.
- `src/persian_math/telegram_runtime.py` is the transport adapter and delegates mathematical work to `ApplicationService`.
- Photo input is validated, OCR-processed and confidence-gated before entering the application service.
- The mathematical Core remains Telegram-independent.
- GitHub-hosted Windows runners are ephemeral and time-limited; this runtime is not a guaranteed 24/7 VPS.


## Phase 19–25 additions
- quality.py — failure matrix and bounded retry contract
- ocr_benchmark.py — character/expression/structure OCR metrics
- adversarial.py — explicit mathematical adversarial cases
- ux.py — Persian-first RTL answer rendering policy
- production.py — environment/resource/recovery contracts
- release_audit.py — mandatory release evidence gate
- docs/engineering/PRODUCTION_VERIFICATION_RUNBOOK.md — operational release procedure

## Release boundaries
Repository code can prove deterministic contracts through CI. It cannot substitute for:
- live Telegram/webhook infrastructure
- real OCR labeled images
- production load environment
- backup/restore execution
- external dependency/security scanning evidence

Those are intentionally explicit boundaries and are not hidden inside the mathematical Core.
