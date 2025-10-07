from __future__ import annotations

"""Basic smoke tests for the MCP server setup."""

from fastmcp.server import FastMCP

from app.mcp_server import REGISTERED_TOOL_NAMES, server


def test_server_tools_registered() -> None:
    expected = {"rag_search", "write_note", "ingest_docs"}
    assert expected.issubset(REGISTERED_TOOL_NAMES)


def test_server_instance() -> None:
    assert isinstance(server, FastMCP)
