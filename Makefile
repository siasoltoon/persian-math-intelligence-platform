test:
	python -m pytest

lint:
	ruff check .

format:
	ruff format --check .

typecheck:
	mypy src

quality: lint format typecheck test
