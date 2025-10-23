"""FAISS vector backend (FlatIP index, snapshot, S3 sync)."""

import faiss
import numpy as np


class FaissBackend:
    """FAISS vector backend for similarity search."""

    def __init__(self, dim: int = 384) -> None:
        """Initialize FAISS backend with given dimension."""
        self.index = faiss.IndexFlatIP(dim)
        self.dim = dim
        self.texts: list[str] = []
        self.metadatas: list[dict[str, object]] = []

    def add(self, texts: list[str], metadatas: list[dict[str, object]]) -> None:
        """Add texts and metadata to the index."""
        # Embed texts externally, add vectors here
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def search(self, query_vec: np.ndarray, k: int) -> list[tuple[str, dict[str, object], float]]:
        """Search for k nearest neighbors."""
        distances, indices = self.index.search(np.array([query_vec]), k)  # type: ignore
        return [
            (self.texts[i], self.metadatas[i], float(distances[0][idx]))
            for idx, i in enumerate(indices[0])
        ]

    def persist(self, path: str) -> None:
        """Persist the index to disk."""
        faiss.write_index(self.index, path)

    def load(self, path: str) -> None:
        """Load the index from disk."""
        self.index = faiss.read_index(path)

    def push_s3(self) -> None:
        """Push index to S3 (stub)."""
        # S3 sync stub
        pass

    def pull_s3(self) -> None:
        """Pull index from S3 (stub)."""
        # S3 sync stub
        pass
