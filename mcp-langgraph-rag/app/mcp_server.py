from __future__ import annotations

"""MCP server exposing LangGraph and RAG capabilities via fastmcp."""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

from fastmcp.server import FastMCP

from app.settings import get_settings
from app.tools import notes, rag
from app.tools.ingest import build_index

server = FastMCP(name="langgraph-rag-mcp")


@server.tool()
def rag_search(query: str, k: int = 4) -> str:
    """Run a semantic search over the local FAISS index."""

    return rag.search(query, k=k)


@server.tool()
def write_note(text: str) -> str:
    """Append a note to the persistent notes store."""

    entry = notes.append_note(text)
    return f"Stored note: {entry.strip()}"


@server.tool()
def ingest_docs(glob: str | None = None) -> str:
    """Trigger synchronous ingestion of documents into the FAISS index."""

    settings = get_settings()
    docs_dir = settings.docs_dir

    if glob:
        matches = sorted(path for path in docs_dir.glob(glob) if path.is_file())
        if not matches:
            return f"No documents matched pattern '{glob}'."
        console_message = f"Ingesting {len(matches)} documents matching '{glob}'."
        with TemporaryDirectory() as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            for source in matches:
                relative = source.relative_to(docs_dir)
                destination = temp_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            summary = build_index(docs_dir=temp_dir, index_dir=settings.index_dir)
        return f"{console_message} {summary}"

    console_message = "Ingesting all documents."
    summary = build_index(docs_dir=docs_dir, index_dir=settings.index_dir)
    return f"{console_message} {summary}"


REGISTERED_TOOL_NAMES = {"rag_search", "write_note", "ingest_docs"}


def main() -> None:
    """Entry point for executing the MCP server via ``python -m``."""

    server.run()


if __name__ == "__main__":
    main()
