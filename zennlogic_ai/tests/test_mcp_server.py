def test_mcp_server_smoke():
    """Basic MCP server behavior: register tools and invoke health check."""
    from service.mcp_server.server import MCPServer
    from service.mcp_server.tools import health, rag, s3

    server = MCPServer()
    # register individual tool modules
    server.register_tool(health)
    assert "check" in server.tools
    assert callable(server.tools["check"])
    assert server.tools["check"]() == {"status": "ok"}

    # register other tool modules (functions may be stubs) and ensure keys added
    server.register_tool(rag)
    server.register_tool(s3)
    # ensure at least one function from rag and s3 registered (names may vary)
    assert any(name in server.tools for name in ("search", "answer", "list"))

    # calling main should not raise (it registers and runs)
    # Note: main only logs in this stub implementation
    from service.mcp_server.server import main as mcp_main

    mcp_main()
