"""RAG endpoints: ingest, search, answer."""

from typing import Any

from fastapi import APIRouter, Body, Query

from service.config import settings
from service.rag.models import Document
from service.rag.pipeline import RAGPipeline


router = APIRouter()
pipeline = RAGPipeline()

# Module-level singleton for Body default
DEFAULT_BODY = Body(...)


@router.post(
    "/ingest", summary="Ingest documents", description="Add docs to vector store and persist."
)
def ingest_docs(docs: list[Document] = DEFAULT_BODY) -> Any:
    """Ingest documents into vector store and persist index."""
    return pipeline.ingest_documents(docs)


@router.get("/search", summary="Vector search", description="Search vector store.")
def search(q: str = Query(...), k: int = Query(settings.top_k)) -> Any:
    """Search vector store for query."""
    results = pipeline.search(q, k)
    return [{"text": text, "metadata": meta, "score": score} for text, meta, score in results]


@router.post("/answer", summary="RAG answer", description="Answer via retriever + LLM.")
def answer(q: str = DEFAULT_BODY) -> Any:
    """Answer query using RAG pipeline."""
    return pipeline.answer(q)
