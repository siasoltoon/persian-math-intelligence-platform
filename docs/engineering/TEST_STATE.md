## Runtime integration coverage
- Missing Telegram credential is rejected.
- Provided Telegram credential is loaded.
- Existing mathematical/OCR/adversarial/phase acceptance suites remain the regression baseline.

## CI evidence
- Previous CI run 35574264424 tested an earlier SHA.
- A fresh CI run is required for the runtime integration commits.

## Required live validation
1. Start `.github/workflows/windows-math-vps.yml` with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`.
2. Verify RDP/Tailscale reachability.
3. Verify Telegram `/start` and `/help`.
4. Send representative text problems and confirm verified results where supported.
5. Send a clear mathematical photo and verify OCR confidence gating and solving.
6. Observe process/job recovery behavior and record the GitHub-hosted runner time limit.
