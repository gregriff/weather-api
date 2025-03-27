# these are for development only. refer to readme for installation instructions

# use this after adding new packages to pyproject.toml
lock:
	uv pip compile --generate-hashes -o requirements.txt pyproject.toml

# install all project and dev dependencies in a development venv
install:
	uv pip install -r requirements.txt

run:
	uv run uvicorn api.main:app \
	--reload --reload-include '*.env.json' \
	--loop uvloop --log-level debug

lint:
	ruff check --fix

format: lint
	ruff format


.PHONY: install format lock run lint format
