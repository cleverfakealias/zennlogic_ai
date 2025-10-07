VENV?=.venv

ifeq ($(OS),Windows_NT)
	PYTHON_BIN?=$(VENV)/Scripts/python.exe
else
	PYTHON_BIN?=$(VENV)/bin/python
endif

PIP_BIN?=$(PYTHON_BIN) -m pip

.PHONY: install fmt lint test ingest run-mcp up down clean

install:
	python -m venv $(VENV)
	$(PYTHON_BIN) -m pip install --upgrade pip
	$(PIP_BIN) install .[dev]

fmt:
	$(PYTHON_BIN) -m black app scripts tests

lint:
	$(PYTHON_BIN) -m ruff check app scripts tests
	$(PYTHON_BIN) -m mypy app scripts

test:
	$(PYTHON_BIN) -m pytest -q

ingest:
	$(PYTHON_BIN) -m scripts.build_index

run-mcp:
	$(PYTHON_BIN) -m app.mcp_server

up:
	docker compose up --build

down:
	docker compose down

clean:
	python -c "import pathlib, shutil; [shutil.rmtree(path, ignore_errors=True) for path in ['$(VENV)', '.pytest_cache', '.mypy_cache', '.ruff_cache']]"
