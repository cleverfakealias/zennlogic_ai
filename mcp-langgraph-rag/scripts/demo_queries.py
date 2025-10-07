from __future__ import annotations

"""CLI for issuing demo queries against the local RAG stack."""

from pathlib import Path

import typer
from rich.console import Console

from app.settings import get_settings
from app.tools import rag

app = typer.Typer(help="Query the local FAISS index and display formatted results.")
console = Console()


@app.command()
def run(
    question: str = typer.Argument(..., help="Question to ask the knowledge base."),
    k: int = typer.Option(4, help="Number of top matches to return."),
    index: Path = typer.Option(
        None,
        help="Override the index directory used for the search.",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """Perform the RAG search and render the markdown output to the console."""

    settings = get_settings()
    index_dir = index or settings.index_dir
    result = rag.search(question, k=k, index_dir=index_dir)
    console.print(result)


def main() -> None:
    """Entry point when executed as ``python -m scripts.demo_queries``."""

    app()


if __name__ == "__main__":
    main()
