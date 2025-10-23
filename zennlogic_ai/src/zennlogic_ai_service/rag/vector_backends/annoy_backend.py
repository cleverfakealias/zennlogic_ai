"""Annoy vector backend (cosine metric, snapshot, S3 sync)."""

from annoy import AnnoyIndex


class AnnoyBackend:
    """Annoy vector backend for similarity search."""

    def __init__(self, dim: int = 384) -> None:
        """Initialize Annoy backend with given dimension."""
        self.index = AnnoyIndex(dim, "angular")
        self.dim = dim
        self.texts: list[str] = []
        self.metadatas: list[dict[str, object]] = []

    def add(self, texts: list[str], metadatas: list[dict[str, object]]) -> None:
        """Add texts and metadata to the index."""
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def search(self, query_vec: list[float], k: int) -> list[tuple[str, dict[str, object], float]]:
        """Search for k nearest neighbors."""
        idxs = self.index.get_nns_by_vector(query_vec, k, include_distances=True)
        return [(self.texts[i], self.metadatas[i], float(d)) for i, d in zip(*idxs, strict=False)]

    def persist(self, path: str) -> None:
        """Persist the index to disk."""
        self.index.save(path)

    def load(self, path: str) -> None:
        """Load the index from disk."""
        self.index.load(path)

    def push_s3(self) -> None:
        """Push index to S3 (stub)."""
        # S3 sync stub
        pass

    def pull_s3(self) -> None:
        """Pull index from S3 (stub)."""
        # S3 sync stub
        pass
