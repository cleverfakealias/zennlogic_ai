"""MCP RAG tools: search, answer.

These are lightweight shims that call into the RAG pipeline. In minimal
deployments the RAG implementation may not be available; to keep the MCP
HTTP wrapper runnable we return a clear stub response when the pipeline is
unavailable.
"""

from typing import Any


# Pipeline may be unavailable when heavy RAG deps are not installed; keep
# a weakly-typed reference so static analysis is satisfied.
_pipeline: Any = None
try:
    from service.rag.pipeline import RAGPipeline

    _pipeline = RAGPipeline()
except Exception:
    _pipeline = None


def search(query: str, k: int = 5) -> dict[str, Any]:
    """Search vector store for query.

    Returns a mapping with search results or an error message if the
    pipeline isn't available.
    """
    if _pipeline is None:
        return {"error": "rag pipeline not available"}
    return {"results": _pipeline.search(query, k)}


def answer(query: str) -> dict[str, Any]:
    """Answer query using RAG pipeline or return a stub when unavailable."""
    if _pipeline is None:
        return {"error": "rag pipeline not available"}
    return {"answer": _pipeline.answer(query)}
