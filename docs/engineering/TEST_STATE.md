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

## Specialized OCR evidence
- CI run #315: Ruff lint ✓, Ruff format ✓, mypy ✓, pytest Python 3.11 ✓, pytest Python 3.12 ✓.
- Specialized backend tests cover missing optional dependencies, environment defaults, safe formula validation, conflicting formula rejection and matching formula consensus.
- Model inference itself is intentionally not claimed as verified by CI because heavyweight model artifacts are not downloaded into the repository CI environment.
- Required next evidence: model-backed benchmark with real handwritten Persian/Latin/math samples, difficult formulas and structural accuracy metrics.


## GitHub-hosted heavy OCR evidence
- Added .github/workflows/heavy-ocr-worker.yml for heavyweight runtime installation and smoke verification.
- The workflow caches Hugging Face artifacts and preloads microsoft/trocr-base-handwritten without committing model weights.
- It runs the complete regression suite before heavyweight backend checks.
- Pending evidence: the first successful heavy workflow run and measured real-world OCR/handwriting/formula benchmark metrics.


## GitHub-hosted heavy OCR evidence
- Heavy OCR workflow run 35649732688: success. Regression suite: 95 passed; TrOCR model load: success; specialized backend construction: success; CPU-safe runtime check: success.
- Main CI run 35649997963: success. Ruff lint, Ruff format, mypy, pytest Python 3.11, pytest Python 3.12 and Heavy OCR runtime all passed.
- First heavy run 35649274960 failed because the workflow smoke test referenced a nonexistent available() method; the check was corrected and replacement run 35649732688 passed.
- Heavy runtime is verified as installable/model-loadable on GitHub-hosted Actions; production accuracy is still not claimed.


## Plain-text Telegram math input regression — 2026-09-22
- Root cause reproduced from live behavior: natural-language Persian wrappers reached the restricted parser instead of first being reduced to a safe mathematical payload.
- Added regression tests for arithmetic and linear-equation Persian prompts, including independent verification assertions.
- Current status: code-level regression coverage added; CI/live Telegram execution evidence still required before marking the task VERIFIED.
