FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY scripts ./scripts

RUN pip install --upgrade pip \
    && pip install .

COPY docker ./docker
COPY tests ./tests
COPY pre-commit-config.yaml ./
COPY Makefile ./
COPY .env.example ./

ENTRYPOINT ["python", "-m", "app.mcp_server"]
