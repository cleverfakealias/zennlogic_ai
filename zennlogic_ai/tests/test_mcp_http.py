from fastapi.testclient import TestClient

from service.mcp_server.api import app


def test_mcp_http_health_and_tools():
    client = TestClient(app)

    # health
    resp = client.get("/mcp/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    # list tools
    resp = client.get("/mcp/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert "tools" in data
    assert isinstance(data["tools"], list)

    # call health.check via tool invoke
    resp = client.post("/mcp/tools/health/check", json={})
    assert resp.status_code == 200
    assert resp.json()["result"] == {"status": "ok"}
