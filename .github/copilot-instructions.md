Project Context
Purpose: Applied AI RAG/chat service (REST API + optional MCP server).

Runtime: Python ≥ 3.12

Core Libraries: FastAPI, Uvicorn, httpx, LangChain/LangGraph/LangSmith, FAISS, sentence-transformers, NumPy/SciPy, boto3/botocore

Infra & DX: pydantic v2, structlog, python-dotenv, pytest (+ pytest-cov), mypy (strict), ruff (lint+format), pre-commit, optional litellm

Copilot: Generate code and tests consistent with these tools and versions.

Ground Rules (Non-Negotiable)
Style & Lint: Obey Ruff rules (line-length=100, Google docstrings, import order). Prefer double quotes.
Types: Pass mypy --strict. Use precise types, TypedDict/Protocol when helpful, pydantic v2 models for IO boundaries.
Logging: No print. Use structlog. Log with event-style keys; never interpolate f-strings.
Errors: Raise explicit exceptions. Use FastAPI error handlers with typed pydantic error payloads.
Config: Read env via python-dotenv once at startup. Centralize settings in a pydantic BaseSettings class.
HTTP: Use httpx clients with timeouts, retries/backoff, and context-managed lifetimes. No global clients.
RAG: Keep embedding, indexing, and retrieval modular/testable, separated from FastAPI routes.
Concurrency: Prefer async endpoints. Avoid blocking CPU work in the event loop.
Security: Never log secrets. Validate all external inputs. Timebox model calls. Add CORS only if needed.
Folder Structure
FastAPI Patterns
Use an app factory (create_app()).
Dependencies from api/deps.py.
Error responses: pydantic models (e.g., ErrorResponse with code, message).
Configuration Example
Logging Example
Usage:

HTTP Client Example
RAG Boundaries
embeddings.py: async/threaded adapter for sentence-transformers.
index_faiss.py: pure functions for build/load/search; persist to settings.index_path.
retriever.py: interface retrieve(query_text, k=5) -> list[DocChunk] (FAISS/Annoy abstraction).
graph.py: LangGraph orchestration only; IO via provider adapters.
LLM Providers
Typed interface, e.g.:
Adapters for OpenAI, Bedrock, LiteLLM. Use timeouts, retries, safe logging.
Testing Best Practices
Use pytest + httpx.ASGITransport + asgi_lifespan for app tests.
Unit tests for RAG: no network calls; use deterministic fixtures.
Use moto for AWS stubs.
High, meaningful coverage (--cov=src/zennlogic_ai_service --cov-report=term-missing).
What Not to Generate
No monolithic “God” classes or sprawling utils.
No global httpx clients or mutable state.
No untyped functions, print debugging, or secret values in code/logs.
No “example notebooks” or placeholder demo routes.
Copilot Prompt Patterns
Use short, explicit scaffolding comments above code:

Commit Hygiene
Keep commits small and descriptive.
Update tests alongside code.
If public signature changes, add/adjust a test.
Pre-commit
Ensure hooks run ruff, mypy, trailing whitespace.
Code must format cleanly and type-check before merging.
