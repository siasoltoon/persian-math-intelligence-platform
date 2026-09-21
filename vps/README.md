# Windows VPS runtime

This directory contains the repository-local runtime integration for the Windows GitHub Actions runner used by the original `siasoltoon/vps` project.

Source repository: https://github.com/siasoltoon/vps

The source workflow is preserved conceptually, but credentials are intentionally supplied through GitHub Secrets instead of being committed to source control.

Required secrets:
- `TAILSCALE_AUTHKEY`
- `RDP_PASSWORD`
- `TELEGRAM_BOT_TOKEN`

The integrated workflow is `.github/workflows/windows-math-vps.yml`.
