# Heavy OCR GitHub Worker

This project currently keeps heavyweight visual-recognition execution on GitHub-hosted Actions rather than requiring a dedicated PC worker.

## Runtime

- Core dependencies remain in `pyproject.toml`.
- Heavy OCR dependencies are isolated in `requirements-heavy-ocr.txt`.
- `.github/workflows/heavy-ocr-worker.yml` installs Tesseract, PyTorch, Transformers, TrOCR support and pix2tex, then runs the full regression suite and heavyweight runtime smoke checks.
- Hugging Face artifacts are cached between workflow runs; model weights are never committed to Git.
- TrOCR is prefetched into the workflow cache so `local_files_only=true` can be used during inference after preparation.
- The workflow is CPU-safe and uses the standard `ubuntu-latest` runner. GitHub currently documents that standard public-repository Ubuntu runners provide 4 vCPUs, 16 GB RAM and 14 GB SSD; larger runners are available separately when needed.

## Production boundary

The GitHub-hosted worker is the temporary compute target. It is not treated as a permanent always-on worker: each hosted job runs in a fresh VM and is decommissioned after completion. The later PC worker can adopt the same isolated heavy dependency file and backend contract without changing the Core/application architecture.

## Verification boundary

A successful workflow proves that the heavyweight runtime can be installed, imported, model-loaded and regression-tested. It does not by itself prove production OCR accuracy. That still requires a labeled real-world handwriting/formula corpus and measured character, expression and structural metrics.
