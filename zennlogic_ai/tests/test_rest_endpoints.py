from fastapi.testclient import TestClient

from service.rest.app import app


def test_chat():
    client = TestClient(app)
    resp = client.post("/chat/", json={"messages": [{"role": "user", "content": "hi"}]})
    assert resp.status_code in (200, 401)  # 401 for missing auth


def test_rag_search():
    client = TestClient(app)
    resp = client.get("/rag/search?q=test")
    assert resp.status_code in (200, 401)  # 401 for missing auth
