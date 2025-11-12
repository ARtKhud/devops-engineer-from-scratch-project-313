start-dev:
	uv run fastapi dev --host 0.0.0.0 --port 8080

install:
	uv sync

fix-lint:
	uv run ruff check . --fix

lint:
	uv run ruff check

test:
	uv run pytest tests
