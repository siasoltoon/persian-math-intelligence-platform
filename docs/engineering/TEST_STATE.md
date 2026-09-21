## Runtime integration coverage
- Missing Telegram credential is rejected.
- Provided Telegram credential is loaded.
- Interactive Telegram UI application flows are covered: menu, profile/level, history, exercises, help and settings.
- Secure document validation is covered for image payloads, empty payloads, file-size limits, PDF signature rejection, real PDF text extraction and page limits.
- OCR regression coverage includes preprocessing plans, reconstruction, consensus rejection and existing OCR safety contracts.
- Existing mathematical/OCR/adversarial/phase acceptance suites remain the regression baseline.

## CI evidence
- CI #258 / run ID 35629310020 passed all jobs on commit `5e4d37dfc59c82c3a250039b44b00867e71df1a8`.
- Passed: Ruff lint, Ruff format, mypy, pytest Python 3.11 and pytest Python 3.12.
- The final cleanup commit `fb4172f9b8a65b12a9af95699849e862f356b108` removed the temporary formatter diagnostic workflow.
- CI #259 / run ID 356? was the cleanup verification; the current documentation commit CI is tracked separately below.
- CI #262 / run ID 35630145223 passed all jobs on the state-update head.
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
