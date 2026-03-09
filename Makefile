.PHONY: lint format fix

lint:
	ruff check .

format:
	ruff format .

fix:
	ruff check --fix .
	ruff format .
