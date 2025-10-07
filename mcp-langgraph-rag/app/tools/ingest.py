from __future__ import annotations

"""Document ingestion pipeline that builds a FAISS index from local files."""

from collections.abc import Iterable
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from rich.console import Console
from rich.progress import track

from app.settings import get_settings

_CHUNK_SIZE = 800
_CHUNK_OVERLAP = 80
_SUPPORTED_SUFFIXES: tuple[str, ...] = (".md", ".txt", ".markdown", ".mdown", ".pdf")
console = Console()


def build_index(docs_dir: Path, index_dir: Path) -> str:
    """Build or update the FAISS index using documents from ``docs_dir``."""

    docs_dir = Path(docs_dir).expanduser()
    index_dir = Path(index_dir).expanduser()
    if not docs_dir.exists() or not any(docs_dir.iterdir()):
        raise FileNotFoundError(f"No documents found in {docs_dir}")

    documents = list(_load_documents(docs_dir))
    if not documents:
        raise ValueError(f"No supported documents discovered in {docs_dir}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=_CHUNK_SIZE,
        chunk_overlap=_CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    split_docs = splitter.split_documents(documents)

    embeddings = get_embeddings()
    if _index_exists(index_dir):
        store = FAISS.load_local(str(index_dir), embeddings, allow_dangerous_deserialization=True)
        store.add_documents(split_docs)
    else:
        store = FAISS.from_documents(split_docs, embeddings)

    index_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(index_dir))

    summary = f"Indexed {len(split_docs)} chunks from {len(documents)} documents."
    console.log(summary)
    return summary


def get_embeddings() -> Embeddings:
    """Return embeddings backed by OpenAI or a deterministic local fallback."""

    settings = get_settings()
    if settings.openai_api_key:
        return OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
        )
    console.log("OPENAI_API_KEY missing; using FakeEmbeddings for local development.")
    return FakeEmbeddings(size=1536)


def _index_exists(index_dir: Path) -> bool:
    """Determine whether a FAISS index already exists at the path."""

    index_dir = index_dir.expanduser()
    return index_dir.exists() and any(index_dir.glob("*.faiss"))


def _load_documents(docs_dir: Path) -> Iterable[Document]:
    """Load supported text documents and emit LangChain ``Document`` objects."""

    paths = sorted(path for path in docs_dir.rglob("*") if path.is_file())
    for path in track(paths, description="Reading documents"):
        suffix = path.suffix.lower()
        if suffix not in _SUPPORTED_SUFFIXES:
            continue
        metadata = {"source": str(path.relative_to(docs_dir))}
        if suffix == ".pdf":
            loader = PyPDFLoader(str(path))
            for document in loader.load():
                document.metadata.setdefault("source", metadata["source"])
                yield document
            continue
        text = path.read_text(encoding="utf-8")
        yield Document(page_content=text, metadata=metadata)
