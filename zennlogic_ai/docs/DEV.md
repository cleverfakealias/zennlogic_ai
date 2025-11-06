Developer notes — installing and running locally

This project contains multiple logical components (API, MCP, RAG/worker). To
keep images and developer environments lean, optional dependencies are exposed
as named extras in `pyproject.toml`.

Install options

API-only (fast, suitable for local development and API container builds):

1. Create and activate a venv (PowerShell):
   - python -m venv .venv
   - . .\.venv\Scripts\Activate.ps1
2. Upgrade pip and install the editable package with API and dev extras:
   - pip install --upgrade pip
   - pip install -e ".[api,dev]"

Full stack (includes vector/RAG/aws packages). Use only for developer work
that needs the full ML stack; installs can be slow and may fail on Windows due
to platform-specific wheels:

   pip install -e ".[full,dev]"

Docker image (API)

The API Dockerfile installs only the `api` extras so the image stays small and
avoids heavy ML dependency installs. From the repository root run the build
from the inner package folder where the Dockerfile lives:

   Set-Location .\zennlogic_ai
   docker build -t zennlogic-api:local -f .\docker\api.Dockerfile .

Notes and recommendations
- When running locally on Windows prefer the `.[api,dev]` install in a venv to
  avoid building faiss/sentence-transformers wheels.
- Use the `full` extra inside a Linux dev container or CI runner to avoid wheel
  build issues on Windows.
- Each service (API, MCP, worker) should install only the extras it needs in
  its Dockerfile or runtime environment.

If you want, I can add example Dockerfiles for the MCP and worker images that
install the appropriate extras (for example `pip install .[mcp]` or
`pip install .[vector,aws]`).
