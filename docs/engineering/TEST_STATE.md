## Runtime integration coverage
- Missing Telegram credential is rejected.
- Provided Telegram credential is loaded.
- Interactive Telegram UI application flows are covered: menu, profile/level, history, exercises, help and settings.
- Existing mathematical/OCR/adversarial/phase acceptance suites remain the regression baseline.

## CI evidence
- Run 35623763413 (CI #202) passed all jobs on the final Telegram UI branch head:
  - Ruff lint: success
  - Ruff format: success
  - Mypy: success
  - Pytest Python 3.11: success
  - Pytest Python 3.12: success
- The final UI change was merged to main as merge commit `f17d65f1409f333789066e00c3c775c083483887`.

## Required live validation
1. Start `.github/workflows/windows-math-vps.yml` with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`.
2. Verify RDP/Tailscale reachability.
3. Verify Telegram /start and /help.
4. Verify persistent main keyboard and every callback route: solve, exercise, profile, history, settings, help and back navigation.
5. Send representative text problems and confirm verified results where supported.
6. Send a clear mathematical photo and verify OCR confidence gating and solving.
7. Observe process/job recovery behavior and record the GitHub-hosted runner time limit.
