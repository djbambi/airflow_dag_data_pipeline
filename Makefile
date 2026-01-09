.PHONY: format lint check fix all

# Format code with ruff
format:
	uv run ruff format .

# Check for linting issues
lint:
	uv run ruff check .

# Run all checks (lint + format check)
check:
	uv run ruff check .
	uv run ruff format --check .

# Auto-fix linting issues
fix:
	uv run ruff check --fix .

# Format and fix all issues
all: fix format
