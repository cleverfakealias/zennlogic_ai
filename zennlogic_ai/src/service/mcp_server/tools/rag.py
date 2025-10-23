"""MCP RAG tools: search, answer."""

from zennlogic_ai_service.rag.pipeline import RAGPipeline


pipeline = RAGPipeline()


def search(query: str, k: int = 5):
    """Search vector store for query."""


def answer(query: str):
    """Answer query using RAG pipeline."""
