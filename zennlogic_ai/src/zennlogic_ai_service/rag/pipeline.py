"""RAG pipeline: ingest, search, answer."""

import os
from typing import Any

import numpy as np

from zennlogic_ai_service.config import settings
from zennlogic_ai_service.rag.embeddings import Embeddings
from zennlogic_ai_service.rag.models import Document
from zennlogic_ai_service.rag.vector_backends.factory import get_vector_backend


class RAGPipeline:
    """RAG pipeline for document ingestion and querying."""

    def __init__(self, dim: int = 384) -> None:
        """Initialize RAG pipeline."""
        self.embeddings = Embeddings()
        self.vector_store = get_vector_backend(dim)

    def ingest_documents(self, docs: list[Document]) -> dict[str, int]:
        """Ingest documents into vector store."""
        texts = [doc.text for doc in docs]
        metadatas = [doc.metadata for doc in docs]
        self.embeddings.embed(texts)  # Compute embeddings (for consistency, though not stored)
        self.vector_store.add(texts, metadatas)
        os.makedirs(os.path.dirname(".data/vector/index"), exist_ok=True)
        self.vector_store.persist(".data/vector/index")
        # Optionally push to S3
        return {"count": len(texts)}

    def search(self, query: str, k: int = 5) -> list[tuple[str, dict[str, object], float]]:
        """Search for relevant documents using FAISS only."""
        query_vec = self.embeddings.embed([query])[0]
        vec = np.array(query_vec)
        return self.vector_store.search(vec, k)

    def answer(self, query: str) -> Any:
        """Answer query using retrieved documents."""
        results = self.search(query, settings.top_k)
        # Minimal answer stub
        return {"answer": results[0][0] if results else "", "sources": [r[1] for r in results]}
