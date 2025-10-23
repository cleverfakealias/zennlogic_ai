import numpy as np
import pytest

from zennlogic_ai_service.rag.vector_backends.factory import get_vector_backend


@pytest.mark.parametrize("backend", ["faiss", "annoy"])
def test_vector_backend_add_search(backend):
    vec = get_vector_backend(384)
    vec.add(["hello"], [{"id": 1}])
    results = vec.search(np.array([0.0] * 384), 1)
    assert isinstance(results, list)
