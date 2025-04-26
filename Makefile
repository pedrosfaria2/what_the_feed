SHELL := /bin/bash
PY = python3

UV := uv
PYTHON := $(UV) run python
SERVICE_NAME := $(shell git remote get-url origin | sed 's/.*\/\([^\/]*\)\.git/\1/')

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo " setup        	Install dependencies using UV"
	@echo " run            Run the application"
	@echo " run-docker     Run the application using Docker"
	@echo " run-compose	Run the application with Compose"
	@echo " update       	Update dependencies using UV"
	@echo " lock         	Generate UV lock file"
	@echo " test         	Run tests"
	@echo " test-coverage  Run tests to get coverage"
	@echo " lint         	Lint the code using flake8"
	@echo " format       	Format the code using black"
	@echo " clean        	Clean the project"
	@echo " migrate       	Run database migrations"

.PHONY: migrate
migrate:
	$(UV) run alembic upgrade head

.PHONY: run-docker
run-docker:
	docker build --pull --rm -f infra/Dockerfile -t $(SERVICE_NAME):latest .
	docker run -d --name $(SERVICE_NAME) -p 8003:8003 $(SERVICE_NAME):latest

.PHONY: run-compose
run-compose:
	docker-compose -f infra/docker-compose.yml --env-file .env up

.PHONY: run
run:
	$(PYTHON) src/main.py

.PHONY: setup
setup:
	$(PY) -m venv .venv && source .venv/bin/activate && $(PY) -m pip install --upgrade pip && $(PY) -m pip install uv && $(UV) pip install -e . && pre-commit install -f && pre-commit install --hook-type commit-msg -f
	@echo "To activate the virtual environment in your terminal, run: source .venv/bin/activate"

.PHONY: update
update:
	$(UV) pip sync

.PHONY: lock
lock:
	$(UV) pip compile pyproject.toml -o uv.lock

.PHONY: test
test:
	$(PYTHON) -m pytest

.PHONY: test-coverage
test-coverage:
	$(PYTHON) -m pytest --cov=src --cov-report=term tests/


.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

.PHONY: format
format:
	$(PYTHON) -m black .

.PHONY: clean
clean:
	@rm -rf .pytest_cache
	@rm -rf __pycache__
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*~" -delete
