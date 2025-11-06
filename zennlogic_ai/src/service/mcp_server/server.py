"""Simple MCP server stub implementation."""

from collections.abc import Callable
import logging
from types import ModuleType
from typing import Any


logger = logging.getLogger(__name__)


class MCPServer:
    """Stub MCP server for development.

    This is a very small in-process tool registry used by the HTTP wrapper
    and by local development. Tools are simple modules exposing callables.
    """

    def __init__(self) -> None:
        """Initialize MCP server."""
        self.tools: dict[str, Callable[..., Any]] = {}

    def register_tool(self, tool_module: ModuleType) -> None:
        """Register a tool module by collecting its public callables.

        Args:
            tool_module: A Python module exposing functions to register.
        """
        # Extract tool functions from the module
        for name in dir(tool_module):
            if not name.startswith("_"):
                func = getattr(tool_module, name)
                if callable(func):
                    self.tools[name] = func

    def run(self) -> None:
        """Run the MCP server (stub)."""
        logger.info("MCP Server running: %s", list(self.tools.keys()))


def main() -> None:
    """Run MCP server with registered tools."""
    server = MCPServer()
    from service.mcp_server.tools import health, rag, s3  # imported for side-effects/registration

    server.register_tool(health)
    server.register_tool(rag)
    server.register_tool(s3)
    server.run()
