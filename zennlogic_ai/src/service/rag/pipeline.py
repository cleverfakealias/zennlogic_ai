"""RAG pipeline: ingest, search, answer."""

import os
from typing import Any, cast

import numpy as np

from service.config import settings
from service.rag.embeddings import Embeddings
from service.rag.models import Document
from service.rag.vector_backends.factory import get_vector_backend


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
        vectors = np.array(self.embeddings.embed(texts), dtype=np.float32)
        # Add vectors + payloads to the underlying index
        if hasattr(self.vector_store, "add_vectors"):
            self.vector_store.add_vectors(vectors, texts, metadatas)
        else:  # pragma: no cover - legacy path
            self.vector_store.add(texts, metadatas)
        os.makedirs(".data/vector", exist_ok=True)
        self.vector_store.persist(".data/vector/index")
        # Optionally push to S3
        return {"count": len(texts)}

    def search(self, query: str, k: int = 5) -> list[tuple[str, dict[str, object], float]]:
        """Search for relevant documents using FAISS only."""
        query_vec = self.embeddings.embed([query])[0]
        vec = np.array(query_vec, dtype=np.float32)
        # Underlying vector backend returns a runtime list/tuple structure.
        # Cast to the declared return type for static checking.
        return cast(
            list[tuple[str, dict[str, object], float]],
            self.vector_store.search(vec, k),
        )

    def answer(self, query: str) -> Any:
        """Answer query using retrieved documents."""
        results = self.search(query, settings.top_k)
        # Minimal answer stub
        return {"answer": results[0][0] if results else "", "sources": [r[1] for r in results]}
