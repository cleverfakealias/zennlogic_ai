#!/usr/bin/env bash
set -e
uv sync
uv run pre-commit install
cp .env.example .env
