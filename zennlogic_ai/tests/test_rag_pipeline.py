from zennlogic_ai_service.rag.models import Document
from zennlogic_ai_service.rag.pipeline import RAGPipeline


def test_rag_pipeline():
    pipeline = RAGPipeline()
    docs = [Document(text="hello", metadata={"id": 1})]
    pipeline.ingest_documents(docs)
    results = pipeline.search("hello", 1)
    assert results
    answer = pipeline.answer("hello")
    assert "answer" in answer
