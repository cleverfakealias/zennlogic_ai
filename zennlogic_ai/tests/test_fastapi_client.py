"""Test the FastAPI app with built-in TestClient."""

from fastapi.testclient import TestClient

from zennlogic_ai_service.rest.app import app


client = TestClient(app)


def test_health_check():
    """Test basic health check endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_requires_auth():
    """Test that chat endpoint requires authentication."""
    response = client.post("/chat/", json={"messages": [{"role": "user", "content": "Hello"}]})
    assert response.status_code == 401  # Should fail without API key


def test_rag_endpoints_require_auth():
    """Test that RAG endpoints require authentication."""
    # Test search
    response = client.get("/rag/search?q=test&k=1")
    assert response.status_code == 401

    # Test ingest
    response = client.post("/rag/ingest", json=[])
    assert response.status_code == 401

    # Test answer
    response = client.post("/rag/answer", json="test query")
    assert response.status_code == 401
