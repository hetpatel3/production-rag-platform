from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from app.core.config import get_settings


@lru_cache
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=get_settings().qdrant_url)


def ensure_collection(vector_size: int) -> None:
    client = get_qdrant_client()
    name = get_settings().collection_name
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )