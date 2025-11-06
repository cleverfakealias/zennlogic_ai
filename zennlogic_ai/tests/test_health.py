from fastapi.testclient import TestClient

from service.rest.app import app


def test_health():
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
