.PHONY: format lint test build

format:
	black .

lint:
	flake8 --max-line-length=120 . --exclude .venv,venv

test:
	pytest -q

build:
	docker build -t windturbine:latest .
