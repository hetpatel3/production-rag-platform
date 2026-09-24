from app.core.config import get_settings
from app.core.qdrant import get_qdrant_client
from app.ingestion.embedder import embed_query


def retrieve_chunks(query: str, top_k: int | None = None) -> list[dict]:
    settings = get_settings()
    top_k = top_k or settings.top_k

    query_vector = embed_query(query)
    results = get_qdrant_client().query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        limit=top_k,
    ).points

    return [
        {
            "text": r.payload.get("text", ""),
            "source": r.payload.get("source", ""),
            "chunk_index": r.payload.get("chunk_index"),
            "score": r.score,
        }
        for r in results
        if r.payload
    ]