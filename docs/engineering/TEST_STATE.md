## Runtime integration coverage
- Missing Telegram credential is rejected.
- Provided Telegram credential is loaded.
- Interactive Telegram UI application flows are covered: menu, profile/level, history, exercises, help and settings.
- Secure document validation is covered for image payloads, empty payloads, file-size limits and PDF signature rejection.
- Existing mathematical/OCR/adversarial/phase acceptance suites remain the regression baseline.

## CI evidence
- Run 35623763413 (CI #202) passed all jobs on the final Telegram UI branch head before the document-intelligence expansion.
- Document-layer commits after that run require fresh CI evidence and are therefore not marked verified.

## Required live validation
1. Start `.github/workflows/windows-math-vps.yml` with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`.
2. Verify RDP/Tailscale reachability.
3. Verify Telegram /start and /help.
4. Verify persistent main keyboard and every callback route: solve, exercise, profile, history, settings, help and back navigation.
5. Send representative text problems and confirm verified results where supported.
6. Send clear mathematical photos and verify OCR confidence gating and solving.
7. Send a text PDF, a scanned multi-page PDF, an image-as-document and malformed/oversized files.
8. Observe process/job recovery behavior and record the GitHub-hosted runner time limit.
