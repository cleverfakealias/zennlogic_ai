from __future__ import annotations

"""Utility functions for querying the local FAISS index."""

from dataclasses import dataclass
from pathlib import Path
from textwrap import shorten

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from rich.console import Console

from app.settings import get_settings
from app.tools.ingest import get_embeddings

console = Console()


@dataclass(slots=True)
class SearchResult:
    """Normalized representation of a similarity search match."""

    source: str
    preview: str
    score: float | None = None


_VECTOR_STORE_CACHE: dict[Path, FAISS] = {}
_EMBEDDINGS = None


def search(query: str, k: int = 4, *, index_dir: Path | None = None) -> str:
    """Run a similarity search and format the results for MCP clients."""

    settings = get_settings()
    target_dir = Path(index_dir).expanduser() if index_dir else settings.index_dir.expanduser()
    if not target_dir.exists():
        raise FileNotFoundError(
            f"Index directory {target_dir} was not found. Run the ingest step first."
        )

    store = _load_index(target_dir)
    matches = store.similarity_search(query, k=k)
    if not matches:
        return f"No matches found for '{query}'."

    normalized = [_normalize_document(doc) for doc in matches]
    answer = _synthesize_answer(normalized)
    bullets = "\n".join(
        f"- **{result.source}** — {result.preview}" for result in normalized
    )
    return f"### Answer\n{answer}\n\n### Matches\n{bullets}"


def _load_index(index_dir: Path) -> FAISS:
    """Load and cache the FAISS index residing at ``index_dir``."""

    global _EMBEDDINGS
    index_dir = index_dir.expanduser()
    if index_dir not in _VECTOR_STORE_CACHE:
        if _EMBEDDINGS is None:
            _EMBEDDINGS = get_embeddings()
        console.log(f"Loading FAISS index from {index_dir}")
        _VECTOR_STORE_CACHE[index_dir] = FAISS.load_local(
            str(index_dir),
            _EMBEDDINGS,
            allow_dangerous_deserialization=True,
        )
    return _VECTOR_STORE_CACHE[index_dir]


def _normalize_document(doc: Document) -> SearchResult:
    """Convert a LangChain Document into a display-friendly result."""

    source = doc.metadata.get("source", "unknown")
    preview = shorten(doc.page_content.replace("\n", " "), width=240, placeholder="…")
    return SearchResult(source=source, preview=preview)


def _synthesize_answer(results: list[SearchResult]) -> str:
    """Produce a lightweight summary using the best match."""

    if not results:
        return "No supporting documents were found."
    return (
        "Based on the local knowledge base, here's the most relevant context: "
        f"{results[0].preview}"
    )
