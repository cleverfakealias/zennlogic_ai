"""Embeddings interface and helpers."""

from typing import Any, cast

from sentence_transformers import SentenceTransformer

from service.config import settings


class Embeddings:
    """Text embeddings using sentence transformers."""

    def __init__(self) -> None:
        """Initialize embeddings model."""
        self.model: Any = SentenceTransformer(settings.embed_model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for texts."""
        raw = self.model.encode(texts, convert_to_numpy=True).tolist()
        # The third-party model returns a nested list shape; cast for mypy.
        return cast(list[list[float]], raw)
