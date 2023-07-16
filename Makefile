run:
	uvicorn main:app --reload

linters:
	black --config pyproject.toml models.py main.py
	isort --sp pyproject.toml models.py main.py
