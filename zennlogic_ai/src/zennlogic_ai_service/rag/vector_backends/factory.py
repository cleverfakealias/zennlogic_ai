"""Vector backend factory: choose FAISS or Annoy."""

from .faiss_backend import FaissBackend


def get_vector_backend(dim: int = 384) -> FaissBackend:
    """Get FAISS vector backend instance only."""
    return FaissBackend(dim)
