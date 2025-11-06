from fastapi.testclient import TestClient

from service.rest.app import app


def test_auth_fail():
    client = TestClient(app)
    resp = client.get("/rag/search?q=test")
    assert resp.status_code == 401  # Missing API key
