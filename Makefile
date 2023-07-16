run:
	uvicorn main:app --reload

linters:
	black --config pyproject.toml models.py main.py conftest.py test_api.py
	isort --sp pyproject.toml models.py main.py conftest.py test_api.py

test:
	pytest
