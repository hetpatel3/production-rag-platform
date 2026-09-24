import uuid
from qdrant_client.models import PointStruct

from app.core.config import get_settings
from app.core.qdrant import get_qdrant_client, ensure_collection
from app.ingestion.chunker import chunk_text
from app.ingestion.embedder import embed_texts, get_vector_size


def ingest_text(text: str, source: str) -> int:
    """Chunk, embed and store a document. Returns the number of chunks stored."""
    settings = get_settings()

    chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        return 0

    vectors = embed_texts(chunks)
    ensure_collection(get_vector_size())

    points = [
        PointStruct(
            # Use a deterministic UUID based on the source and chunk index to avoid duplicates
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}:{i}")),
            vector=vector,
            payload={"text": chunk, "source": source, "chunk_index": i},
        )
        for i, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]

    get_qdrant_client().upsert(collection_name=settings.collection_name, points=points)
    return len(points)