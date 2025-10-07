# FastAPI Copilot Instructions

> These guidelines teach Copilot how to draft Python code and documentation that align with production-grade FastAPI API services. Favor modern, secure, asynchronous patterns.

## General expectations

- Assume Python 3.13+ and FastAPI. Prefer standard library features before external packages.
- Always generate fully typed code (function annotations, TypedDict/`pydantic` models, `Enum` where meaningful).
- Default to asynchronous functions (`async def`) for request handlers and data-access calls unless blocking work is unavoidable.
- Embrace immutability where practical; avoid hidden side effects.
- Include concise docstrings and inline comments that clarify intent, not restate code.

## Environment specifics

- Author workflow happens on Windows (PowerShell 5.1). Use Windows-friendly commands and path separators.
- Chain commands with `;` instead of `&&`, and prefer cmdlets such as `Remove-Item -Recurse -Force` over `rm -rf`.
- When illustrating filesystem commands, rely on `New-Item`, `Copy-Item`, `Get-ChildItem`, or `python -m` utilities that work cross-platform.

## Project layout

Structure generated files using a layered FastAPI project layout:

```
app/
  main.py            # FastAPI app factory, startup/shutdown hooks
  api/
    __init__.py
    v1/
      __init__.py
      routers.py     # APIRouter instances grouped by domain
  core/
    config.py        # `BaseSettings` application settings
    security.py      # auth utilities
  services/
    ...              # business logic services
  repositories/
    ...              # persistence access layer
  schemas/
    ...              # pydantic request/response models
  db/
    session.py       # database session management
```

- Keep FastAPI route declarations thin; delegate business logic to services.
- Centralize startup, shutdown, middleware, CORS, and exception wiring in `main.py`.
- Use dependency overrides in tests instead of monkeypatching modules.

## API surface design

- Always expose routes through `APIRouter` instances mounted in a versioned namespace (e.g., `/api/v1`).
- Name handlers using verbs (`create_user`, `list_orders`).
- Define `response_model` and explicit status codes for each endpoint.
- Validate request payloads with Pydantic models. Use `Config` / `model_config` to enable `from_attributes=True` when mapping ORM entities.
- Favor `Enum` classes for finite sets of values.

## Validation & serialization

- Leverage Pydantic validators, `Field` constraints, and `Annotated` types for strict schemas.
- Avoid returning ORM models directly; convert to Pydantic models.
- Use `datetime` with TZ awareness (`datetime.datetime` with `timezone.utc`).
- Provide examples via `model_config = ConfigDict(json_schema_extra={"example": {...}})` to improve OpenAPI docs.

## Dependency management

- Use FastAPI `Depends` for request-scoped resources (database sessions, authenticated user, settings).
- Implement configuration with `BaseSettings`, environment variable prefixes, and `.env` loading via `pydantic-settings`.
- For expensive dependencies, create startup-shared singletons and inject lightweight callables per request.

## Error handling

- Raise `HTTPException` with descriptive `detail` payloads.
- Implement custom exception classes and register handlers with `app.exception_handler` to normalize error envelopes.
- Return problem-details JSON `{ "type": "...", "title": "...", "detail": "...", "status": 400, "instance": "..." }` where suitable (RFC 7807).

## Security & auth

- Prefer OAuth2 with JWT bearer tokens (`OAuth2PasswordBearer`).
- Hash passwords using `passlib`'s `bcrypt` or `argon2` and store salted hashes only.
- Apply role/permission checks in dependencies, not in route bodies.
- Sanitize and log security-relevant events (auth failures, permission denials) without leaking secrets.

## Persistence & async operations

- Default to async database drivers (`asyncpg`, `SQLAlchemy 2.0 AsyncSession`).
- Wrap blocking I/O (e.g., legacy SDKs) in `run_in_threadpool`.
- Reuse connection pools; manage sessions with context managers injected via dependencies.

## Observability & logging

- Configure structured logging (JSON) at info level by default.
- Include request tracing middleware (`X-Request-ID` headers, `contextvars`).
- Emit metrics via OpenTelemetry or Prometheus exporters; instrument `@router` handlers and services.

## Documentation & DX

- Document every endpoint with a summary and description (`@router.get(..., summary="", description="")`).
- Supply OpenAPI response examples for key success and error cases.
- Provide inline usage examples in docstrings for shared utilities where clarity matters.

## Testing strategy

- Use `pytest` with `pytest-asyncio` for async coverage and `httpx.AsyncClient` for integration tests.
- Mock external services at the boundary (e.g., using `respx` for HTTP clients).
- Cover happy path, validation errors, authorization failures, and integration with the persistence layer.
- Keep fixtures deterministic; seed random data with fixed values.

## Performance & resilience

- Prefer pagination over unbounded list endpoints. Support cursor or page-number patterns.
- Apply timeouts and retries (e.g., `tenacity`) on outbound network calls, with exponential backoff.
- Use background tasks (`BackgroundTasks`) for non-critical work; for heavy workloads, emit to a task queue (Celery, RQ, Dramatiq).
- Guard against thundering herds with caching (`fastapi-cache`, Redis) where justified.

## Tooling & style

- Format with `ruff` or `black` and lint with `ruff` (including complexity checks).
- Run `mypy` in strict mode; silence or refactor code rather than ignore type errors.
- Keep dependencies pinned in `pyproject.toml`/`poetry.lock` or `requirements.txt`.

## Pull request expectations

- Each change should include updated tests and documentation when behavior changes.
- Keep functions small, single-purpose, and covered by tests.
- Mention architectural decisions in ADRs or the project README when introducing new patterns.

Following these rules ensures Copilot outputs production-quality FastAPI code that is maintainable, secure, and well-instrumented.
