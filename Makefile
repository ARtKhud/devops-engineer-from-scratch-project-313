start-dev:
	export ENVIRONMENT=development && uv run fastapi dev --host 0.0.0.0 --port 8080 

install:
	uv sync --no-dev

fix-lint:
	uv run ruff check . --fix

lint:
	uv run ruff check

test:
	export ENVIRONMENT=development && uv run pytest tests

install-dev:
	uv sync 