"""MCP health tool."""


def check() -> dict[str, str]:
    """Check service health status.

    Returns a simple status mapping to be consumed by MCP clients.
    """
    return {"status": "ok"}
