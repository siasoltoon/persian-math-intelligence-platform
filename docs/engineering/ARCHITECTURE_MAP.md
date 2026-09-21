# Architecture Map

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
