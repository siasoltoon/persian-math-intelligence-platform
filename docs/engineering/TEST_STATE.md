## Runtime integration coverage
- Missing Telegram credential is rejected.
- Provided Telegram credential is loaded.
- Interactive Telegram UI application flows are covered: menu, profile/level, history, exercises, help and settings.
- Secure document validation is covered for image payloads, empty payloads, file-size limits, PDF signature rejection, encrypted PDF rejection, real PDF text extraction, page limits and pixel limits.
- Document regression coverage includes a scanned-like PDF whose native text layer contains only `Scanned by CamScanner`; accepted OCR replaces that sparse/watermark-only layer instead of being concatenated with it.
- Low-confidence OCR is rejected as problem text rather than promoted to a solver input.
- OCR regression coverage includes preprocessing plans, reconstruction, consensus rejection, extreme-degradation preprocessing requirements, poor-source classification, structural fraction/power/matrix detection and strict handwriting-backend corroboration.
- Mathematical parser security coverage rejects Python-expression syntax and oversized mathematical inputs.
- Verification coverage includes deterministic numeric re-evaluation and an alternate `solveset` equation verification path.
- Existing mathematical/OCR/adversarial/phase acceptance suites remain the regression baseline.

## CI evidence
- PR #8 CI #304 / run ID 35643936787 passed all jobs on commit `1845722758b2ac85a17601d7122fccf745a469ec`.
- Main CI #305 / run ID 35644040284 passed all jobs on merge commit `d41fe316ab6b94375cd21a87c90272e0a20086d5`.
- No failed CI run is treated as release evidence.

## Required live validation
1. Start `.github/workflows/windows-math-vps.yml` with `TAILSCALE_AUTHKEY`, `RDP_PASSWORD`, and `TELEGRAM_BOT_TOKEN`.
2. Verify RDP/Tailscale reachability.
3. Verify Telegram /start and /help.
4. Verify persistent main keyboard and every callback route: solve, exercise, profile, history, settings, help and back navigation.
5. Send representative text problems and confirm verified results where supported.
6. Send clear, degraded and difficult mathematical photos; verify OCR confidence, structure warnings and consensus rejection behavior.
7. Send a text PDF, a scanned multi-page PDF, a mixed text/image PDF, an image-as-document and malformed/oversized files.
8. Run the labeled OCR/handwriting corpus and record character, expression and structural accuracy.
9. Observe process/job recovery behavior and record the GitHub-hosted runner time limit.
