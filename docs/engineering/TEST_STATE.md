## Runtime integration coverage
- Missing Telegram credential is rejected.
- Provided Telegram credential is loaded.
- Interactive Telegram UI application flows are covered: menu, profile/level, history, exercises, help and settings.
- Secure document validation is covered for image payloads, empty payloads, file-size limits, PDF signature rejection, encrypted PDF rejection, real PDF text extraction, page limits and pixel limits.
- Document regression coverage now includes a scanned-like PDF whose native text layer contains only `Scanned by CamScanner`; accepted OCR replaces that sparse/watermark-only layer instead of being concatenated with it.
- Low-confidence OCR is rejected as problem text rather than promoted to a solver input.
- OCR regression coverage includes preprocessing plans, reconstruction, consensus rejection and existing OCR safety contracts.
- Mathematical parser security coverage rejects Python-expression syntax and oversized mathematical inputs.
- Verification coverage includes deterministic numeric re-evaluation and an alternate `solveset` equation verification path.
- Existing mathematical/OCR/adversarial/phase acceptance suites remain the regression baseline.

## CI evidence
- CI #278 / run ID 35634158094 passed all jobs on commit `46c4d7552122398e32bc25b997d15ba1481c1d92`.
- Passed: Ruff lint, Ruff format, mypy, pytest Python 3.11 and pytest Python 3.12.
- The hardening branch was merged to main as `b573f1078edc8f864a7e9371fb4492fd8dbef729`.
- Earlier failed CI runs #271–#277 were diagnosis iterations and are not release evidence.
- No failed CI run is treated as release evidence.

## Required live validation
1. Start `.github/workflows/windows-math-vps.yml` with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`.
2. Verify RDP/Tailscale reachability.
3. Verify Telegram /start and /help.
4. Verify persistent main keyboard and every callback route: solve, exercise, profile, history, settings, help and back navigation.
5. Send representative text problems and confirm verified results where supported.
6. Send clear, degraded and difficult mathematical photos; verify OCR confidence and consensus rejection behavior.
7. Send a text PDF, a scanned multi-page PDF, a mixed text/image PDF, an image-as-document and malformed/oversized files.
8. Observe process/job recovery behavior and record the GitHub-hosted runner time limit.
