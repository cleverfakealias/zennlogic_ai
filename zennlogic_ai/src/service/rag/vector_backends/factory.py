"""Vector backend factory: choose FAISS or Annoy based on settings."""

from typing import Any

from service.config import settings

from .annoy_backend import AnnoyBackend
from .faiss_backend import FaissBackend


def get_vector_backend(dim: int = 384) -> Any:
    """Get a vector backend instance according to configuration.

    Falls back to an available backend when set to "auto".
    """
    backend = settings.vector_backend
    if backend == "faiss":
        return FaissBackend(dim)
    if backend == "annoy":
        return AnnoyBackend(dim)
    # auto-detect: prefer faiss if importable
    try:
        import faiss  # noqa: F401

        return FaissBackend(dim)
    except Exception:
        return AnnoyBackend(dim)
