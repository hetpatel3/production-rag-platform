from functools import lru_cache
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    settings = get_settings()
    return SentenceTransformer(settings.embedding_model)


def get_vector_size() -> int:
    dimension = get_embedding_model().get_embedding_dimension()
    if dimension is None:
        raise RuntimeError("Embedding model does not provide a vector size")
    return dimension


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed many texts at once (used when ingesting chunks)."""
    vectors = get_embedding_model().encode(texts)
    return vectors.tolist()


def embed_query(query: str) -> list[float]:
    """Embed one text (used at question time)."""
    return get_embedding_model().encode(query).tolist()