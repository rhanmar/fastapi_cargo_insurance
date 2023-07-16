run:
	uvicorn app.main:app --reload

linters:
	black --config pyproject.toml app tests
	black --config pyproject.toml app tests

test:
	pytest
