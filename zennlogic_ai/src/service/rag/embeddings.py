"""Embeddings interface and helpers."""

from sentence_transformers import SentenceTransformer
from zennlogic_ai_service.config import settings


class Embeddings:
    """Text embeddings using sentence transformers."""

    def __init__(self):
        """Initialize embeddings model."""
        self.model = SentenceTransformer(settings.embed_model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for texts."""
        return self.model.encode(texts, convert_to_numpy=True).tolist()
