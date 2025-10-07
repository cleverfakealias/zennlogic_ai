# LangGraph MCP RAG Server

A reference implementation of a Model Context Protocol (MCP) server that wraps a LangGraph agent, a local retrieval-augmented generation (RAG) stack, and a lightweight note-taking tool. The project is intentionally modular so you can embed the MCP server into any HTTP framework or CLI.

## Features

- ⚡ **fastmcp server** exposing three tools (`rag_search`, `write_note`, `ingest_docs`).
- 🧠 **LangGraph agent** bound to the same RAG tool for direct conversations.
- 📚 **Local FAISS index** backed by LangChain components with OpenAI or deterministic fallback embeddings.
- 🛠️ **Typer CLIs** for ingestion and demo queries.
- 🐋 **Dockerized services** for the MCP server and ingestion worker.
- 🧹 **Pre-commit hooks** with `ruff`, `black`, and `mypy` to keep contributions consistent.

## Quickstart (PowerShell)

```powershell
# 1. Create and activate a virtual environment (Python 3.13)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install the project with development extras
python -m pip install --upgrade pip
python -m pip install ".[dev]"

# 3. Configure environment variables
Copy-Item .env.example .env
# populate OPENAI_API_KEY if you want real embeddings

# 4. Ingest bundled docs into FAISS
python -m scripts.build_index

# 5. Launch the MCP server (stdio transport)
python -m app.mcp_server
```

> **Note:** Without an OpenAI API key, the tooling falls back to deterministic `FakeEmbeddings` so tests and local demos still work—results will be generic but predictable.

## MCP Tools

Once the server is running, try invoking tools from an MCP-capable client:

- `rag_search` — `{"query": "How does this project use LangGraph?"}`
- `write_note` — `{"text": "Investigate Chroma integration next."}`
- `ingest_docs` — `{"glob": "**/*.md"}`

## Swap FAISS for Chroma

The RAG utilities are isolated in `app/tools`. To switch vector stores:

1. Replace FAISS imports with your preferred backend (e.g., `langchain_community.vectorstores import Chroma`).
2. Update `build_index` to instantiate the new store and persist metadata accordingly.
3. Adjust Dockerfiles to include any additional system dependencies.
4. Run `make ingest` to rebuild the index.

## Development Workflow

```powershell
# Core tasks (PowerShell friendly)
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[dev]"
.\.venv\Scripts\python.exe -m black app scripts tests
.\.venv\Scripts\python.exe -m ruff check app scripts tests
.\.venv\Scripts\python.exe -m mypy app scripts
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m scripts.build_index
.\.venv\Scripts\python.exe -m app.mcp_server

# Optional Docker workflows
docker compose up --build
docker compose down
```

> Prefer `make`? Install GNU Make (e.g., `winget install GnuWin32.Make`) and use the provided `Makefile` targets instead of the individual commands above.

## Project Layout

```
mcp-langgraph-rag/
  app/                 # core application modules
  scripts/             # Typer-based CLI utilities
  tests/               # pytest suite
  docker/              # container builds for MCP + ingestion
```

The architecture intentionally keeps HTTP frameworks optional—drop `app.mcp_server` into a FastAPI/Starlette task if you want REST endpoints later.
