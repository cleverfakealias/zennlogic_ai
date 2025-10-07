from __future__ import annotations

"""Tests for the RAG ingestion and search workflow."""

from pathlib import Path

import pytest

from app.tools.ingest import build_index
from app.tools import rag


@pytest.fixture()
def temp_docs(tmp_path: Path) -> Path:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "intro.md").write_text(
        "LangGraph agents can call MCP tools to augment their reasoning capabilities.",
        encoding="utf-8",
    )
    return docs_dir


@pytest.fixture()
def temp_index(tmp_path: Path) -> Path:
    index_dir = tmp_path / "index"
    index_dir.mkdir()
    return index_dir


def test_build_index_and_search_returns_results(temp_docs: Path, temp_index: Path) -> None:
    summary = build_index(temp_docs, temp_index)
    assert "Indexed" in summary

    output = rag.search("What can LangGraph agents do?", index_dir=temp_index)
    assert "Matches" in output
    assert "LangGraph" in output
