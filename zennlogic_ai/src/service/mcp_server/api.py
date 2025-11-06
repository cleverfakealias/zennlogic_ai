"""HTTP wrapper for the MCP server.

This module exposes a small FastAPI app that allows invoking registered MCP
tools via HTTP. The MCPServer implementation remains available for in-process
use; this wrapper is optional and designed for deployments where MCP is
exposed over an internal HTTP endpoint.
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service.mcp_server.server import MCPServer
from service.mcp_server.tools import health, s3


app = FastAPI(title="mcp-server")

# Build a server instance and register known tool modules
_server: MCPServer = MCPServer()
_server.register_tool(health)
# Register optional tool modules lazily. Some tools (e.g., rag) pull heavy
# ML/vector dependencies at import time. Import them inside a try/except so
# the HTTP wrapper can start with a minimal image and still provide health
# and S3 tools.
try:
    from service.mcp_server.tools import rag

    _server.register_tool(rag)
except Exception:
    # If rag (or its heavy deps) aren't installed, skip registration.
    # Tests or runtime calls that need rag will see it missing and should
    # return a 404 from the call endpoint.
    pass
_server.register_tool(s3)


class CallBody(BaseModel):
    """Request body for calling an MCP tool function.

    args: optional positional arguments list.
    payload_kwargs: optional keyword arguments mapped from the external JSON
      key "kwargs" (alias) to avoid collisions with internal names.
    """

    args: list[Any] | None = None
    # Use an internal name that avoids any potential module-level name clashes.
    kwargs_: dict[str, Any] | None = None


@app.get("/mcp/health")
def health_check() -> dict[str, str]:
    """Return a minimal health payload for the MCP HTTP wrapper."""
    return {"status": "ok"}


@app.get("/mcp/tools")
def list_tools() -> dict[str, list[str]]:
    """Return the list of registered MCP tool function names."""
    return {"tools": sorted(_server.tools.keys())}


@app.post("/mcp/tools/{tool}/{fn}")
def call_tool(tool: str, fn: str, body: CallBody | None = None) -> dict[str, Any]:
    """Invoke a registered tool function by name.

    The path contains the tool module and function name; the body may
    optionally provide positional `args` and keyword `kwargs`.
    """
    key = fn
    if key not in _server.tools:
        raise HTTPException(status_code=404, detail=f"tool function not found: {key}")

    func_callable = _server.tools[key]
    args = body.args if body and body.args is not None else []
    call_kwargs = body.kwargs_ if body and body.kwargs_ is not None else {}
    try:
        result = func_callable(*args, **call_kwargs)
    except Exception as exc:  # pragma: no cover - surface exceptions in tests
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"result": result}
