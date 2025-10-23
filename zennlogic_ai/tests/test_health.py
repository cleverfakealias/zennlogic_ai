from fastapi.testclient import TestClient

from zennlogic_ai_service.rest.app import app


def test_health():
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
