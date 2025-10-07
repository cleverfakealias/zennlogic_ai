from __future__ import annotations

"""CLI for building or refreshing the local FAISS index."""

from pathlib import Path

import typer
from rich.console import Console

from app.settings import get_settings
from app.tools.ingest import build_index

app = typer.Typer(help="Build the local FAISS index used by the MCP RAG tools.")
console = Console()


@app.command()
def run(
    docs: Path = typer.Option(
        None,
        help="Directory containing source documents.",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    index: Path = typer.Option(
        None,
        help="Directory where the FAISS index should be stored.",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """Trigger ingestion with optional overrides for docs and index paths."""

    settings = get_settings()
    docs_dir = docs or settings.docs_dir
    index_dir = index or settings.index_dir
    summary = build_index(docs_dir=docs_dir, index_dir=index_dir)
    console.print(summary)


def main() -> None:
    """Entry point when executed as ``python -m scripts.build_index``."""

    app()


if __name__ == "__main__":
    main()
